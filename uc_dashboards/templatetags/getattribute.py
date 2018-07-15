
__author__ = 'Fitti'

# app/templatetags/getattribute.py
# http://stackoverflow.com/questions/844746/performing-a-getattr-style-lookup-in-a-django-template

import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()


def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID


register.filter('getattribute', getattribute)

def get_can_do_action(value, action):
    from xf.xf_services.xf_security_service import XFSecurityService

    if XFSecurityService.security_service is not None:
        security_method_object = XFSecurityService.security_service.get_model_access_permissions(type(value))
        can_do_action_method_name = "can_do_" + action.action_name + "_instance"
        can_do_action_method = getattr(security_method_object, can_do_action_method_name, None)
        if can_do_action_method:
            return can_do_action_method(action.action_name, action.user, value)


    else:
        can_do_action_method_name = "can_do_" + action.action_name
        can_do_action_method = getattr(value, can_do_action_method_name, None)
        if can_do_action_method:
            return can_do_action_method(action.action_name, action.user)

        return True


register.filter('candoaction', get_can_do_action)