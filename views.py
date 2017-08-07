


class XFNavigationViewMixin():
    """
    This class enables the new navigation tree. You should use it by calling self.set_navigation_context() within the
    get_context_data method of your view.

    The navigation tree is shared across apps.

    """

    navigation_tree_observers = []

    def set_navigation_context(self):
        """

        :return:
        """

        # Create a navigation_tree list in the context if it doesn't exist already
        if not self.context.has_key("navigation_trees"):
            self.context["navigation_trees"] = {}

        # Call all observers and provide them an opportunity to add their links to the navigation tree
        for observer in XFNavigationViewMixin.navigation_tree_observers:
            observer(self, self.context["navigation_trees"], self.request)


