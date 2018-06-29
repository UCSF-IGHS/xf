import ast

from django.contrib.auth.views import redirect_to_login
from django.template import TemplateDoesNotExist, Template
from django.template.loader import _engine_list
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import get_language

import xf.uc_dashboards
from xf.uc_dashboards.models import Page
from xf.uc_dashboards.views.dashboard_view import DashboardView
from xf.xf_crud.permission_mixin import XFPermissionMixin
from xf.xf_system.views import XFNavigationViewMixin


class DashboardPageView(DashboardView, XFPermissionMixin):
    """
    The base view for any dashboard type page. It checks for security as needed.
    """

    def __init__(self):
        super().__init__()
        XFNavigationViewMixin.__init__(self)

        self.page = None
        self.perspective = None

    def dispatch(self, request, *args, **kwargs):
        '''
        This method loads a page. If a perspective is provided in the URL, it will first load that perspective.
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        self.page = Page.objects.get(slug=self.kwargs['slug'])
        print(self.kwargs)

        if not self.page.allow_anonymous:
            if not self.request.user.is_authenticated():
                # return HttpResponseRedirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
                return redirect_to_login(self.request.path)
            else:
                self.ensure_groups_or_403(self.page.permissions_to_view.all())

        return super(DashboardPageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        print("B")
        context = super(DashboardPageView, self).get_context_data(**kwargs)
        page = self.page

        context['change_url'] = reverse('admin:uc_dashboards_page_change', args=(page.id,), current_app='uc_dashboards')
        context['change_template_url'] = reverse('admin:uc_dashboards_template_change', args=(page.template.id,),
                                                 current_app='uc_dashboards')
        if self.perspective:
            context['change_perspective_url'] = reverse('admin:uc_dashboards_perspective_change',
                                                        args=(self.perspective.id,),
                                                        current_app='uc_dashboards')
        context['delete_url'] = reverse('admin:uc_dashboards_page_delete', args=(page.id,), current_app='uc_dashboards')
        context['page'] = page
        context['title'] = page.title
        context['filter_query_string'] = "?" + self.preset_filters + self.request.META['QUERY_STRING']
        context["locale_code"] = get_language()

        # Version 2.4: Pre-loading widgets for the template
        if self.page.widgets != "":
            widgets = ast.literal_eval("{" + self.page.widgets + "}")

            for (key) in widgets:
                context[key] = widgets[key]


        self.template_name = page.template.template_path
        return context

    def get_template2(self, template_name, using=None):
        """
        Loads and returns a template for the given name.

        Raises TemplateDoesNotExist if no such template exists.
        """
        chain = []
        engines = _engine_list(using)
        for engine in engines:
            try:
                return engine.get_template(template_name)
            except TemplateDoesNotExist as e:
                chain.append(e)

        raise TemplateDoesNotExist(template_name, chain=chain)

    def response_class(self, request, template, context, **response_kwargs):
        """
        We are override this method so that it can inject a template that is loaded with content from the database,
        if necessary. If the template is supposed to come from a template file (in the file system), nothing happens
        and we just call the super class' method.
        :param request:
        :param template:
        :param context:
        :param response_kwargs:
        :return:
        """
        if int(self.page.template.template_source) == int(xf.uc_dashboards.models.template.Template.DATABASE):
            template = Template(self.page.template.template_text)

            template2 = self.get_template2(template_name="dashboards/t_ibbs_overview.html")
            template2.template = template

            # We need to return the template here directly
            return super(DashboardPageView, self).response_class(request, template2, context, **response_kwargs)
            t = TemplateResponse(request, template)
            return t
        else:
            return super(DashboardPageView, self).response_class(request, template, context, **response_kwargs)