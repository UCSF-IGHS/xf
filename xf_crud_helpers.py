from crispy_forms.helper import FormHelper
from django.forms import ALL_FIELDS

from xf_crud.generic_forms import XFModelForm
from . import generic_forms

__author__ = 'Fitti'
from django.conf.urls import include, url
from .generic_views import XFCreateView, XFDetailView, XFDeleteView, XFListView, XFUpdateView

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

def crudurl(appname, modelname, model, form_class):

    """
    Generates a set of CRUL URLs for the given model.
    :param appname: the app for which to generate the URL
    :param modelname: the modelname for which to generate the URL
    :param model: the actual model for which to generate the URL
    :param form_class: the form class to use for the URL. May be NULL, in which case it will be generated automatically.
    :return: a set of patterns.
"""

    if form_class is None:
        try:
            form_class = mmodelform_factory(model, fields=model._meta.form_field_list)
        except:
            form_class = mmodelform_factory(model)

        form_class.Meta.title = modelname.capitalize()

    return [
        url(r'^%s/%s/new' % (appname, modelname), XFCreateView.as_view(model=model, form_class=form_class, success_url="%s/%s/" % (appname, modelname))),
        url(r'^%s/%s/(?P<pk>(\d))/edit' % (appname, modelname), XFUpdateView.as_view(model=model, form_class=form_class, success_url="%s/%s/" % (appname, modelname))),
        url(r'^%s/%s/(?P<pk>(\d))/delete' % (appname, modelname), XFDeleteView.as_view(model=model, success_url="%s/%s/" % (appname, modelname))),
        url(r'^%s/%s/' % (appname, modelname), XFListView.as_view(model=model, generic=True, queryset=model.objects.order_by("name"))),
    ]

#    return patterns('',
#                    (r'^%s/%s/new' % (appname, modelname) , XFCreateView.as_view(model=model, form_class=form_class, success_url="%s/%s/" % (appname, modelname))),
#                    (r'^%s/%s/(?P<pk>(\d))/edit' % (appname, modelname) , XFUpdateView.as_view(model=model, form_class=form_class, success_url="%s/%s/" % (appname, modelname))),
#                    (r'^%s/%s/(?P<pk>(\d))/delete' % (appname, modelname) , XFDeleteView.as_view(model=model, success_url="%s/%s/" % (appname, modelname))),
#                    (r'^%s/%s/' % (appname, modelname) , XFListView.as_view(model=model, generic=True, queryset= model.objects.order_by("name"))),

#                    )


