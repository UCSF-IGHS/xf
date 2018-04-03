import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


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
        if request.GET.get('embed') is not None:
            context['extends'] = 'listview_generic_embedded.html'
            context['ajax'] = '&embed'
        elif request.GET.get('ajax') is not None:
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
            return redirect('./')
        else:
            self.message = self.success_message
            self.success = True
            return_value = {'success': self.success, 'message': self.message, 'pk': self.object.id, 'object': self.object.__str__()}
            #print return_value
            return HttpResponse(json.dumps(return_value), content_type='application/json', )

    def xf_is_ajax(self):

        return self.request.GET.get('ajax') is not None or self.request.is_ajax()

    def prepare_ajax_post_response(self, **kwargs):

        if self.xf_is_ajax():

            self.message = self.success_message
            if self.success:
                payload = {'success': self.success, 'message': self.message}
                return HttpResponse(json.dumps(payload), content_type='application/json', )
            else:
                self.resp = self.render_to_response(self.get_context_data(**kwargs)).rendered_content
                payload = {'success': self.success, 'message': self.message, 'html': self.resp}
                return HttpResponse(json.dumps(payload), content_type='application/json', )

        else:
            if self.success:
                context = self.get_context_data(**kwargs)
                return HttpResponseRedirect(context['next_url'])
            else:
                # Do something here that renders the error message
                return self.render_to_response(self.get_context_data(**kwargs))

