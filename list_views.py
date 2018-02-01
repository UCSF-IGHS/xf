from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView

from xf_crud.ajax_mixins import XFAjaxViewMixin
from xf_crud.generic_lists import XFModelList
from xf_crud.permission_mixin import XFPermissionMixin
from xf_system.views import XFNavigationViewMixin




class XFGenericListView(ListView, XFNavigationViewMixin):

    paginate_by = 10
    generic = False
    list_class = None

    def __init__(self, *args, **kwargs):
        super(XFGenericListView, self).__init__(**kwargs)

        if kwargs['list_class'] is not None:
            self.list_class = kwargs['list_class'](kwargs['model'])
        else:
            self.list_class = XFModelList(kwargs['model'])


    def get_template_names(self):

        if not self.generic:
            return super(XFGenericListView, self).get_template_names()
        else:
            return "listview_generic_objectlist.html"

    def get_context_data(self, **kwargs):
        self.context = context = super(XFGenericListView, self).get_context_data(**kwargs)
        context['primary_key'] = self.model._meta.pk.name

        if self.generic:

            context['fields'] = self.list_class.list_field_list

            # Add the columns
            context['columns'] = []
            for field in context['fields']:
                context['columns'].append(self.model._meta.get_field(field).verbose_name.title())

            # Add pre-set filters, if any
            try:
                # Correct way of doing this – don't use hasattr
                # https://hynek.me/articles/hasattr/
                context['preset_filter_list'] = self.list_class.preset_filters
                context['preset_filter'] = self.kwargs['preset_filter'] if 'preset_filter' in self.kwargs else ""
            except:
                pass

            context['list_title'] = self.list_class.list_title
            context['list_hint'] = self.list_class.list_hint
            context['search_hint'] = self.list_class.search_hint

        context['current_url'] = self.request.get_full_path()
        if not context['current_url'].endswith("/"):
            context['current_url'] += '/'

        self.set_navigation_context()
        return context


    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """

        if self.list_class:
            return self.list_class.get_queryset(self.search_string, self.model,
                                                self.kwargs['preset_filter'] if 'preset_filter' in self.kwargs else None)
        else:
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


class XFListView(XFGenericListView, XFPermissionMixin, XFAjaxViewMixin):
    """
    A list view that requires authentication.
    """

    def __init__(self, *args, **kwargs):
        super(XFListView, self).__init__(*args, **kwargs)


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
        self.list_class.add_assets_to_context(context)
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

