
class XFModelPermissionBase:
    model = None
    security_service = None

    @classmethod
    def can_do_new(cls, user):
        cls.security_service.ensure_user_has_model_permission(cls.model, user, 'add')

    @classmethod
    def can_do_edit(cls, user, physical_exam):
        cls.security_service.ensure_user_has_model_permission(cls.model, user, 'change')

    @classmethod
    def can_do_delete(cls, user, physical_exam):
        cls.security_service.ensure_user_has_model_permission(cls.model, user, 'delete')

    @classmethod
    def can_do_view_details(cls, user, physical_exam):
        cls.security_service.ensure_user_has_model_permission(cls.model, user, 'view')

    @classmethod
    def can_do_list(cls, user, physical_exam):
        cls.security_service.ensure_user_has_model_permission(cls.model, user, 'list')
