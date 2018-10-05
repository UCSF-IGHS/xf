from enum import Enum

from django.contrib.auth.models import User
from django.db.models.base import ModelBase

from xf.xf_services.xf_business_logic_exceptions import XFInvalidModelStateException, \
    XFBusinessRuleViolationException, XFBusinessLogicExceptionBase, XFPermissionDeniedException

from xf.xf_services.xf_model_state_mixin import XFModelStateMixIn, XFModelState


class XFServiceLayer:
    pass


class XFService:

    class RequesterType(Enum):
        CLASS = 1,
        INSTANCE = 2

    def __init__(self, requester, user) -> None:
        super().__init__()
        self._user = user
        self._requester: XFModelStateMixIn = requester
        self.user_service = None
        self._set_class_or_instance_type()

    def _set_class_or_instance_type(self):
        if isinstance(self._requester, ModelBase):
            self.requester_type = XFService.RequesterType.CLASS
        else:
            self.requester_type = XFService.RequesterType.INSTANCE

    # @classmethod
    # def ensure_business_rule(cls, condition, message=None, business_rule_number=None):
    #     if not condition:
    #         raise XFBusinessRuleViolationException(message)
    #
    # @classmethod
    # def ensure_model_is_in_state(cls, model: XFModelStateMixIn, state: XFModelState,
    #                              message=None, business_rule_number=None):
    #     if not model.is_in_state(state):
    #         raise XFInvalidModelStateException(message)
    #
    # @classmethod
    # def ensure_model_is_in_states(cls, model: XFModelStateMixIn, states,
    #                               message=None, business_rule_number=None):
    #     for state in states:
    #         cls.ensure_model_is_in_state(model, state, message)
    #
    # @classmethod
    # def ensure_user_has_model_permission(cls, model: ModelBase, user: User, permission):
    #
    #     if not user.has_perm("%s.%s_%s" % (self.model._meta.app_label, permission, model.__name__.lower())):
    #         raise XFPermissionDeniedException(("User does not have %s permission" % permission))

    @classmethod
    def check_is_valid(cls, check_function):
        try:
            check_function()
        except XFBusinessLogicExceptionBase:
            return False

        return True

