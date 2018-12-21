
from django.core.urlresolvers import reverse
from django import template

import json
from django.core.serializers.json import DjangoJSONEncoder

register = template.Library()


@register.filter(name='rev')
def rev(value):
    """
    This filter returns the URL from the urls.py by using reverse. It can be used
    inside a template, such as url='login'|rev
    :param value: the name of the URL to return
    :return: the URl to return
    """
    return reverse(value)


@register.filter(name='cw')
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
    elif value == 9:
        return "col-md-9 col-sm-9 col-xs-12"


    elif value == 3:
        return "col-md-3 col-sm-3 col-xs-12"
    elif value == 6:
        return "col-md-6 col-sm-6 col-xs-12"
    elif value == 8:
        return "col-md-8 col-sm-8 col-xs-12"
    elif value == 12:
        return "col-md-12 col-sm-12 col-xs-12"
    return "col-md-12 col-sm-12 col-xs-12"


@register.filter(name='lookup_in_dict')
def lookup_in_dictionary(value, arg):

    if value is None or arg is None:
        return None

    for item in value:
        if item[list(arg.keys())[0]] == list(arg.values())[0]:
            return arg

    return None

@register.filter(name='lookup')
def cut(value, arg):
    #if value.has_key(arg):
    # PYTHON3 UPDATE

    if value is None:
        return None

    if arg in value:
        return value[arg]
    else:
        return ""

@register.filter(name='lookup_list')
def cut_list(value, arg):

    if value is not None:
        return value.getlist(arg, None)
    else:
        return ""


@register.filter(name='findforkey')
def findforkey(value, arg):
    for item in value:
        if item['key'] == arg:
            my_item = item
            break
    else:
        my_item = None

    return my_item


@register.filter(name='columnnameforkey')
def column_name_for_key(columns, key):

    return findforkey(columns, key)['column_name']
    pass


@register.filter(name='jsonify')
def get_object_by_property(objects):
    return json.dumps(list(objects), cls=DjangoJSONEncoder)
