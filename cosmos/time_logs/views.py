from rest_framework.viewsets import ModelViewSet

from .serializers import TimeLogSerializer
from .models import TimeLog


class TimeLogViewSet(ModelViewSet):
    serializer_class = TimeLogSerializer
    queryset = TimeLog
