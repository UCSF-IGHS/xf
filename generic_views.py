

class AjaxViewMixin():
    """
    Enables Ajax functionality and compatibility. Wraps responses to JSON when needed.
    """

    success_message = "Operation completed"
    ajax_template_name = "ajax_widget.html"

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

