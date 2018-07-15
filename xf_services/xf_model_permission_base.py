
from xf.xf_services.xf_business_rules_checks import XFBusinessRulesChecks


class XFModelPermissionBase:
    model = None
    security_service: XFBusinessRulesChecks = XFBusinessRulesChecks()

    @classmethod
    def can_do_new(cls, action, user, **kwargs):
        model_list = kwargs['model_list']
        cls.security_service.ensure_user_has_model_permission(model_list.model, user, 'add')
        return True


    @classmethod
    def can_do_edit(cls, action, user, **kwargs):
        model_list = kwargs['model_list']
        cls.security_service.ensure_user_has_model_permission(model_list.model, user, 'change')
        return True

    @classmethod
    def can_do_edit_instance(cls, action, user, model_instance, **kwargs):
        cls.security_service.ensure_user_has_model_permission(type(model_instance), user, 'change')
        return True

    @classmethod
    def can_do_delete(cls, action, user, **kwargs):
        model_list = kwargs['model_list']
        cls.security_service.ensure_user_has_model_permission(model_list.model, user, 'delete')
        return True

    @classmethod
    def can_do_delete_instance(cls, action, user, model_instance, **kwargs):
        cls.security_service.ensure_user_has_model_permission(type(model_instance), user, 'delete')
        return True

    @classmethod
    def can_do_details(cls, action, user, **kwargs):
        model_list = kwargs['model_list']
        cls.security_service.ensure_user_has_model_permission(model_list.model, user, 'view')
        return True

    @classmethod
    def can_do_details_instance(cls, action, user, model_instance, **kwargs):
        cls.security_service.ensure_user_has_model_permission(type(model_instance), user, 'view')
        return True

    @classmethod
    def can_do_list(cls, action, user, **kwargs):
        model_list = kwargs['model_list']
        cls.security_service.ensure_user_has_model_permission(model_list.model, user, 'list')
        return True
