from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

import xf.uc_dashboards
from xf.uc_dashboards.views.dashboard_page_view import DashboardPageView


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
                        url = reverse("load_perspective", args=[user.profile.default_perspective.slug])

                        # Load the user's default perspective
                        perspective = get_object_or_404(xf.uc_dashboards.models.perspective.Perspective, id=user.profile.default_perspective.id)
                        perspective = request.user.load_perspective(perspective, True)
                        if perspective:
                            request.session["perspective_id"] = perspective.id

                        # If a next parameter is available, navigate to that page
                        # If not, load the perspective's default page
                        next_url = request.GET.get('next', '/')
                        if next_url != "/" and next_url != "/dashboards/home/overview/":
                            url = next_url

                        return HttpResponseRedirect(url)

                # If the user doesn't have a profile, check the next parameter, or go to the home page
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                context["login_incorrect"] = True
        else:
            context["login_incorrect"] = True

        return super(TemplateView, self).render_to_response(context)