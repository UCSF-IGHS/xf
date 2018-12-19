from crispy_forms.helper import FormHelper
from django.forms import ALL_FIELDS

from xf.xf_crud.model_forms import XFModelForm
from xf.xf_crud.generic_list_views import XFListView
from xf.xf_crud.model_lists import XFModelList
from xf.xf_system.utilities.deprecated_decorator import xf_deprecated
from . import model_forms

__author__ = 'Fitti'
from django.conf.urls import include, url
from xf.xf_crud.generic_crud_views import XFDetailView, XFUpdateView, XFDeleteView, XFCreateView

# Providing ability to inject custom delete view (soft delete support), may be removed when
# class based implementation is done - WaH -- 2018-12-19
_delete_view = XFDeleteView

def mmodelform_factory(model, form=XFModelForm, fields=None, exclude=None,
                       formfield_callback=None, widgets=None):
    """
    Returns a ModelForm containing form fields for the given model.

    ``fields`` is an optional list of field names. If provided, only the named
    fields will be included in the returned fields.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned fields, even if they are listed
    in the ``fields`` argument.

    ``widgets`` is a dictionary of model field names mapped to a widget.

    ``formfield_callback`` is a callable that takes a model field and returns
    a form field.
    """
    # Create the inner Meta class. FIXME: ideally, we should be able to
    # construct a ModelForm without creating and passing in a temporary
    # inner class.

    # Build up a list of attributes that the Meta object will have.
    attrs = {'model': model}
    if fields is not None:
        attrs['fields'] = fields
    else:
        attrs['fields'] = ALL_FIELDS
    if exclude is not None:
        attrs['exclude'] = exclude
    if widgets is not None:
        attrs['widgets'] = widgets

    # If parent form class already has an inner Meta, the Meta we're
    # creating needs to inherit from the parent's inner meta.
    parent = (object,)
    if hasattr(form, 'Meta'):
        parent = (form.Meta, object)
    Meta = type(str('Meta'), parent, attrs)

    # Give this new form class a reasonable name.
    class_name = model.__name__ + str('Form')

    # Class attributes for the new form class.
    form_class_attrs = {
        'Meta': Meta,
        'formfield_callback': formfield_callback,
    }

    # Instatiate type(form) in order to use the same metaclass as form.

    return type(form)(class_name, (form,), form_class_attrs)

#@xf_deprecated("Please use url builder instead of crudurl")
def crudurl(appname: object, modelname: object, model_type: object, form_class_type: object, list_class_type: object = XFModelList) -> object:
    """
    Generates a set of CRUL URLs for the given model.
    :param appname: the app for which to generate the URL
    :param modelname: the modelname for which to generate the URL
    :param model_type: the actual model for which to generate the URL
    :param form_class_type: the form class to use for the URL. May be NULL, in which case it will be generated automatically.
    :return: a set of patterns.
"""

    if form_class_type is None:
        try:
            form_class_type = mmodelform_factory(model_type, fields=model_type._meta.form_field_list)
        except:
            form_class_type = mmodelform_factory(model_type)

        form_class_type.Meta.title = modelname.capitalize()

    list_class = list_class_type(model_type)

    urls = []
    if 'add' in list_class.supported_crud_operations:
        urls.append(
            url(r'^%s/%s/new' % (appname, modelname), XFCreateView.as_view(model=model_type, form_class=form_class_type,
                                                                           success_url="%s/%s/" % (appname, modelname),
                                                                           app_name=appname, model_url_part=modelname),
                name="%s_%s_new" % (appname, modelname)))
        urls.append(
            url(r'^%s/%s/add_to' % (appname, modelname), XFCreateView.as_view(model=model_type, form_class=form_class_type,
                                                                           success_url="%s/%s/" % (appname, modelname),
                                                                           app_name=appname, model_url_part=modelname),
                name="%s_%s_add_to" % (appname, modelname))
        )

    if 'change' in list_class.supported_crud_operations:
        urls.append(url(r'^%s/%s/(?P<pk>[-\w]+)/edit' % (appname, modelname),
                        XFUpdateView.as_view(model=model_type, form_class=form_class_type,
                                             success_url="%s/%s/" % (appname, modelname),
                                             app_name=appname,
                                             model_url_part=modelname),
                        name="%s_%s_edit" % (appname, modelname)))

    if 'view' in list_class.supported_crud_operations:
        urls.append(url(r'^%s/%s/(?P<pk>[-\w]+)/details' % (appname, modelname),
                        XFDetailView.as_view(model=model_type, form_class=form_class_type,
                                             success_url="%s/%s/" % (appname, modelname), app_name=appname,
                                             model_url_part=modelname), name="%s_%s_details" % (appname, modelname)))

    if 'delete' in list_class.supported_crud_operations:
        urls.append(url(r'^%s/%s/(?P<pk>[-\w]+)/delete' % (appname, modelname),
                        _delete_view.as_view(model=model_type, success_url="%s/%s/" % (appname, modelname),
                                             app_name=appname,
                                             model_url_part=modelname), name="%s_%s_delete" % (appname, modelname)))

    if 'list' in list_class.supported_crud_operations:
        urls.append(url(r'^%s/%s/(?P<preset_filter>[-\w]+)' % (appname, modelname),
                        XFListView.as_view(model=model_type, generic=True, queryset=model_type.objects.order_by("name"),
                                           list_class=list_class_type, app_name=appname, model_url_part=modelname),
                        name="%s_%s_list_filter" % (appname, modelname)))
        urls.append(url(r'^%s/%s/' % (appname, modelname),
                        XFListView.as_view(model=model_type, generic=True, queryset=model_type.objects.order_by("name"),
                                           list_class=list_class_type, app_name=appname, model_url_part=modelname),
                        name="%s_%s_list" % (appname, modelname)))


    return urls
