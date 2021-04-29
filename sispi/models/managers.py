from django.contrib.gis.db import models
from django.http import JsonResponse
#from sispi.models.outputs import RunOutput


class ProvincesManager(models.Manager):

    def forecast(self):
        data = {'max': 3, 'min': 1, 'mean': 2.5}
        return JsonResponse(data)


class MunicipalitiesManager(models.Manager):

    def set_forecast(self):
        #output = RunOutput.objects.latest('utc_init_date')
        #forecast = output.forecast.latest('hour')
        #print(output.pk, output.utc_init_date)
        #print(forecast.pk, forecast.hour)
        data = {'max': 3, 'min': 1, 'mean': 2.5}
        return JsonResponse(data)
