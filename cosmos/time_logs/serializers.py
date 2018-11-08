from rest_framework import serializers

from .models import TimeLog


class TimeLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeLog
        fields = ('project', 'start', 'end', 'description', 'creation_type')