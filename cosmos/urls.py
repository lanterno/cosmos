from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views

from cosmos.core.views import SwaggerSchemaView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='docs', permanent=False), name='index'),
    path('api/docs/', SwaggerSchemaView.as_view(), name='docs'),
    path('api/v1/auth/', include('cosmos.accounts.urls', namespace='auth')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
