import csv
from datetime import datetime
from django.http import HttpResponse, StreamingHttpResponse
from django.template.defaultfilters import lower
from django.urls import reverse_lazy, reverse


#from xf.xf_crud.xf_classes import XFUIBuilder
from io import StringIO, BytesIO
from pytz import unicode


class XFCrudMixin(object):
    app_name = ""
    form_name = ""
    model_url_part = ""

    def __init__(self):
        self.app_name = ""
        self.form_name = ""
        self.model_url_part = ""
        #self.ui_builder = XFUIBuilder(url_app_name=self.app_name, model_type=None, form_class_type=self.form_name, list_class_type=None)

    def add_crud_urls_to_context(self, context):
        context['url_name_list'] = "%s_%s_list" % (self.get_app_name(), self.get_model_name())
        context['url_name_new'] = "%s_%s_new" % (self.get_app_name(), self.get_model_name())
        context['url_name_edit'] = "%s_%s_edit" % (self.get_app_name(), self.get_model_name())
        context['url_name_delete'] = "%s_%s_delete" % (self.get_app_name(), self.get_model_name())
        context['url_name_details'] = "%s_%s_details" % (self.get_app_name(), self.get_model_name())
        context['url_name_list_filter'] = "%s_%s_list_filter" % (self.get_app_name(), self.get_model_name())
        pass

    def add_urls_to_actions_for_list_class(self, list_class, context):
        for action in list_class.row_link_action_list:
            action.url_name = self._process_url_name_with_app_and_model_name(action.url_name)
            if action.next_url is not None:
                action.next_url = reverse(action.next_url, args=(0,))

        for action in list_class.row_action_list:
            action.url_name = self._process_url_name_with_app_and_model_name(action.url_name)
            if action.next_url is not None:
                action.next_url = reverse(action.next_url, args=(0,))


        for action in list_class.screen_actions:
            action.url_name = self._process_url_name_with_app_and_model_name(action.url_name)
            if action.next_url is not None:
                action.next_url = reverse(action.next_url, args=(0,))

        for action in list_class.screen_action_list:
            action.url_name = self._process_url_name_with_app_and_model_name(action.url_name)
            if action.next_url is not None:
                action.next_url = reverse(action.next_url, args=(0,))


        if list_class.row_default_action is not None:
            list_class.row_default_action.url_name = \
                self._process_url_name_with_app_and_model_name(list_class.row_default_action.url_name)

        context['row_link_action_list'] = list_class.row_link_action_list
        context['row_action_list'] = list_class.row_action_list
        context['screen_actions'] = list_class.screen_actions
        context['screen_action_list'] = list_class.screen_action_list
        context['row_default_action'] = list_class.row_default_action

    def prepare_form_class(self):

        self.form_class = self.get_form_class()
        self.form = self.get_form(self.form_class)

        pass


    def _process_url_name_with_app_and_model_name(self, url):
        try:
            return url % (self.app_name, self.model_url_part)
        except:
            return url




    def get_app_name(self):
        return self.app_name

    def get_initial_form_data_from_querystring(self):

        initial_form_data = {}
        for key in self.request.GET:
            initial_form_data[key] = self.request.GET.get(key)
        return initial_form_data

    def get_model_name(self):

        return self.model_url_part
        in_a_list_view = hasattr(self, 'model')

        if in_a_list_view:
            return self.get_model_name_for_list_view()
        else: # in a crud view
            return self.get_model_name_for_crud_view()

    def get_model_name_for_list_view(self):
        return self.model.__name__.lower()

    def get_model_name_for_crud_view(self):
        return self.get_form_class().Meta.model.__name__.lower()


class XFExportMixin(object):

    def get_formatted_content(self):
        response_format = self.request.GET.get('format')

        if response_format == 'csv':
            complete_field_list = []
            for field in self.model._meta.fields:
                complete_field_list.append(field.name)

            export_data = self.list_class.get_queryset(self.search_string, self.model, "").\
                values_list(*complete_field_list)

            def stream():
                buffer_ = StringIO()
                writer = csv.writer(buffer_)
                write_header = True

                for row in export_data:
                    if write_header:
                        writer.writerow(complete_field_list)
                        buffer_.seek(0)
                        data = buffer_.read()
                        buffer_.seek(0)
                        buffer_.truncate()
                        yield data
                        write_header = False

                    writer.writerow(row)
                    buffer_.seek(0)
                    data = buffer_.read()
                    buffer_.seek(0)
                    buffer_.truncate()
                    yield data

            response = StreamingHttpResponse(stream(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="{}-{}.csv"'.format(lower(self.model._meta),
                                                                                        datetime.now())
            return response
