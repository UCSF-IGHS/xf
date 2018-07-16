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
        self.security_service.ensure_user_has_model_permission(self.model, self.user, 'add')
        return True

    def can_do_edit(self):
        self.security_service.ensure_user_has_model_permission(self.model, self.user, 'change')
        return True

    def can_do_edit_instance(self):
        self.security_service.ensure_user_has_model_permission(self.model, self.user, 'change')
        return True

    def can_do_delete(self):
        self.security_service.ensure_user_has_model_permission(self.model, self.user, 'delete')
        return True

    def can_do_delete_instance(self):
        self.security_service.ensure_user_has_model_permission(self.model, self.user, 'delete')
        return True

    def can_do_details(self):
        self.security_service.ensure_user_has_model_permission(self.model, self.user, 'view')
        return True

    def can_do_details_instance(self):
        self.security_service.ensure_user_has_model_permission(self.model, self.user, 'view')
        return True

    def can_do_list(self):
        self.security_service.ensure_user_has_model_permission(self.model, self.user, 'list')
        return True

