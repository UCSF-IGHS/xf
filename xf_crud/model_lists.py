from django.conf.urls import url
import uuid

from xf.xf_crud.generic_crud_views import XFCreateView
from xf.xf_crud.xf_classes import XFUIAction, ACTION_ROW_INSTANCE, ACTION_NEW_INSTANCE


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

        #for field in self.initial:
        #    self.fields[field].disabled = True


class XFModelList(XFCrudAssetLoaderMixIn):

    def __init__(self, model):
        super(XFModelList, self).__init__()
        self.model = model
        self.list_field_list = []
        self.create_default_field_list()
        self.list_title = None
        self.list_hint = None
        self.foreign_key_name = None
        self.list_url = None
        self.search_hint = "Search for.."
        self.supported_crud_operations = ['add', 'change', 'delete', 'view', 'list']
        self.search_field = None
        self.preset_filters = {
            'all': 'All',
        }
        self.action_list = {}
        self.user = None
        self.request = None
        self.kwargs = None

        #Action lists represents the actions that we can do in a list. We have 3 types:
        # Those that apply to a particular record – i.e. a row so Edit, Details, Delete
        # Those that don't apply to a record, but to a class – i.e. New
        # Search
        self.row_action_list = []
        self.row_default_action = None
        self.screen_actions = []
        self.screen_action_list = []
        self.initialise_action_lists()

    def initialise_action_lists(self):
        self.screen_actions.append(
            XFUIAction('new', 'Create new', 'add', action_type=ACTION_NEW_INSTANCE, user=self.user)
        )

        self.row_action_list.extend(
            (XFUIAction('edit', 'Edit', 'change', action_type=ACTION_ROW_INSTANCE, user=self.user),
             XFUIAction('delete', 'Delete', 'delete', action_type=ACTION_ROW_INSTANCE, user=self.user),
             XFUIAction('details', 'View details', 'view', action_type=ACTION_ROW_INSTANCE, use_ajax=True, user=self.user))
        )

    def get_entity_action(self, action_name):
        return next((s for s in self.row_action_list if s.action_name == action_name), None)

    def get_action(self, action_name):
        return next((s for s in self.screen_actions if s.action_name == action_name), None)


    def create_default_field_list(self):
        for field in self.model._meta.fields:
            if not field.primary_key:
                self.list_field_list.append(field.name)

    def prepare_actions(self):
        pass

    def get_queryset(self, search_string, model, preset_filter, view_kwargs=None):

        qs = model._default_manager.all()

        try:
            qs = qs.filter(** {self.foreign_key_name: view_kwargs['related_fk']})
        except:
            pass

        try:
            if not search_string is None:
                kwargs = {
                    '{0}__{1}'.format(self.search_field, 'icontains'): search_string
                }
                qs_search = qs.filter(**kwargs)
                return qs_search
        except:
            return qs


class XFDivLoader:

    def __init__(self,
                 caption = None,
                 url = None):
        self.id = str(uuid.uuid4()).replace("-", "_")
        self.url = url
        self.caption = caption


