from django.urls import path, include
from rest_framework.routers import SimpleRouter

from cosmos.projects.views import ProjectViewSet

router = SimpleRouter()
router.register(r'projects', ProjectViewSet)


urlpatterns = [
    path('api/v1/auth/', include('cosmos.accounts.urls', namespace='auth')),

] + router.urls
