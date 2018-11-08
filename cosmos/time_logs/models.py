from django.db import models


class TimeLog(models.Model):
    REALTIME = 0
    SYNCED = 1
    ADDED_MANUALLY = 2
    CREATION_TYPES = (
        (REALTIME, 'RealTime'),
        (SYNCED, 'Synced'),
        (ADDED_MANUALLY, 'Added manually'),
    )

    project = models.ForeignKey('projects.Project', related_name='time_logs', on_delete=models.PROTECT)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    description = models.TextField(null=True)

    creation_type = models.PositiveSmallIntegerField(choices=CREATION_TYPES, default=REALTIME)

    def __str__(self):
        return "Log: {} - {} - in project: {}".format(self.start, self.end, str(self.project))
