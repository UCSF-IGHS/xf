from django.urls import reverse_lazy


class XFCrudMixin(object):
    app_name = ""
    form_name = ""
    model_url_part = ""

    def __init__(self):
        self.app_name = ""
        self.form_name = ""
        self.model_url_part = ""

    def add_crud_urls_to_context(self, context):
        context['url_name_list'] = "%s_%s_list" % (self.get_app_name(), self.get_model_name())
        context['url_name_new'] = "%s_%s_new" % (self.get_app_name(), self.get_model_name())
        context['url_name_edit'] = "%s_%s_edit" % (self.get_app_name(), self.get_model_name())
        context['url_name_delete'] = "%s_%s_delete" % (self.get_app_name(), self.get_model_name())
        context['url_name_details'] = "%s_%s_details" % (self.get_app_name(), self.get_model_name())
        context['url_name_list_filter'] = "%s_%s_list_filter" % (self.get_app_name(), self.get_model_name())
        pass

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

