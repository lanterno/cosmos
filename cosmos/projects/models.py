from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    estimation = models.IntegerField(null=True)

    created_by = models.ForeignKey('accounts.User', related_name='created_projects', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('created_by', 'name')
