import ast
from django.http import JsonResponse

from xf.uc_dashboards.views.widget_view import WidgetView


class PagedTableWidgetView(WidgetView):

    def __init__(self):
        super().__init__()
        self.draw: int = None
        self.length: int = None
        self.records_total: int = None
        self.offset = None
        self.offset_by: int = None

    def dispatch(self, request, *args, **kwargs):
        """
        Unpack paging information sent by the client
        """
        self.draw = int(request.GET['draw']) if 'draw' in request.GET else 1
        self.length = int(request.GET['length']) if 'length' in request.GET else 0
        self.offset_by = int(request.GET['start'])
        return super(PagedTableWidgetView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        """
        Generate the desired response format including information required to display
        the right paging by the client.
        """
        context = self.get_context_data(**kwargs)

        if 'format' in self.kwargs and self.kwargs['format'] == 'json':
            json_data = {
                'draw': self.draw,
                'recordsTotal': self.records_total,
                'recordsFiltered': self.records_total,
                'data': context['rows']
            }
            return JsonResponse(json_data)

        return self.render_to_response(context)


    def load_widget_data(self, context):
        """
        Before loading, we check if the offset details were provided in attributes.
        """
        attributes = self.widget.custom_attributes if self.widget.dataset is None else self.widget.dataset.custom_attributes
        custom_attributes = ast.literal_eval("{ %s }" % attributes)
        if 'offset' in custom_attributes:
            self.offset = custom_attributes['offset']
        else:
            self.offset = 'OFFSET @offset'
        super().load_widget_data(context)


    def execute_sql_query(self, conn, sql_query):
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            self.records_total = cursor.rowcount
            rows = cursor.fetchmany(self.length)

            # some DBs such as SQLite will return -1 as rowcount
            # as a workaround, we extend the page by one more page every time until no more records are available
            if self.records_total == -1:
                self.records_total = self.offset_by + len(rows) + self.length
        finally:
            # conn.close()
            pass
        return rows


    def add_parameters_to_query(self, conn, params, sql_query, query_filters):
        """
        Append the offset details to query if provided. If length is -1, a full dataset download was requested
        """
        if self.offset and self.length != -1:
            sql_query += ' {}'.format(self.offset)
            sql_query = sql_query.replace('@offset', str(self.offset_by))
        return super().add_parameters_to_query(conn, params, sql_query, query_filters)


    def result_set_to_dict(self, result_set, widget_keys, result_set_keys=None):
        """
        Uses all columns in the dataset rather than just the ones displayed on widget
        """
        if result_set_keys is not None:
            widget_keys = result_set_keys
        return super().result_set_to_dict(result_set, widget_keys, result_set_keys)
