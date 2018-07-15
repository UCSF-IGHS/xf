import ast

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

import xf.uc_dashboards
from xf.uc_dashboards.models import NavigationSection
from xf.uc_dashboards.models.xf_viz_site_settings import XFVizSiteSettings
from xf.xf_system.views import XFNavigationViewMixin


class DashboardView(TemplateView, XFNavigationViewMixin):
    """
    The base view for a dashboard. This view ensures that navigation sections are
    properly rendered within the context.

    It also loads all the perspectives.
    """

    template_name = "dashboards/t_dashboard_overview.html"

    def __init__(self):
        super(DashboardView, self).__init__()
        XFNavigationViewMixin.__init__(self)

        print("delegate set")

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        self.load_perspectives()
        context["perspectives"] = self.perspectives

        if self.perspective:
            context["current_perspective"] = self.perspective
            context["navigation_sections"] = self.navigation_sections

        else:
            # No perspective - load legacy menus
            navigationsections = NavigationSection.objects.order_by("index")
            context["legacy_navigation"] = True
            context["navigationsections"] = navigationsections

        self.context = context
        self.set_navigation_context()
        return context

    def load_perspectives(self):

        self.preset_filters = ""
        self.perspective = None
        self.perspectives = None
        self.anonymous_perspective = None
        self.pages = None
        self.navigation_sections = {}
        print("load perspectives")
        print(self.kwargs)

        # Add the anonymous perspective, if it is defined

        if XFNavigationViewMixin.site_settings:
            xf_viz_settings = XFVizSiteSettings.objects.filter(settings=XFNavigationViewMixin.site_settings).first()
            if xf_viz_settings:
                self.anonymous_perspective = xf_viz_settings.anonymous_perspective
                if not self.request.user.is_authenticated():
                    self.perspective = self.anonymous_perspective

        # Load the current perspective

        # We are building a nivigation structure here
        # Tuple: (NavigationItem, [Page])
        # Dictionary: {NavivationItemID, (Tuple)}
        # Dictionary: {ParentNavigationItemID, Dictionary}

        # if self.request.session.has_key("perspective_id"):
        # PYTHON3 UPDATE

        if "perspective_slug" in self.kwargs:
            perspective = get_object_or_404(xf.uc_dashboards.models.perspective.Perspective,
                                            slug=self.kwargs["perspective_slug"])
            perspective = self.request.user.load_perspective(perspective, True)
            if perspective:
                self.perspective = perspective
                self.request.session["perspective_id"] = self.perspective.id

        elif "perspective_id" in self.request.session:
            self.perspective = xf.uc_dashboards.models.perspective.Perspective.objects.get(pk=self.request.session["perspective_id"])

        if self.perspective:
            self.pages = self.perspective.pages.all()

            for page in self.pages:
                navigation_section = None
                # if not self.navigation_sections.has_key(page.navigation_section_id):
                # PYTHON3 UPDATE

                if not page.navigation_section.id in self.navigation_sections:
                    self.navigation_sections[page.navigation_section_id] = (page.navigation_section, [page])
                else:
                    self.navigation_sections[page.navigation_section_id][1].append(page)

            # Don't allow loading a page outside the current perspective

            if not self.page.allow_anonymous:
                found = False
                for page in self.pages:
                    if self.page.id == page.id:
                        found = True
                        break

                if not found:
                    raise Http404("This page does not exist in this perspective")

        # Load all perspectives available to this user
        if self.request.user.is_authenticated():
            self.request.user.load_perspectives()
            self.perspectives = self.request.user.perspectives

            if not self.perspectives:
                raise PermissionDenied("User doesn't have any associated perspectives")

            # Set preset filters for groups
            for group in self.request.user.groups.all():
                if group.profile:
                    if group.profile.preset_filters:
                        filters = ast.literal_eval('{' + group.profile.preset_filters + '}')
                        if self.perspective:
                            # if filters.has_key("*"):
                            # PYTHON3 UPDATE
                            if "*" in filters:
                                self.preset_filters = filters["*"]
                            # if filters.has_key(self.perspective.code):
                            # PYTHON3 UPDATE
                            if self.perspective.code in filters:
                                self.preset_filters = filters[self.perspective.code]

            # Set preset filters for users - this means that user filters superseed group filters
            if self.request.user.profile:
                if self.request.user.profile.preset_filters:
                    # load all the filters as a dictionary and load the filter for the particular perspective
                    # a * may be used for all perspectives - and this can be overridden by a more specific filter
                    filters = ast.literal_eval('{' + self.request.user.profile.preset_filters + '}')
                    if self.perspective:
                        # if filters.has_key("*"):
                        # PYTHON3 UPDATE
                        if "*" in filters:
                            self.preset_filters = filters["*"]
                        # if filters.has_key(self.perspective.code):
                        # PYTHON3 UPDATE
                        if self.perspective.code in filters:
                            self.preset_filters = filters[self.perspective.code]

        elif self.anonymous_perspective is not None:
            self.request.user.load_perspectives()
        pass
