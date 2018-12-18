from django.http import JsonResponse

from xf.uc_dashboards.views.widget_view import WidgetView


class WidgetDataView(WidgetView):

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if 'format' in self.kwargs and self.kwargs['format'] == 'json':
            draw = int(request.GET['draw']) if 'draw' in request.GET else 1
            json_data = {
                'draw': draw,
                'recordsTotal': len(context['rows']),
                'recordsFiltered': len(context['rows']),
                'data': context['rows']
            }
            return JsonResponse(json_data)

        return self.render_to_response(context)
