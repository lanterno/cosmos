from django.conf.urls import include, url

from . import views


app_name = 'accounts'

urlpatterns = (
    url(r'^disable-account/$', views.SuspendAccountView.as_view(), name='disable_account'),
    url(r'^activate/$', views.ActivationView.as_view(), name='activate'),
    url(r'^', include('djoser.urls')),
    url(r'^', include('djoser.urls.authtoken')),
    url(r'^', include('rest_social_auth.urls_token')),
)
