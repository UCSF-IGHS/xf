import ast

from django.utils.translation import get_language


class XFNavigationViewMixin(object):
    site_settings = None

    """
    This class enables the new navigation tree. You should use it by calling self.set_navigation_context() within the
    get_context_data method of your view.

    The navigation tree is shared across apps. Each app will get their own tree.

    """

    navigation_tree_observers = []

    def __init__(self):
        if hasattr(self, "lc"):
            if XFNavigationViewMixin.site_settings is not None:
                self.lc = XFNavigationViewMixin.site_settings.site_default_language
            else:
                self.lc = "en"
        else:
            self.lc = "en"

        pass

    def set_navigation_context(self):
        """

        :return:
        """

        # Create a navigation_tree list in the context if it doesn't exist already
        # if not self.context.has_key("navigation_trees"):
        # PYTHON3 UPDATE
        if not "navigation_trees" in self.context:
            self.context["navigation_trees"] = {}

        # Call all observers and provide them an opportunity to add their links to the navigation tree
        for observer in XFNavigationViewMixin.navigation_tree_observers:
            observer(self, self.context["navigation_trees"], self.request)

        # Site settings are passed here

        self.context["site_title"] = XFNavigationViewMixin.site_settings.site_title
        self.context["custom_theme"] = XFNavigationViewMixin.site_settings.custom_theme
        if XFNavigationViewMixin.site_settings.footer_details is not None:
            self.context["footer_details"] = ast.literal_eval(
                "{" + XFNavigationViewMixin.site_settings.footer_details + "}")
        if hasattr(self, "lc"):
            self.context["site_title"] = XFNavigationViewMixin.site_settings.translate("site_title", self.lc)
        else:
            self.context["site_title"] = XFNavigationViewMixin.site_settings.translate("site_title", "en")
        self.context["site_icon"] = XFNavigationViewMixin.site_settings.site_icon

        print(get_language())
