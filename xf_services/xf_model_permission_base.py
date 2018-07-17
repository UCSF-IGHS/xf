import inspect

from xf.xf_services.xf_business_rules_checks import XFBusinessRulesChecks


class XFModelPermissionBase:
    security_service: XFBusinessRulesChecks = XFBusinessRulesChecks()

    def __init__(self, model=None, user=None, *args, **kwargs) -> None:
        self.user = user
        self.model = model if inspect.isclass(model) else type(model)
        self.model_list = kwargs.get('model_list', None)
        self.model_instance = model if not inspect.isclass(model) else None
        super().__init__()

    def can_do_new(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'add')
        except:
            return False

        return True

    def can_do_edit(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'change')
        except:
            return False
        return True

    def can_do_edit_instance(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'change')
        except:
            return False

        return True

    def can_do_delete(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'delete')
        except:
            return False

        return True

    def can_do_delete_instance(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'delete')
        except:
            return False

        return True

    def can_do_details(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'view')
        except:
            return False

        return True

    def can_do_details_instance(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'view')
        except:
            return False

        return True

    def can_do_list(self):
        try:
            self.security_service.ensure_user_has_model_permission(self.model, self.user, 'list')
        except:
            return False

        return True

    def get_field_list(self, fields, action):

        return fields