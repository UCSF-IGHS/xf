

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
        self.default_permissions = ('add', 'change', 'delete', 'view')
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


