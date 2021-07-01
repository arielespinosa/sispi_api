from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save

from .meta import Domain, MetVariable, PointLocation


class Forecast(models.Model):
    hour = models.PositiveSmallIntegerField(default=0)
    forecast = JSONField(null=True, blank=True)

    def __str__(self):
        return self.pk


class RunOutput(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING, related_name='domain')
    utc_init_date = models.DateTimeField()
    forecast = models.ManyToManyField(Forecast, related_name='outputs', blank=True, null=True)

    def __str__(self):
        return 'Output {}'.format(self.utc_init_date)

    def utc_ini_date_2_local(self):
        return self.utc_init_date


