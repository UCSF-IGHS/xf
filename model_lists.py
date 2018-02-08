from django.conf.urls import url

from xf_crud.generic_crud_views import XFCreateView


class XFCrudAssetLoaderMixIn(object):

    def __init__(self):
        super(XFCrudAssetLoaderMixIn, self).__init__()
        self.js_assets = []
        self.css_assets = []

    def add_javascript(self, js_file):
        self.js_assets.append(js_file)

    def add_stylesheet(self, css_file):
        self.css_assets.append(css_file)

    def add_assets_to_context(self, context):
        context['crud_js_assets'] = self.js_assets
        context['crud_css_assets'] = self.css_assets


class XFModelList(XFCrudAssetLoaderMixIn):

    def __init__(self, model):
        super(XFModelList, self).__init__()
        self.model = model
        self.list_field_list = []
        self.create_default_field_list()
        self.list_title = None
        self.list_hint = None
        self.search_hint = "Search for.."
        self.supported_crud_operations = ['add', 'change', 'delete', 'view', 'list']
        self.search_field = None
        self.preset_filters = {
            'all': 'All',
        }



    def create_default_field_list(self):
        for field in self.model._meta.fields:
            if not field.primary_key:
                self.list_field_list.append(field.name)

    def get_queryset(self, search_string, model, preset_filter):

        try:
            if not search_string is None:
                kwargs = {
                    '{0}__{1}'.format(self.search_field, 'icontains'): search_string
                }
                queryset = model._default_manager.filter(**kwargs)
                return queryset
        except:
            return model._default_manager.all()


# DO NOT USE
class XFModelList2:

    #crud_url_generator = XFCrudUrlGenerator()  #static

    def __init__(self, model):
        super(XFModelList2, self).__init__()
        self.model = model
        self.list_field_list = []
        self.create_default_field_list()
        self.list_title = None
        self.list_hint = None
        self.search_hint = "Search for.."
        self.supported_crud_operations = ['add', 'change', 'delete', 'view',]
        self.search_field = None
        self.preset_filters = {
            'all': 'All',
        }



    def create_default_field_list(self):
        for field in self.model._meta.fields:
            if not field.primary_key:
                self.list_field_list.append(field.name)

    def get_queryset(self, search_string, model, preset_filter):

        try:
            if not search_string is None:
                kwargs = {
                    '{0}__{1}'.format(self.search_field, 'icontains'): search_string
                }
                queryset = model._default_manager.filter(**kwargs)
                return queryset
        except:
            return model._default_manager.all()


# DO NOT USE
class XFCrudUrlGenerator:
    pass
    #def generate_add_urls(self):
    #    return url(r'^%s/%s/new' % (appname, modelname),
    #               XFCreateView.as_view(model=model_type, form_class=form_class_type,
    #                                    success_url="%s/%s/" % (appname, modelname),
    #                                    app_name=appname, model_url_part=modelname),
    #               name="%s_%s_new" % (appname, modelname))


