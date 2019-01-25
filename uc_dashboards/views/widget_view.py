import ast

from django.contrib.auth.views import redirect_to_login
from django.db import connections
from django.shortcuts import get_object_or_404
from django.template import TemplateDoesNotExist, Template
from django.template.loader import _engine_list
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import get_language
from django.views.generic import TemplateView

import xf.uc_dashboards
from xf.uc_dashboards.models.dataset import DataSet
from xf.uc_dashboards.models.perspective import Perspective
from xf.uc_dashboards.models.widget import Widget
from xf.uc_dashboards.views.custom_dataset_loader_base import XFCustomDataSetLoaderBase


class WidgetView(TemplateView):
    """
    Serves as a base class for widgets, which are content types of a dashboard.
    """

    def __init__(self):
        # Data columns that may be displayed
        super(WidgetView, self).__init__()
        self.data_columns = []
        self.result_set_columns = []
        self.widget = None

    def dispatch(self, request, *args, **kwargs):

        if 'slug' in self.kwargs:
            self.widget = get_object_or_404(Widget, slug=self.kwargs['slug'])

        if self.widget:
            # TODO: CRASH Gracefully
            if not self.widget.allow_anonymous:
                if not self.request.user.is_authenticated():
                    # return HttpResponseRedirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
                    return redirect_to_login(self.request.path)

            self.template_name = self.widget.template.template_path
        return super(WidgetView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Loading templates and all kinds of data here
        :param kwargs:
        :return:
        """
        context = super(WidgetView, self).get_context_data(**kwargs)
        if 'zoom' in self.request.GET:
            context["extends_template"] = "dashboards/t_dashboard_widget_zoom.html"
            context["disable_zoom"] = True
        elif self.request.is_ajax():
            context["extends_template"] = "dashboards/t_dashboard_widget_ajax_container.html"
        else:
            context["extends_template"] = "dashboards/t_dashboard_widget_container_tester.html"

        context["widget_id"] = self.__class__.__name__
        if self.widget:
            context['change_url'] = reverse('admin:uc_dashboards_widget_change', args=(self.widget.id,),
                                            current_app='uc_dashboards')

        context["widget"] = self.widget
        context['filter_query_string'] = "?" + self.request.META['QUERY_STRING']
        self.load_widget_data(context)

        return context

    def result_set_to_dict(self, result_set, widget_keys, result_set_keys=None):
        """
        This function helps to create a dictionary object out of a SQL query
        :param result_set:
        :param widget_keys:
        :param result_set_keys:
        :return:
        """

        # build dict for template:
        fdicts = []
        for row in result_set:
            i = 0
            cur_row = {}
            for key in widget_keys:
                data_index = i if result_set_keys is None else result_set_keys.index(key)
                cur_row[key] = row[data_index]
                i = i + 1
            fdicts.append(cur_row)
        return fdicts

    def result_set_to_transposed_dict(self, result_set, columns, label_column):
        """
        Transposes a recordset for use in bar charts
        :param result_set:
        :param columns:
        :param label_column:
        :return:
        """

        result = []
        for row in result_set:
            pass
        pass

    def get_connection(self, database_key):
        """
        Returns a connection object for PTBi
        :return: The connection object
        """

        # ptbi_data

        conn = connections[database_key]
        return conn

    def load_widget_data(self, context):
        """
        Loads the data for the widget. Some widget fields must be set as follows:

        The column_names field is used to extract data from the SQL result set and convert it into a dictionary.
        Each column name will become a field. There may be additional information in column names.


        :param context:
        :return:
        """

        if self.widget:

            if "perspective_slug" in self.kwargs:
                perspective = get_object_or_404(xf.uc_dashboards.models.perspective.Perspective, slug=self.kwargs["perspective_slug"])
                perspective = self.request.user.load_perspective(perspective, True)
                if perspective:
                    self.perspective = perspective
                    self.request.session["perspective_id"] = self.perspective.id

            if "perspective_id" in self.request.session:
                self.perspective = Perspective.objects.get(pk=self.request.session["perspective_id"])

            if self.widget.widget_type != Widget.TEXT_BLOCK:

                if self.widget.dataset is not None:
                    if self.widget.dataset.dataset_type == DataSet.CUSTOM:
                        rows = self.load_custom_dataset(self.widget.dataset, self.request, **self.kwargs)
                    else:
                        rows = self.load_sql_dataset(self.widget.dataset, self.request)
                else:

                    params = []
                    sql_query = self.widget.sql_query
                    conn = self.get_connection(self.widget.database_key)

                    sql_query = self.add_parameters_to_query(conn, params, sql_query, self.widget.filters)

                    rows = self.execute_sql_query(conn, sql_query)

            # print sql_query

            context["widget_id"] += self.widget.slug.replace("-", "_")
            context["widget_slug"] = self.widget.slug
            context["caption"] = self.widget.title
            context["extra_text"] = self.widget.sub_text
            context["widget_type"] = self.widget.widget_type
            context["locale_code"] = get_language()

            if self.perspective:
                context["perspective_code"] = self.perspective.code
                context["perspective_slug"] = self.perspective.slug

            # Custom attributes
            if self.widget.custom_attributes != "":
                custom_attributes = ast.literal_eval("{" + self.widget.custom_attributes + "}")
                context["custom_attr"] = custom_attributes

                # Putting back what was once lost
                for (key) in custom_attributes:
                    context[key] = custom_attributes[key]

            context["extends_base_template"] = "t_xpanel_control_base.html"

            if self.widget.widget_type == Widget.PIE or \
                            self.widget.widget_type == Widget.TABLE or \
                            self.widget.widget_type == Widget.PAGED_TABLE or \
                            self.widget.widget_type == Widget.MAP or \
                            self.widget.widget_type == Widget.FILTER_DROP_DOWN or \
                            self.widget.widget_type == Widget.TILES or \
                            self.widget.widget_type == Widget.LINE_GRAPH or \
                            self.widget.widget_type == Widget.PROGRESS_CIRCLE or \
                            self.widget.widget_type == Widget.BAR_GRAPH or \
                            self.widget.widget_type == Widget.GAUGE or \
                            self.widget.widget_type == Widget.STACKED_BAR_GRAPH or \
                            self.widget.widget_type == Widget.BAR_GRAPH_HORIZONTAL:

                widget_column_names = []
                for line in self.widget.data_columns.split('\n'):
                    # Add entire column line to data_columns array, which is passed to template
                    data_column = ast.literal_eval('{' + line + '}')
                    self.data_columns.append(data_column)
                    widget_column_names.append(data_column['column_name'])

                result_set_column_names = None
                if self.widget.dataset is not None and self.widget.dataset.data_columns != '':
                    result_set_column_names = []
                    for line in self.widget.dataset.data_columns.split('\n'):
                        data_column = ast.literal_eval('{' + line + '}')
                        self.result_set_columns.append(data_column)
                        result_set_column_names.append(data_column['column_name'])
                    context["result_set_columns"] = self.result_set_columns

                # Convert the result set from the SQL query into a dictionary
                rows = self.result_set_to_dict(rows, widget_column_names, result_set_column_names)
                context["rows"] = rows
                context["data_columns"] = self.data_columns
                if len(rows) > 0:
                    context["tile_width"] = int(12 / len(rows))

            # Data points
            if self.widget.widget_type == Widget.PIE or \
                            self.widget.widget_type == Widget.LINE_GRAPH or \
                            self.widget.widget_type == Widget.BAR_GRAPH_HORIZONTAL or \
                            self.widget.widget_type == Widget.STACKED_BAR_GRAPH or \
                            self.widget.widget_type == Widget.BAR_GRAPH:
                labels = []
                for row in rows:
                    labels.append(str(row[self.widget.label_column]))
                    # if isinstance(row[self.widget.label_column], str):
                    # UNICODE MAY FAIL HERE - without the str a 'u' will be added
                    #    labels.append(str(row[self.widget.label_column]))
                    # else:
                    #    labels.append("XXX")

                context["labels"] = str(labels).replace("'", '"')

                # Data points is what will actually hold the data. For a pie, this will be an array.
                # For a line or bar chart, it will be several arrays. Therefore, everything will be
                # wrapped into an array of arrays - with only one element for pie
                datapoints = []
                legend_labels = []
                chart_types = []
                y_axis = []
                for column in self.widget.data_point_column.split('\n'):

                    # create a dictionary like {'legend_label': 'number of admissions', 'column_name': 'admissions'}
                    data_point_column_description = ast.literal_eval('{' + column + '}')
                    # if data_point_column_description.has_key('legend_label'):
                    # PYTHON3 UPDATE
                    if "legend_label" in data_point_column_description:
                        legend_labels.append(data_point_column_description['legend_label'])
                    if "chart_type" in data_point_column_description:
                        chart_types.append(data_point_column_description['chart_type'])
                    else:
                        chart_types.append('bar')
                    if "y_axis" in data_point_column_description:
                        y_axis.append(data_point_column_description['y_axis'])
                    else:
                        y_axis.append('0')
                    # single row with data points, for a line chart with 2 lines will have two of them
                    datapoint_row = []
                    for row in rows:
                        datapoint_row.append(str(row[data_point_column_description['column_name']]))

                    datapoints.append(str(datapoint_row).replace("'", ''))
                context["datapoints"] = datapoints
                context["legend_labels"] = legend_labels
                context["chart_types"] = chart_types
                context["y_axis"] = y_axis

            # This variable determines whether the "view data" command is available in the widget. Only
            # available for widgets that support it.
            context["supports_view_data"] = True if \
                self.widget.widget_type == Widget.LINE_GRAPH or \
                self.widget.widget_type == Widget.BAR_GRAPH or \
                self.widget.widget_type == Widget.BAR_GRAPH_HORIZONTAL or \
                self.widget.widget_type == Widget.GAUGE or \
                self.widget.widget_type == Widget.STACKED_BAR_GRAPH or \
                self.widget.widget_type == Widget.PIE \
                else False

    def execute_sql_query(self, conn, sql_query):
        if self.widget.widget_type == Widget.PAGED_TABLE:
            return {} # paged table will get data later by api
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
        finally:
            # conn.close()
            pass
        return rows

    def add_parameters_to_query(self, conn, params, sql_query, query_filters):
        if query_filters:
            filters = ast.literal_eval(query_filters)
            for filter in filters:
                multiselect = filter.endswith('[]')
                filter = filter[:-2] if multiselect else filter
                params.append(self.request.GET.get(filter, ''))
                try:
                    sql_query = sql_query.replace("@" + filter, conn.literal(
                        "'" + "', '".join(self.request.GET.getlist(filter, '')) + "'"
                        if multiselect else conn.literal(self.request.GET.get(filter, ''))))
                except:
                    # UNSAFE!!!!
                    # TODO: FIX
                    sql_query = sql_query.replace("@" + filter,
                                                  "'" + "', '".join(self.request.GET.getlist(filter, '')) + "'"
                                                  if multiselect else "'" + self.request.GET.get(filter,
                                                                                                 '') + "'")
        # Add a perspective code as a filter, which allows you to filter any widget based on the current perspective
        # Very useful if you want to filter a filter based on a perspective
        if self.perspective:
            sql_query = sql_query.replace("@perspective_code", self.perspective.code)
        # Send the locale code to the database
        locale = get_language()
        sql_query = sql_query.replace("@locale_code", locale)
        # Send current user to the database
        if not self.request.user.is_anonymous and self.request.user.is_authenticated:
            sql_query = sql_query.replace("@user_id", str(self.request.user.id))

        return sql_query

    def get_template2(self, template_name, using=None):
        """
        Loads and returns a template for the given name.

        Raises TemplateDoesNotExist if no such template exists.
        """
        chain = []
        engines = _engine_list(using)
        for engine in engines:
            try:
                return engine.get_template(template_name)
            except TemplateDoesNotExist as e:
                chain.append(e)

        raise TemplateDoesNotExist(template_name, chain=chain)

    def response_class(self, request, template, context, **response_kwargs):
        """
        We are overloading this method so that it can inject a template that is loaded with content from the database,
        if necessary. If the template is supposed to come from a template file (in the file system), nothing happens
        and we just call the super class' method.
        :param request:
        :param template:
        :param context:
        :param response_kwargs:
        :return:
        """
        if self.widget:
            if int(self.widget.template.template_source) == int(xf.uc_dashboards.models.template.Template.DATABASE):
                template = Template(self.widget.template.template_text)
                template2 = self.get_template2(template_name="dashboards/t_ibbs_overview.html")
                template2.template = template

                # We need to return the template here directly
                return super(WidgetView, self).response_class(request, template2, context, **response_kwargs)
                t = TemplateResponse(request, template)
                return t

        return super(WidgetView, self).response_class(request, template, context, **response_kwargs)

    def load_sql_dataset(self, dataset: DataSet, request):

        if dataset.custom_daset_loader is not None and dataset.custom_daset_loader != '':
            return self.load_custom_dataset(dataset, request)

        params = []
        sql_query = dataset.sql_query
        conn = self.get_connection(dataset.database_key)

        sql_query = self.add_parameters_to_query(conn, params, sql_query, dataset.filters)

        rows = self.execute_sql_query(conn, sql_query)

        return rows

    def load_custom_dataset(self, dataset: DataSet, request, **kwargs):

        dataset_class = self._load_custom_dataset_class(dataset.custom_daset_loader)
        dataset_loader: XFCustomDataSetLoaderBase = dataset_class()
        return dataset_loader.load_dataset(dataset, request, **kwargs)

    def _load_custom_dataset_class(self, class_name: str):
        components = class_name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
