from django.contrib.auth.models import User
from django.db.models.base import ModelBase

from xf.xf_services import XFBusinessRuleViolationException, XFModelStateMixIn, XFModelState, \
    XFInvalidModelStateException, XFPermissionDeniedException


class XFBusinessRulesChecks:
    """
    This class is meant to describe a mixin that implements business rules.
    """
    pass


    @classmethod
    def ensure_business_rule(cls, condition, message=None, business_rule_number=None):
        if not condition:
            raise XFBusinessRuleViolationException(message)

    @classmethod
    def ensure_model_is_in_state(cls, model: XFModelStateMixIn, state: XFModelState,
                                 message=None, business_rule_number=None):
        if not model.is_in_state(state):
            raise XFInvalidModelStateException(message)

    @classmethod
    def ensure_model_is_in_states(cls, model: XFModelStateMixIn, states,
                                  message=None, business_rule_number=None):
        for state in states:
            cls.ensure_model_is_in_state(model, state, message)

    @classmethod
    def ensure_user_has_model_permission(cls, model: ModelBase, user: User, permission):

        if user is not None:
            if not user.has_perm("%s.%s_%s" % (model._meta.app_label, permission, model.__name__.lower())):
                raise XFPermissionDeniedException(("User does not have %s permission" % permission))
