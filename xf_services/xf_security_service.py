from xf.xf_services import XFService, XFModelPermissionBase


class XFSecurityService(XFService):
    security_service = None

    @classmethod
    def get_model_access_permissions(cls, model, user, **kwargs):
        return XFModelPermissionBase(model=model, user=user, **kwargs)

# ASSIGN THIS TO ENABLE THIS FEATURE. IF IT IS NOT ENABLED, IT WILL BE IGNORED
#XFSecurityService.security_service = XFSecurityService

