# import MySQLdb
from django.db import connections
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import Template, TemplateDoesNotExist
from django.template.backends.django import Template as Template2, DjangoTemplates
from django.template.loader import _engine_list
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.conf import settings
from django import template
import ast
from django.db.models import Q
from django.http import HttpResponse
from . import extensions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models as UCModels

# Create your views here.
from uc_dashboards.models import NavigationSection, Page, Widget, Perspective

# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
from xf_system.views import XFNavigationViewMixin
from xf_system.xf_navigation import add_navigation


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

            pages = current_perspective.pages\
                .select_related('section', 'navigation_section', 'parent_page', 'template', 'page_type')\
                .order_by('navigation_section__index', 'index')

            for page in pages:
                print("Processing: %s: " % page.title)

                if page.page_id:

                    url = reverse(viewname=page.page_type.url_section,
                                  kwargs={'section': page.section.title, 'slug': page.slug, 'page_id': page.page_id})
                else:
                    url = reverse(viewname=page.page_type.url_section,
                                  kwargs={'section': page.section.title, 'slug': page.slug})

                if page.parent_page:
                    add_navigation(navigation_tree, 'Dashboard', page.parent_page.navigation_section.caption, url,
                                   page.parent_page.navigation_section.icon, page.title, page.parent_page.title)

                elif page.navigation_section:
                    add_navigation(navigation_tree, 'Dashboard', page.navigation_section.caption, url,
                                   page.navigation_section.icon, page.title)

    return


# This statement adds a callback function to the XFNavigationMixin - when the navigation menus need to be loaded,
# this callback will be called.
XFNavigationViewMixin.navigation_tree_observers.append(load_navigation)


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
        self.pages = None
        self.navigation_sections = {}

        # Load the current perspective

        # We are building a nivigation structure here
        # Tuple: (NavigationItem, [Page])
        # Dictionary: {NavivationItemID, (Tuple)}
        # Dictionary: {ParentNavigationItemID, Dictionary}

        # if self.request.session.has_key("perspective_id"):
        # PYTHON3 UPDATE
        if "perspective_id" in self.request.session:
            self.perspective = Perspective.objects.get(pk=self.request.session["perspective_id"])
            self.pages = self.perspective.pages.all()

            for page in self.pages:
                navigation_section = None
                # if not self.navigation_sections.has_key(page.navigation_section_id):
                # PYTHON3 UPDATE
                if not page.navigation_section.id in self.navigation_sections:
                    self.navigation_sections[page.navigation_section_id] = (page.navigation_section, [page])
                else:
                    self.navigation_sections[page.navigation_section_id][1].append(page)

        # Load all perspectives available to this user
        if self.request.user.is_authenticated():
            self.request.user.load_perspectives()
            self.perspectives = self.request.user.perspectives

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

        pass


# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
class WidgetView(TemplateView):
    """
    Serves as a base class for widgets, which are content types of a dashboard.
    """

    def __init__(self):
        # Data columns that may be displayed
        super(WidgetView, self).__init__()
        self.data_columns = []
        self.widget = None

    def dispatch(self, request, *args, **kwargs):

        if 'slug' in self.kwargs:
            self.widget = get_object_or_404(Widget, slug=self.kwargs['slug'])

        if self.widget:
            # TODO: CRASH Gracefully
            if not self.widget.allow_anonymous:
                if not self.request.user.is_authenticated():
                    # return HttpResponseRedirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
                    return redirect_to_login(self.request.path)

            self.template_name = self.widget.template.template_path
        return super(WidgetView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Loading templates and all kinds of data here
        :param kwargs:
        :return:
        """
        context = super(WidgetView, self).get_context_data(**kwargs)
        if 'zoom' in self.request.GET:
            context["extends_template"] = "dashboards/t_dashboard_widget_zoom.html"
            context["disable_zoom"] = True
        elif self.request.is_ajax():
            context["extends_template"] = "dashboards/t_dashboard_widget_ajax_container.html"
        else:
            context["extends_template"] = "dashboards/t_dashboard_widget_container_tester.html"

        context["widget_id"] = self.__class__.__name__
        if self.widget:
            context['change_url'] = reverse('admin:uc_dashboards_widget_change', args=(self.widget.id,),
                                            current_app='uc_dashboards')

        context["widget"] = self.widget
        context['filter_query_string'] = "?" + self.request.META['QUERY_STRING']
        self.load_widget_data(context)

        return context

    def result_set_to_dict(self, result_set, qkeys):
        """
        This function helps to create a dictionar object out of a SQL query
        :param result_set:
        :param qkeys:
        :return:
        """

        # build dict for template:
        fdicts = []
        for row in result_set:
            i = 0
            cur_row = {}
            for key in qkeys:
                cur_row[key] = row[i]
                i = i + 1
            fdicts.append(cur_row)
        return fdicts

    def result_set_to_transposed_dict(self, result_set, columns, label_column):
        """
        Transposes a recordset for use in bar charts
        :param result_set:
        :param columns:
        :param label_column:
        :return:
        """

        result = []
        for row in result_set:
            pass
        pass

    def get_connection(self, database_key):
        """
        Returns a connection object for PTBi
        :return: The connection object
        """

        # ptbi_data

        conn = connections[database_key]
        return conn

    def load_widget_data(self, context):
        """
        Loads the data for the widget. Some widget fields must be set as follows:

        The column_names field is used to extract data from the SQL result set and convert it into a dictionary.
        Each column name will become a field. There may be additional information in column names.


        :param context:
        :return:
        """

        if self.widget:

            if "perspective_id" in self.request.session:
                self.perspective = Perspective.objects.get(pk=self.request.session["perspective_id"])

            if self.widget.widget_type == Widget.TEXT_BLOCK:
                return

            params = []
            sql_query = self.widget.sql_query
            conn = self.get_connection(self.widget.database_key)

            if self.widget.filters:
                filters = ast.literal_eval(self.widget.filters)
                for filter in filters:
                    params.append(self.request.GET.get(filter, ''))
                    try:
                        sql_query = sql_query.replace("@" + filter, conn.literal(self.request.GET.get(filter, '')))
                    except:
                        # UNSAFE!!!!
                        # TODO: FIX
                        sql_query = sql_query.replace("@" + filter, "'" + self.request.GET.get(filter, '') + "'")

            # Add a perspective code as a filter, which allows you to filter any widget based on the current perspective
            # Very useful if you want to filter a filter based on a perspective
            if self.perspective:
                sql_query = sql_query.replace("@perspective_code", self.perspective.code)

            # print sql_query

            context["widget_id"] += self.widget.slug.replace("-", "_")
            context["caption"] = self.widget.title
            context["extra_text"] = self.widget.sub_text
            context["widget_type"] = self.widget.widget_type
            if self.perspective:
                context["perspective_code"] = self.perspective.code

            # Custom attributes
            if self.widget.custom_attributes != "":
                custom_attributes = ast.literal_eval("{" + self.widget.custom_attributes + "}")
                context["custom_attr"] = custom_attributes
                if "stripped_base" in custom_attributes and custom_attributes.get("stripped_base") == "yes":
                    context["extends_base_template"] = "t_xpanel_stripped_control_base.html"
                else:
                    context["extends_base_template"] = "t_xpanel_control_base.html"
            else:
                context["extends_base_template"] = "t_xpanel_control_base.html"

            try:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                rows = cursor.fetchall()
            finally:
                # conn.close()
                pass

            if self.widget.widget_type == Widget.PIE or \
                            self.widget.widget_type == Widget.TABLE or \
                            self.widget.widget_type == Widget.MAP or \
                            self.widget.widget_type == Widget.FILTER_DROP_DOWN or \
                            self.widget.widget_type == Widget.TILES or \
                            self.widget.widget_type == Widget.LINE_GRAPH or \
                            self.widget.widget_type == Widget.PROGRESS_CIRCLE or \
                            self.widget.widget_type == Widget.BAR_GRAPH or \
                            self.widget.widget_type == Widget.GAUGE or \
                            self.widget.widget_type == Widget.BAR_GRAPH_HORIZONTAL:

                column_names = []
                for line in self.widget.data_columns.split('\n'):
                    # Add entire column line to data_columns array, which is passed to template
                    data_column = ast.literal_eval('{' + line + '}')
                    self.data_columns.append(data_column)
                    column_names.append(data_column['column_name'])

                # Convert the result set from the SQL query into a dictionary
                rows = self.result_set_to_dict(rows, column_names)
                context["rows"] = rows;
                context["data_columns"] = self.data_columns
                context["tile_width"] = int(12 / len(rows))

            # Data points
            if self.widget.widget_type == Widget.PIE or \
                            self.widget.widget_type == Widget.LINE_GRAPH or \
                            self.widget.widget_type == Widget.BAR_GRAPH_HORIZONTAL or \
                            self.widget.widget_type == Widget.BAR_GRAPH:
                labels = []
                for row in rows:
                    labels.append(str(row[self.widget.label_column]))
                    # if isinstance(row[self.widget.label_column], str):
                    # UNICODE MAY FAIL HERE - without the str a 'u' will be added
                    #    labels.append(str(row[self.widget.label_column]))
                    # else:
                    #    labels.append("XXX")

                context["labels"] = str(labels).replace("'", '"')

                # Data points is what will actually hold the data. For a pie, this will be an array.
                # For a line or bar chart, it will be several arrays. Therefore, everything will be
                # wrapped into an array of arrays - with only one element for pie
                datapoints = []
                legend_labels = []
                for column in self.widget.data_point_column.split('\n'):

                    # create a dictionary like {'legend_label': 'number of admissions', 'column_name': 'admissions'}
                    data_point_column_description = ast.literal_eval('{' + column + '}')
                    # if data_point_column_description.has_key('legend_label'):
                    # PYTHON3 UPDATE
                    if "legend_label" in data_point_column_description:
                        legend_labels.append(data_point_column_description['legend_label'])
                    # single row with data points, for a line chart with 2 lines will have two of them
                    datapoint_row = []
                    for row in rows:
                        datapoint_row.append(str(row[data_point_column_description['column_name']]))

                    datapoints.append(str(datapoint_row).replace("'", ''))
                context["datapoints"] = datapoints
                context["legend_labels"] = legend_labels

            # This variable determines whether the "view data" command is available in the widget. Only
            # available for widgets that support it.
            context["supports_view_data"] = True if \
                self.widget.widget_type == Widget.LINE_GRAPH or \
                self.widget.widget_type == Widget.BAR_GRAPH or \
                self.widget.widget_type == Widget.BAR_GRAPH_HORIZONTAL or \
                self.widget.widget_type == Widget.GAUGE or \
                self.widget.widget_type == Widget.PIE \
                else False

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
        We are overloading this method so that it can inject a template that is loaded with content from the database,
        if necessary. If the template is supposed to come from a template file (in the file system), nothing happens
        and we just call the super class' method.
        :param request:
        :param template:
        :param context:
        :param response_kwargs:
        :return:
        """
        if self.widget:
            if int(self.widget.template.template_source) == int(UCModels.Template.DATABASE):
                template = Template(self.widget.template.template_text)
                template2 = self.get_template2(template_name="dashboards/t_ibbs_overview.html")
                template2.template = template

                # We need to return the template here directly
                return super(WidgetView, self).response_class(request, template2, context, **response_kwargs)
                t = TemplateResponse(request, template)
                return t

        return super(WidgetView, self).response_class(request, template, context, **response_kwargs)


# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
class DashboardPageView(DashboardView):
    """
    The base view for any dashboard type page. It checks for security as needed.
    """

    def __init__(self):
        super().__init__()
        XFNavigationViewMixin.__init__(self)

        self.page = None

    def dispatch(self, request, *args, **kwargs):
        self.page = Page.objects.get(slug=self.kwargs['slug'])

        if not self.page.allow_anonymous:
            if not self.request.user.is_authenticated():
                # return HttpResponseRedirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
                return redirect_to_login(self.request.path)

        return super(DashboardPageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
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
        if int(self.page.template.template_source) == int(UCModels.Template.DATABASE):
            template = Template(self.page.template.template_text)

            template2 = self.get_template2(template_name="dashboards/t_ibbs_overview.html")
            template2.template = template

            # We need to return the template here directly
            return super(DashboardPageView, self).response_class(request, template2, context, **response_kwargs)
            t = TemplateResponse(request, template)
            return t
        else:
            return super(DashboardPageView, self).response_class(request, template, context, **response_kwargs)


########################################################################################################################
class StartView(DashboardPageView):
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                if hasattr(user, "profile"):
                    if hasattr(user.profile, "default_perspective") and user.profile.default_perspective is not None:
                        url = reverse("load_perspective", args=[user.profile.default_perspective.id])
                        return HttpResponseRedirect(url)

                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                context["login_incorrect"] = True
        else:
            context["login_incorrect"] = True

        return super(TemplateView, self).render_to_response(context)


# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==

# Don't like these non-class based views, but they work, for now
def load_perspective(request, perspective_id):
    perspective = get_object_or_404(UCModels.Perspective, id=perspective_id)
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
        url = reverse("dashboards", args=[perspective.default_page.section.title, perspective.default_page.slug])
        # perspective.default_page
        return HttpResponseRedirect(url)

    # No perspecive - load default homepage
    return HttpResponseRedirect("/dashboards/home/overview/")
