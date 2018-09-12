from django.contrib.auth.models import User
from django.http import HttpRequest

from xf.xf_services.xf_business_logic_exceptions import XFSaveException
from xf.xf_services.xf_security_service import XFSecurityService


class XFSaveService():

    @classmethod
    def get_user(cls) -> User:

        # See https://stackoverflow.com/questions/32332329/getting-the-request-user-form-pre-save-in-django
        import inspect

        request: HttpRequest = None
        for frame_record in inspect.stack():
            if frame_record[3] == 'get_response':
                request = frame_record[0].f_locals['request']
                break

        return request.user if request is not None else None

    @staticmethod
    def apply_model_access_permissions(instance):
        is_existing_object = instance.pk is not None
        if is_existing_object:
            old_instance = type(instance).objects.get(pk=instance.id)
            access_permissions = XFSecurityService.security_service.get_model_access_permissions(old_instance, XFSaveService.get_user())
            if not access_permissions.can_perform_edit_instance():
                raise XFSaveException("Object not eligible to be saved")
        else:
            access_permissions = XFSecurityService.security_service.get_model_access_permissions(instance, XFSaveService.get_user())
            if not access_permissions.can_perform_new():
                raise XFSaveException("Object not eligible to be created")


