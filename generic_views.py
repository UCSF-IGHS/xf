from django.conf import settings
from django.db.models import ProtectedError
import json as simplejson
import json
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, FormView
from django.views.generic.base import TemplateView
from django.http import Http404, HttpResponseRedirect, HttpResponse



# Addtional Views providing extra functionality
# For XFListView: Providing search functionality by adding a search_string variable to the context
# Override get_queryset to benefit from this search_string

from django.views.generic.edit import FormMixin, ModelFormMixin, ProcessFormView
from .auth.permission_mixin import *
from .auth.permission_mixin import PermissionMixin
from xf_system.views import XFNavigationViewMixin


def errors_to_json2(errors):
    """
    Convert a Form error list to JSON::
    """
    # TODO PYTHON3: CHECK THIS
    return dict(
        (k, v)
            for (k,v) in errors.iteritems()
    )

class XFAjaxViewMixin():
    """
    Enables Ajax functionality and compatibility. Wraps responses to JSON when needed.
    """

    success_message = "Operation completed"
    ajax_template_name = "ajax_form.html"

    def __init__(self):
        self.template_name = self.ajax_template_name
        self.message = ""
        self.data = None
        self.success = None
        self.resp = None
        pass;

    def get(self, request, **kwargs):
        """
        Ensures that a view that is requested via AJAX is wrapped in a stripped template, so that only its body
        is being rendered, rather than full site.
        """

        #If AJAX - use a special form

        if request.GET.get('ajax') is not None:
            self.template_name = self.ajax_template_name

    def post(self, request, *args, **kwargs):
        """
        Ensures that a view that is posted via AJAX is wrapped in a stripped template, so that only its body
        is being rendered, rather than full site.
        """

        if request.GET.get('ajax') is not None:
            self.template_name = self.ajax_template_name

    def set_list_template(self, context, request):
        """
        Sets the

        OLD: Sets the form when using a list. A list requires a different approach - it is either
        fully embedded within a template, or just plain.
        """
        if request.GET.get('ajax') is not None:
            context['extends'] = 'ajax_list.html'
            context['ajax'] = '&ajax'
        else:
            context['extends'] = 'listview_generic.html'
            context['ajax'] = '&'

    def prepare_form_invalid(self, request, form, response):
        if not request.is_ajax() and request.GET.get('ajax56_debug') is None:
            return response

        self.message = "Validation failed."
        try:
            self.data = errors_to_json2(form.errors)
        except:
            self.data = ""
        self.success = False
        self.resp = response.rendered_content
        payload = {'success': self.success, 'message': self.message, 'data':self.data, 'html':self.resp}
        return HttpResponse(json.dumps(payload), content_type='application/json', )

    def prepare_form_valid(self, request, form, response):

        if not request.is_ajax() and request.GET.get('ajax56_debug') is None:
            return response
        else:
            self.message = self.success_message
            self.success = True
            return_value = {'success': self.success, 'message': self.message}
            #print return_value
            return HttpResponse(json.dumps(return_value), content_type='application/json', )


class XFGenericListView(ListView, XFNavigationViewMixin):

    paginate_by = 3
    generic = False

    def get_template_names(self):
        """


        :return:
        """
        if not self.generic:
            return super(XFGenericListView, self).get_template_names()
        else:
            return "listview_generic_objectlist.html"

    def get_context_data(self, **kwargs):
        self.context = context = super(XFGenericListView, self).get_context_data(**kwargs)
        context['primary_key'] = self.model._meta.pk.name

        if self.generic:

            try:
                context['fields'] = self.model._meta.list_field_list
            except:
                # First pick the fields
                context['fields'] = []
                for field in self.model._meta.fields:
                    if not field.primary_key:
                        context['fields'].append(field.name)

            # Add the columns
            context['columns'] = []
            for field in context['fields']:
                context['columns'].append(self.model._meta.get_field(field).verbose_name.title())

        try:
            context['list_title'] = self.model._meta.list_title
            context['list_hint'] = self.model._meta.list_hint
        except:
            pass

        self.set_navigation_context()
        return context

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        try:
            if not self.search_string is None:
                kwargs = {
                    '{0}__{1}'.format(self.model._meta.search_field, 'icontains'): self.search_string
                }
                queryset = self.model._default_manager.filter(**kwargs)
                return queryset
        except:
            return self.model._default_manager.all()



    def get(self, request, *args, **kwargs):

        # Get the search string from the text box, if entered - needed by the sub class
        #TODO: Fix The Search

        self.search_string = request.GET.get('search_string', '')
        #self.search_string = ""
        self.request = request
        return super(XFGenericListView, self).get(request, *args, **kwargs)


