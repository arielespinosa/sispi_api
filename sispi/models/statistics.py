from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.http import JsonResponse
#from sispi.models.meta import Municipality

"""
class Historical(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    data = JSONField(blank=True, null=True)

    def __str__(self):
        return self.municipality
"""