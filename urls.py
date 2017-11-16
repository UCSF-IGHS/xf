from django.conf.urls import url
from django.views.generic import View
from django.views.generic import TemplateView, RedirectView



from .views import DashboardView, DashboardPageView, WidgetView, StartView
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'other/t_login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout' ),
    url(r'^widgets/(?P<perspective_slug>[-\w]+)/(?P<slug>[-\w]+)/$', WidgetView.as_view(), name='widgets'),
    url(r'^widgets/(?P<slug>[-\w]+)/$', WidgetView.as_view(), name='widgets'),
    url(r'^start/$', StartView.as_view(), name='dashboards', kwargs={'slug': 'welcome'}),
    url(r'^dashboards/perspectives/clear/$', views.clear_perspective, name='clear_perspective'),
    url(r'^perspectives/(?P<slug>[-\w]+)/$', views.load_perspective, name='load_perspective'),
    #url(r'^dashboards/perspectives/(?P<perspective_id>[-\w]+)/$', views.load_perspective, name='load_perspective'),
    url(r'^dashboards/0/(?P<section>[-\w]+)/(?P<slug>[-\w]+)/$', StartView.as_view(), name='dashboards_start'),
    #url(r'^dashboards/(?P<slug>[-\w]+)/$', DashboardPageView.as_view(), name='dashboards'),
    url(r'^dashboards/(?P<section>[-\w]+)/(?P<perspective_slug>[-\w]+)/(?P<slug>[-\w]+)/$', DashboardPageView.as_view(), name='dashboards'),
    #url(r'^dashboards/(?P<section>[-\w]+)/(?P<slug>[-\w]+)/$', DashboardPageView.as_view(), name='dashboards'),
    url(r'^dashboards/(?P<page_id>[-\w]+)/(?P<section>[-\w]+)/(?P<perspective_slug>[-\w]+)/(?P<slug>[-\w]+)/$', DashboardPageView.as_view(), name='dashboards'),
    url(r'^%s/(?P<section>[-\w]+)/(?P<perspective_slug>[-\w]+)/(?P<slug>[-\w]+)/$' %  (getattr(settings, "DASHGENT_PAGES", 'pages')), DashboardPageView.as_view(), name='pages'),
    url(r'^404$', TemplateView.as_view(template_name='404.html')),
    url(r'^500$', TemplateView.as_view(template_name='500.html')),
    url(r'^403$', TemplateView.as_view(template_name='403.html')),
]