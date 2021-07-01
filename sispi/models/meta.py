from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from sispi.models.managers import ProvincesManager, MunicipalitiesManager

MODEL_CHOICES = [
    ('SisPI', 'Sistema de Pronóstico Inmediato'),
    ('SPNOA', 'Śistema de Pronóstico Oceano-Atmosférico')
]


class UM(models.Model):
    slug_name = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.slug_name


class PointLocation(models.Model):
    location = models.PointField(blank=True)

    def __str__(self):
        return '{}'.format(self.location)


class MetVariable(models.Model):
    name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    um = models.ForeignKey(UM, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name


class Domain(models.Model):
    slug_name = models.SlugField(max_length=5)
    resolution = models.IntegerField()
    grid = models.PolygonField(blank=True, null=True)  # The ractangle area. Check if the object is the apropiate
    description = models.CharField(max_length=500, blank=True, null=True)
    model = models.CharField(max_length=10, choices=MODEL_CHOICES, blank=True, null=True)
    points = models.ManyToManyField(PointLocation, related_name='domain')

    def __str__(self):
        return '{} km'.format(self.resolution)

    def save(self, *args, **kwargs):
        if self.pk:
            if not self.grid:
                # Create grid atribute
                pass
            else:
                my_self = Domain.objects.get(pk=self.pk)
                if (my_self.top_lat, my_self.bottom_lat, my_self.left_long, my_self.right_long) != (self.top_lat, self.bottom_lat, self.left_long, self.right_long):
                    # Update grid atribute
                    pass
        super(Domain, self).save(*args, **kwargs)


class Province(models.Model):
    short_name = models.SlugField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    km2 = models.FloatField(blank=True, null=True)
    geom = models.MultiPolygonField(srid=4608, blank=True, null=True)
    objects = ProvincesManager()

    def __str__(self):
        return self.name

    def forecast(self):
        data = {'max': 3, 'min': 1, 'mean': 2.5}
        return JsonResponse(data)


class Municipality(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    km2 = models.FloatField(blank=True, null=True)
    geom = models.MultiPolygonField(srid=4608, blank=True, null=True)
    objects = MunicipalitiesManager()

    def __str__(self):
        return self.name

    def domain_points(self, domain_pk):
        domain = Domain.objects.get(pk=domain_pk)
        geom = GEOSGeometry(self.geom, srid=4608)
        return [point for point in domain.points.all() if geom.contains(GEOSGeometry(point.location))]

    def forecast(self):
        data = {'max': 3, 'min': 1, 'mean': 2.5}
        return JsonResponse(data)


# Delete this on production
# This model its only for update sispi_municipality table
class Municipios(models.Model):
    geom = models.MultiPolygonField(srid=4608, blank=True, null=True)
    municipio = models.CharField(max_length=25, blank=True, null=True)
    provincia = models.CharField(max_length=25, blank=True, null=True)
    area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'municipios'
