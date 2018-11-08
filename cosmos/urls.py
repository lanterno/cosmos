from django.urls import path, include
from rest_framework.routers import SimpleRouter

from cosmos.projects.views import ProjectViewSet
from cosmos.time_logs.views import TimeLogViewSet


router = SimpleRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'time_logs', TimeLogViewSet)


urlpatterns = [
    path('api/v1/auth/', include('cosmos.accounts.urls', namespace='auth')),

] + router.urls
