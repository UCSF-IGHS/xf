from abc import abstractmethod

from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import ModelFormMixin

from xf.xf_crud.ajax_mixins import XFAjaxViewMixin
from xf.xf_crud.mixins import XFCrudMixin

from xf.xf_crud.permission_mixin import XFPermissionMixin
from xf.xf_system.views import XFNavigationViewMixin


class XFDetailView(DetailView, ModelFormMixin, XFPermissionMixin, XFAjaxViewMixin, XFNavigationViewMixin, XFCrudMixin):
    template_name = "form_generic.html"

    def get_context_data(self, **kwargs):
        self.context = context = super(XFDetailView, self).get_context_data(**kwargs)

        if not self.user_has_model_permission("view"):
            raise PermissionDenied

        context['action'] = "Detail"
        context['formname'] = self.get_form_class().__name__

        self.prepare_form_class()
        self.form.make_readonly()
        context['form'] = self.form
        context['browse'] = True

        self.set_navigation_context()
        self.add_crud_urls_to_context(context)
        self.form.add_assets_to_context(context)
        return context

    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return DetailView.get(self, request, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs



class XFMasterChildView(XFDetailView):
    template_name = "form_master_child.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.related_tabs = []
        self.action_list = []
        self.action_buttons = []

    def add_related_listview(self, related_list_view):
        self.related_tabs.append(related_list_view)

    def add_action_button(self, action):
        self.action_buttons.append(action)

    def add_action_list_item(self, action):
        self.action_list.append(action)

    def get_context_data(self, **kwargs):
        context = super(XFMasterChildView, self).get_context_data(**kwargs)
        #context['list_url'] = reverse('library_book-instances_list_related', kwargs={'related_fk':self.kwargs['pk']})

        self.add_actions()
        context['related_tabs'] = self.related_tabs
        context['action_buttons'] = self.action_buttons
        context['action_list'] = self.action_list
        context['primary_key'] = self.model._meta.pk.name
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    @abstractmethod
    def add_actions(self):
        pass


class XFUnsafeDetailView(DetailView, ModelFormMixin, XFAjaxViewMixin, XFCrudMixin):
    template_name = "form_details_generic.html"

    def get_context_data(self, **kwargs):
        self.context = context = super(XFUnsafeDetailView, self).get_context_data(**kwargs)
        context['action'] = "Detail"
        self.form_class = self.get_form_class()
        context['form'] = self.get_form(self.form_class)
        #Used because there is no VIEW permission (yet)
        context['browse'] = True
        self.add_crud_urls_to_context(context)
        return context

    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return DetailView.get(self, request, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs



class XFUpdateView(UpdateView, XFPermissionMixin, XFAjaxViewMixin, XFCrudMixin):
    template_name = "form_generic.html"


    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return UpdateView.get(self, request, **kwargs)

    def post(self, request, **kwargs):

        if not self.user_has_model_permission("change"):
            raise PermissionDenied

        self.success_message = "%s has been updated" % (self.get_object())
        XFAjaxViewMixin.post(self, request, **kwargs)
        self.request = request
        return UpdateView.post(self, request, **kwargs)

    def get_context_data(self, **kwargs):
        self.context = context = super(XFUpdateView, self).get_context_data(**kwargs)
        context['action'] = "Update"
        context['formname'] = self.get_form_class().__name__
        self.prepare_form_class()
        self.ensure_set_context_perm("change")
        self.add_crud_urls_to_context(context)
        return context

    def form_invalid(self, form):
        return XFAjaxViewMixin.prepare_form_invalid(self, self.request, form,
                                                    UpdateView.form_invalid(self, form))

    def form_valid(self, form):
        form.prepare_form_for_save(form.instance)
        if hasattr(form.instance, "prepare_for_save"):
            form.instance.prepare_for_save(self.request, self.request.user if self.request.user else None)

        form_valid_output = UpdateView.form_valid(self, form)
        self.success_message = "%s has been updated" % (self.object)

        return XFAjaxViewMixin.prepare_form_valid(self, self.request, form, form_valid_output)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs



class XFDeleteView(DeleteView, XFPermissionMixin, XFAjaxViewMixin, XFCrudMixin):
    template_name = "form_delete_generic.html"
    ajax_template_name = "ajax_form_confirm_delete.html"
    protected_error = False

    def get_context_data(self, **kwargs):
        self.context = context = super(XFDeleteView, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        context['formname'] = "DeleteForm"
        context['protected_error'] = self.protected_error
        self.ensure_set_context_perm("delete")
        self.add_crud_urls_to_context(context)
        return context


    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return DeleteView.get(self, request, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, **kwargs):

        if not self.user_has_model_permission("delete"):
            raise PermissionDenied

        self.success_message = "%s has been deleted" % (self.get_object())
        XFAjaxViewMixin.post(self, request, **kwargs)
        self.request = request
        try:
            return XFAjaxViewMixin.prepare_form_valid(self, self.request, None,
                                                      DeleteView.post(self, request, **kwargs))
        except ProtectedError:
            self.protected_error = True
            return XFAjaxViewMixin.prepare_form_invalid(self, self.request, None,
                                                        XFDeleteView.get(self, request, **kwargs))


class XFCreateView(CreateView, XFPermissionMixin, XFAjaxViewMixin, XFNavigationViewMixin, XFCrudMixin):
    template_name = "form_generic.html"



    def get(self, request, **kwargs):
        XFAjaxViewMixin.get(self, request, **kwargs)
        return CreateView.get(self, request, **kwargs)

    def post(self, request, **kwargs):

        if not self.user_has_model_permission("add"):
            raise PermissionDenied

        XFAjaxViewMixin.post(self, request, **kwargs)
        return CreateView.post(self, request, **kwargs)

    def form_invalid(self, form):
        return XFAjaxViewMixin.prepare_form_invalid(self, self.request, form,
                                                    CreateView.form_invalid(self, form))

    def form_valid(self, form):
        form.prepare_form_for_save(form.instance)
        if hasattr(form.instance, "prepare_for_save"):
            form.instance.prepare_for_save(self.request, self.request.user if self.request.user else None)
        form_valid_output = CreateView.form_valid(self, form)
        self.success_message = "%s has been created" % (self.object)
        return XFAjaxViewMixin.prepare_form_valid(self, self.request, form,
                                                  form_valid_output)

    def get_initial(self):
        return self.get_initial_form_data_from_querystring()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        self.context = context = super(XFCreateView, self).get_context_data(**kwargs)
        context['action'] = "Create"
        context['formname'] = self.get_form_class().__name__

        self.prepare_form_class()
        self.ensure_set_context_perm("add")
        self.set_navigation_context()
        self.add_crud_urls_to_context(context)

        return context