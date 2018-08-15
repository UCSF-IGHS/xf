from django.conf.urls import url
import uuid

from xf.xf_crud.generic_crud_views import XFCreateView
from xf.xf_crud.xf_classes import XFUIAction, ACTION_ROW_INSTANCE, ACTION_NEW_INSTANCE
from xf.xf_services import XFModelPermissionBase
from xf.xf_services.xf_security_service import XFSecurityService
from xf.xf_system.utilities.deprecated_decorator import xf_deprecated


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
        self.paginate_by = 10
        self.foreign_key_name = None
        self.list_url = None
        self.search_hint = "Search for.."
        self.supported_crud_operations = ['add', 'change', 'delete', 'view', 'list']
        self.search_field = None
        self.custom_column_names = None
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
        self._row_link_action_list = []
        self.row_link_default_action = None
        self._row_action_list = []
        self.row_default_action = None
        self._screen_actions = []
        self.screen_action_list = []

    @property
    def row_link_action_list(self):
        return self._row_link_action_list

    @row_link_action_list.setter
    def row_link_action_list(self, value):
        self._row_link_action_list = value

    @property
    def instance_action_list(self):
        return self._row_action_list

    @instance_action_list.setter
    def instance_action_list(self, value):
        self._row_action_list = value

    @property
    def class_action_list(self):
        return self._screen_actions

    @class_action_list.setter
    def class_action_list(self, value):
        self._screen_actions = value


    @property
    @xf_deprecated("Use class_action_list instead")
    def screen_actions(self):
        return self._screen_actions

    @screen_actions.setter
    @xf_deprecated("Use class_action_list instead")
    def screen_actions(self, value):
        self._screen_actions = value

    @property
    @xf_deprecated("Use instance_action_list instead")
    def row_action_list(self):
        return self._row_action_list

    @row_action_list.setter
    @xf_deprecated("Use instance_action_list instead")
    def row_action_list(self, value):
        self._row_action_list = value



    def initialise_action_lists(self):

        list_is_a_child_list = self.foreign_key_name is not None
        if not list_is_a_child_list:
            self.try_add_screen_action(XFUIAction('new', 'Create new', 'add', action_type=ACTION_NEW_INSTANCE, user=self.user))
        else:
            self.try_add_screen_action(
                XFUIAction('add_to', 'Add new', 'add', action_type=ACTION_NEW_INSTANCE, user=self.user))

        self.try_add_row_action(XFUIAction('edit', 'Edit', 'change', action_type=ACTION_ROW_INSTANCE, user=self.user))
        self.try_add_row_action(XFUIAction('delete', 'Delete', 'delete', action_type=ACTION_ROW_INSTANCE, user=self.user))
        self.try_add_row_action(XFUIAction('details', 'View details', 'view', action_type=ACTION_ROW_INSTANCE, use_ajax=True, user=self.user))


    def try_add_screen_action(self, action: XFUIAction):

        if self.action_is_allowed(action):
            self.class_action_list.append(action)


    def try_add_row_action(self, action: XFUIAction):

        if self.action_is_allowed(action):
            self.instance_action_list.append(action)

    def action_is_allowed(self, action: XFUIAction):

        security_method_object = self.model
        action_allowed = True
        if XFSecurityService.security_service is not None:
            model_permission = XFSecurityService.security_service.get_model_access_permissions(
                model=self.model, user=self.user, model_list=self)
            action_method_name = 'can_perform_' + action.action_name
            can_perform_method = getattr(model_permission, action_method_name, None)
            if can_perform_method is not None:
                action_allowed = can_perform_method()

        else:
            action_method_name = 'can_do_' + action.action_name
            can_do_function = getattr(security_method_object, action_method_name, None)
            if can_do_function is not None:
                action_allowed = can_do_function(security_method_object, action, self.user)

        return action_allowed

    def get_entity_action(self, action_name):
        return next((s for s in self.instance_action_list if s.action_name == action_name), None)

    def get_action(self, action_name):
        return next((s for s in self.class_action_list if s.action_name == action_name), None)


    def create_default_field_list(self):
        for field in self.model._meta.fields:
            if not field.primary_key:
                self.list_field_list.append(field.name)

    def prepare_actions(self):

        self.initialise_action_lists()

        for action in self.row_action_list:
            action.user = self.user

        for action in self.screen_actions:
            action.user = self.user



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
        auto_generated_div_id_for_use_in_template = str(uuid.uuid4()).replace("-", "_")
        self.id = auto_generated_div_id_for_use_in_template
        self.url = url
        self.caption = caption


