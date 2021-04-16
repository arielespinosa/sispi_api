from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from .meta import Domain, MetVariable, PointLocation


class Forecast(models.Model):
    """
    Forecast field contains all vars with its forecast values
    for a point in json format. This field replace variable & value
    features. Doing this the instance in database reduce x/y % where
     x is the number of vars and y the hour*number_of_vars
    """
    v_lvl = models.SmallIntegerField(default=0)
    point = models.ForeignKey(PointLocation, on_delete=models.DO_NOTHING, blank=True, null=True) # Find if this can be define in 3D
    forecast = JSONField(null=True, blank=True)

    def __str__(self):
        return self.pk


class Output(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING, related_name='domain')
    utc_init_date = models.DateTimeField()
    hour = models.PositiveSmallIntegerField(default=0)
    forecast = models.ManyToManyField(Forecast, related_name='outputs', blank=True, null=True)

    def __str__(self):
        return 'Output {}'.format(self.utc_init_date)

    def utc_ini_date_2_local(self):
        return self.utc_init_date