class XFListView(XFGenericListView, PermissionMixin, XFAjaxViewMixin):
    """
    A list view that requires authentication.
    """

    def get(self, request, *args, **kwargs):

        # If no user is logged in - redirect to login page
        if not request.user.is_authenticated():
            return HttpResponseRedirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        return super(XFListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.context = context = super(XFListView, self).get_context_data(**kwargs)
        context['search_string'] = self.search_string
        context['action'] = "List"
        self.ensure_group_or_403("Data Browser")
        self.set_context_perm("add")
        self.set_context_perm("change")
        self.set_context_perm("delete")
        context['browse'] = True
        # Set to AJAX list if necessary
        self.set_list_template(context, self.request)
        return context



class XFUnsafeListView(XFGenericListView):
    """
    A list view used for non-authenticated items. This list view does not restrict any access.
    """


    def get_context_data(self, **kwargs):
        self.context = context = super(XFUnsafeListView, self).get_context_data(**kwargs)
        context['search_string'] = self.search_string
        context['action'] = "List"
        return context

    #def render_to_response(self, context, **response_kwargs):
    #    return super(XFUnsafeListView, self).render_to_response(context, **response_kwargs)

class XFDetailView(DetailView, ModelFormMixin, PermissionMixin, XFAjaxViewMixin):
    template_name = "form_details_generic.html"

    def get_context_data(self, **kwargs):
        self.context = context = super(XFDetailView, self).get_context_data(**kwargs)
        context['action'] = "Detail"
        self.form_class = self.get_form_class()
        context['form'] = self.get_form(self.form_class)
        #Used because there is no VIEW permission (yet)
        self.ensure_group_or_403("Data Browser")
        context['browse'] = True

        return context

    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return DetailView.get(self, request, **kwargs)

class XFUnsafeDetailView(DetailView, ModelFormMixin, XFAjaxViewMixin):
    template_name = "form_details_generic.html"

    def get_context_data(self, **kwargs):
        self.context = context = super(XFUnsafeDetailView, self).get_context_data(**kwargs)
        context['action'] = "Detail"
        self.form_class = self.get_form_class()
        context['form'] = self.get_form(self.form_class)
        #Used because there is no VIEW permission (yet)
        context['browse'] = True

        return context

    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return DetailView.get(self, request, **kwargs)

class XFUpdateView(UpdateView, PermissionMixin, XFAjaxViewMixin):
    template_name = "form_generic.html"

    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return UpdateView.get(self, request, **kwargs)

    def post(self, request, **kwargs):
        XFAjaxViewMixin.post(self, request, **kwargs)
        self.request = request
        return UpdateView.post(self, request, **kwargs)

    def get_context_data(self, **kwargs):
        self.context = context = super(XFUpdateView, self).get_context_data(**kwargs)
        context['action'] = "Update"
        self.ensure_set_context_perm("change")
        return context

    def form_invalid(self, form):
        return XFAjaxViewMixin.prepare_form_invalid(self, self.request, form,
                                                    UpdateView.form_invalid(self, form))

    def form_valid(self, form):
        return XFAjaxViewMixin.prepare_form_valid(self, self.request, form,
                                                  UpdateView.form_valid(self, form))


class XFDeleteView(DeleteView, PermissionMixin, XFAjaxViewMixin):
    template_name = "form_delete_generic.html"
    ajax_template_name = "ajax_form_confirm_delete.html"
    protected_error = False

    def get_context_data(self, **kwargs):
        self.context = context = super(XFDeleteView, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        context['protected_error'] = self.protected_error
        self.ensure_set_context_perm("delete")
        return context


    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return DeleteView.get(self, request, **kwargs)

    def post(self, request, **kwargs):
        XFAjaxViewMixin.post(self, request, **kwargs)
        self.request = request
        try:
            return XFAjaxViewMixin.prepare_form_valid(self, self.request, None,
                                                      DeleteView.post(self, request, **kwargs))
        except ProtectedError:
            self.protected_error = True
            return XFAjaxViewMixin.prepare_form_invalid(self, self.request, None,
                                                        XFDeleteView.get(self, request, **kwargs))



class XFCreateView(CreateView, PermissionMixin, XFAjaxViewMixin):
    template_name = "form_generic.html"

    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return CreateView.get(self, request, **kwargs)

    def post(self, request, **kwargs):
        XFAjaxViewMixin.post(self, request, **kwargs)
        return CreateView.post(self, request, **kwargs)

    def form_invalid(self, form):
        return XFAjaxViewMixin.prepare_form_invalid(self, self.request, form,
                                                    CreateView.form_invalid(self, form))

    def form_valid(self, form):
        return XFAjaxViewMixin.prepare_form_valid(self, self.request, form,
                                                  CreateView.form_valid(self, form))

    def get_context_data(self, **kwargs):
        self.context = context = super(XFCreateView, self).get_context_data(**kwargs)
        context['action'] = "Create"
        print(self.get_form_class().Meta.model.__name__.lower())
        self.ensure_set_context_perm("add")
        return context


class XFContextFormView(FormView):
    """
    TO DO: WRITE DOCUMENTATION FOR WHAT THIS DOES
    """
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return HttpResponseRedirect(self.get_success_url())

    def prepare_response(self):
        """
        Returns either a normal response, or an AJAX response. Packs a dictionary and an HTML response
        together.
        """
        pass

