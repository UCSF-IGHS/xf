from django.conf import settings
from django.core.urlresolvers import reverse
from django import template
import re

register = template.Library()

@register.filter(name='xf_rev')
def rev(value):
    """
    This filter returns the URL from the urls.py by using reverse. It can be used
    inside a template, such as url='login'|rev
    :param value: the name of the URL to return
    :return: the URl to return
    """
    return reverse(value)

@register.filter(name='xf_cw')
def columnwidth(value):
    """
    This filter returns a recommended column width, you can specify a column width of 3, 4 or 12 and all
    styles will be set appropriately.
    :param value:
    :return:
    """
    if value == 4:
        return "col-md-4 col-sm-4 col-xs-12"
    elif value == 2:
        return "col-md-2 col-sm-2 col-xs-12"
    elif value == 1:
        return "col-md-1 col-sm-1 col-xs-12"

    elif value == 5:
        return "col-md-5 col-sm-5 col-xs-12"
    elif value == 7:
        return "col-md-7 col-sm-7 col-xs-12"

    elif value == 3:
        return "col-md-3 col-sm-3 col-xs-12"
    elif value == 6:
        return "col-md-6 col-sm-6 col-xs-12"
    elif value == 8:
        return "col-md-8 col-sm-8 col-xs-12"
    elif value == 12:
        return "col-md-12 col-sm-12 col-xs-12"
    return "col-md-12 col-sm-12 col-xs-12"

@register.filter(name='xf_lookup')
def cut(value, arg):
    return value[arg]

@register.filter(name='xf_findforkey')
def findforkey(value, arg):
    for item in value:
        if item['key'] == arg:
            my_item = item
            break
    else:
        my_item = None

    return my_item

@register.filter(name='xf_columnnameforkey')
def column_name_for_key(columns, key):

    return findforkey(columns, key)['column_name']
    pass

#def object_for_attribute_value(objects, attribute_name, attribute_value):

@register.filter(name='column_action')
def action_for_column_index(value, arg):
    for action in value:
        if action.column_index == arg:
            return action

    return None

register.filter('boo', action_for_column_index)

@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')


@register.filter(name='cut3')
def cut3(value, arg):
    return value.replace(arg, '')



#=======================================================================================================================
# GetAttribute


numeric_test = re.compile("^\d+$")


@register.filter(name='xf_getattr')
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

register.filter('xf_getattribute', getattribute)


#=======================================================================================================================
# IIF


class IifNode(template.Node):
    def __init__(self, exp1 = None, exp2 = None, exp3 = None):
        if not exp3:
            exp3 = exp2
            exp2 = exp1
        self.exp1 = self.fix_type(exp1)
        self.exp2 = self.fix_type(exp2)
        self.exp3 = self.fix_type(exp3)

    def render(self, context):
        try:
            if isinstance(self.exp1, template.Variable):
                self.exp1 = self.exp1.resolve(context)
            if isinstance(self.exp2, template.Variable):
                self.exp2 = self.exp2.resolve(context)
            if isinstance(self.exp3, template.Variable):
                self.exp3 = self.exp3.resolve(context)
            return self.exp2 if bool(self.exp1) else self.exp3
        except template.VariableDoesNotExist:
            return self.exp3    # MODIFIED BY FITTI (original was "" and not self.exp3)

    def fix_type(self, v):
        try:
            i = int(v)
            if str(i) == v:
                v = i
            else:
                raise ValueError()
        except ValueError:
            try:
                f = float(v)
                v = f
            except ValueError:
                if v[0] == v[-1] and v[0] in ('"', "'"):
                    v = v[1:-1]
                elif v == "None":
                    v = None
                elif v in ("True", "False"):
                    v = bool(v)
                else:
                    v = template.Variable(v)

        return v

@register.tag("?:")
@register.tag("xf_iif")
@register.tag("iif")
def iif(parser, token):
    try:
        tag, exp1, exp2, exp3 = token.split_contents()
    except ValueError:
        try:
            tag, exp1, exp2 = token.split_contents()
            exp3 = None
        except ValueError:
            raise template.TemplateSyntaxError("%r tag requires two or three arguments" % token.contents.split()[0])

    return IifNode(exp1 = exp1, exp2 = exp2, exp3 = exp3)



def trans(context, text, language_code):
    request = context["request"]
    current_language = request.LANGUAGE_CODE
    return text if language_code == current_language else ""



@register.simple_tag(name='update_variable')
def update_variable(value):
    return value

def update_variable2(value):
    data = value
    return data

register.filter('update_variable2', update_variable2)

@register.simple_tag()
def alias(obj):
    """
    Alias Tag
    """
    return obj