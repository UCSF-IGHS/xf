import inspect

from xf.xf_services.xf_business_rules_checks import XFBusinessRulesChecks
from xf.xf_system.utilities.deprecated_decorator import xf_deprecated


class XFModelPermissionBase:
    security_service: XFBusinessRulesChecks = XFBusinessRulesChecks()

    def __init__(self, model=None, user=None, *args, **kwargs) -> None:
        self.user = user
        self.model = model if inspect.isclass(model) else type(model)
        self.model_list = kwargs.get('model_list', None)
        self.model_instance = model if not inspect.isclass(model) else None

        # Support for master-child relationships
        if self.model_list is not None:
            self.foreign_key_name = self.model_list.foreign_key_name
            self.foreign_key_value = self.model_list.kwargs['related_fk'] if 'related_fk' in self.model_list.kwargs else None

        super().__init__()

    def can_perform_new(self):

        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'add')
        except:
            return False

        return True


    def can_perform_add_to(self):

        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'add')
        except:
            return False

        return True

    def can_perform_edit(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'change')
        except:
            return False
        return True

    def can_perform_edit_instance(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'change')
        except:
            return False
        return True

    def can_perform_delete(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'delete')
        except:
            return False

        return True

    def can_perform_delete_instance(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'delete')
        except:
            return False

        return True

    def can_perform_details(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'view')
        except:
            return False

        return True

    def can_perform_details_instance(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'view')
        except:
            return False

        return True

    def can_perform_list(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'list')
        except:
            return False

        return True

    def get_field_list(self, fields, action):

        return fields


    @xf_deprecated("Use can_perform instead.")
    def can_do_new(self):
        return self.can_perform_new()

    @xf_deprecated("Use can_perform instead.")
    def can_do_edit(self):
        return self.can_perform_edit()

    @xf_deprecated("Use can_perform instead.")
    def can_do_edit_instance(self):
        return self.can_perform_edit_instance()

    @xf_deprecated("Use can_perform instead.")
    def can_do_delete(self):
        return self.can_perform_delete()

    @xf_deprecated("Use can_perform instead.")
    def can_do_delete_instance(self):
        return self.can_perform_delete_instance()

    @xf_deprecated("Use can_perform instead.")
    def can_do_details(self):
        return self.can_perform_details()

    @xf_deprecated("Use can_perform instead.")
    def can_do_details_instance(self):
        return self.can_perform_details_instance()

    @xf_deprecated("Use can_perform instead.")
    def can_do_list(self):
        return self.can_perform_list()
