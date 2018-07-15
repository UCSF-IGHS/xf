# import MySQLdb
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

import xf.uc_dashboards.models.perspective
import xf.uc_dashboards.models.template
from xf.uc_dashboards.models.perspective import Perspective
from xf.uc_dashboards.models.xf_viz_site_settings import XFVizSiteSettings
from xf.xf_crud.permission_mixin import XFPermissionMixin
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
from xf.xf_system.models import XFSiteSettings
from xf.xf_system.views import XFNavigationViewMixin
from xf.xf_system.xf_navigation import add_navigation


# Create your views here.


def get_current_perspective(request):
    """
    Returns the currently active perspective, if any. Otherwise it returns None
    :param request:
    :return:
    """

    # If a perspective is set in the session, return that
    # if request.session.has_key("perspective_id"):
    # PYTHON3 UPDATE
    if "perspective_id" in request.session:
        perspective = Perspective.objects.get(pk=request.session["perspective_id"])
        return perspective

    # No perspective set. Try to get the default perspective from the user
    # Load all perspectives available to this user
    if request.user.is_authenticated():
        request.user.load_perspectives()
        perspectives = request.user.perspectives
        user = request.user

        if hasattr(user, "profile"):
            if hasattr(user.profile, "default_perspective") and user.profile.default_perspective is not None:
                return user.profile.default_perspective
        else:
            settings = XFSiteSettings.objects.first()
            if settings:
                xf_viz_settings = XFVizSiteSettings.objects.filter(settings=settings).first()
                if xf_viz_settings:
                    return xf_viz_settings.anonymous_perspective
    return None


def load_navigation(sender, navigation_trees, request):
    preset_filters = ""
    perspective = None
    perspectives = None
    pages = None
    navigation_sections = {}

    # Load the current perspective

    # We are building a nivigation structure here
    # Tuple: (NavigationItem, [Page])
    # Dictionary: {NavivationItemID, (Tuple)}
    # Dictionary: {ParentNavigationItemID, Dictionary}

    # Create a navigation tree for dashboards


    # if not navigation_trees.has_key("dashboard"):
    # PYTHON3 UPDATE
    if not "dashboard" in navigation_trees:
        navigation_tree = []
        navigation_trees["dashboard"] = navigation_tree

        current_perspective = get_current_perspective(request)
        if current_perspective:

            print("******* Calling load_navigation with pperspective")

            pages = current_perspective.pages \
                .select_related('section', 'navigation_section', 'parent_page', 'template', 'page_type') \
                .order_by('navigation_section__index', 'index')

            for page in pages:
                print("Processing: %s: " % page.title)

                if page.page_id:

                    url = reverse(viewname=page.page_type.url_section,
                                  kwargs={'section': page.section.title,
                                          'perspective_slug': current_perspective.slug,
                                          'slug': page.slug,
                                          'page_id': page.page_id
                                          })
                else:
                    url = reverse(viewname=page.page_type.url_section,
                                  kwargs={'section': page.section.title,
                                          'perspective_slug': current_perspective.slug,
                                          'slug': page.slug
                                          })

                # Check if user is part of one of the allowed groups to view this page, before adding menu item
                # to navigation
                if is_user_allowed_to_page(request.user, page):
                    if page.parent_page:
                        add_navigation(navigation_tree, 'Dashboard', page.parent_page.navigation_section.caption, url,
                                       page.parent_page.navigation_section.icon, page.title, page.parent_page.title)

                    elif page.navigation_section:
                        add_navigation(navigation_tree, 'Dashboard', page.navigation_section.caption, url,
                                       page.navigation_section.icon, page.title)

    return


def is_user_allowed_to_page(user, page):
    return XFPermissionMixin.user_in_group(user, page.permissions_to_view.all()) \
           or (not user.is_authenticated and page.allow_anonymous)

# This statement adds a callback function to the XFNavigationMixin - when the navigation menus need to be loaded,
# this callback will be called.
XFNavigationViewMixin.navigation_tree_observers.append(load_navigation)


# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==


# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==


########################################################################################################################


# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==

# Don't like these non-class based views, but they work, for now
def load_perspective(request, perspective_id):
    perspective = get_object_or_404(xf.uc_dashboards.models.perspective.Perspective, id=perspective_id)
    perspective = request.user.load_perspective(perspective, True)
    if perspective:
        request.session["perspective_id"] = perspective.id
    return home_page(request)
    pass


def load_perspective(request, slug):
    perspective = get_object_or_404(xf.uc_dashboards.models.perspective.Perspective, slug=slug)
    perspective = request.user.load_perspective(perspective, True)
    if perspective:
        request.session["perspective_id"] = perspective.id
    return home_page(request)
    pass


def clear_perspective(request):
    request.session["perspective_id"] = None
    return HttpResponse("Cleared")


def home_page(request):
    '''
    Serves the appropriate home page
    :param request:
    :return:
    '''

    # If there is a perspective, try to load that perspective's home page
    # if request.session.has_key("perspective_id"):
    # PYTHON3 UPDATE
    if "perspective_id" in request.session:
        perspective = Perspective.objects.get(pk=request.session["perspective_id"])
        url = reverse("dashboards",
                      args=[perspective.default_page.section.title, perspective.slug, perspective.default_page.slug])
        # perspective.default_page
        return HttpResponseRedirect(url)

    # No perspecive - load default homepage
    return HttpResponseRedirect(settings.HOME_PAGE)
    # return HttpResponseRedirect("/")
