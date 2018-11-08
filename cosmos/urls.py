from django.urls import path, include
from rest_framework.routers import SimpleRouter


urlpatterns = [
    path('api/v1/auth/', include('cosmos.accounts.urls', namespace='auth')),

]
