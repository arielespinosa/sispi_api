from django.contrib.gis.db import models
from django.http import JsonResponse


class ProvincesManager(models.Manager):

    def forecast(self):
        data = {'max': 3, 'min': 1, 'mean': 2.5}
        return JsonResponse(data)


