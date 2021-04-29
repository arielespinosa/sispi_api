from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from .meta import Domain, MetVariable, PointLocation, Province, Municipality
import django


class ProvinceForecast(models.Model):
    """
    Forecast feature have this structure:
    {
        "varname":{
            "min": value,
            "max": value,
            "mean": value,
        }
    }
    """
    date_time = models.DateTimeField(default=django.utils.timezone.now())
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="forecast")
    forecast = JSONField(null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.province, self.date_time)


class MunicipalityForecast(models.Model):
    """
     Forecast feature have this structure:
     {
         "varname":{
             "min": value,
             "max": value,
             "mean": value,
         }
     }
     """
    date_time = models.DateTimeField(default=django.utils.timezone.now())
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="forecast")
    forecast = JSONField(null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.municipality, self.date_time)

