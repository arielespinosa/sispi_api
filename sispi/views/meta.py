from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import viewsets, status
from sispi.serializers.meta import *


class DomainModelViewSet(viewsets.ModelViewSet):
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()

    def create(self, request, *args, **kwargs):

        """
        lat = request.POST.get('lat', None)
        lng = request.POST.get('long', None)
        name = request.POST.get('name', None)
        resolution = request.POST.get('r', None)
        # grid = models.PolygonField(blank=True, null=True)
        description = request.POST.get('d', None)
        model = request.POST.get('m', None)
        """

        #print(request.POST)

        domain_serializer = self.serializer_class(data=request.POST)
        #domain = Domain(slug_name=name, resolution=resolution, grid=None, description=description, model=model)
        if not domain_serializer.is_valid():
            return Response(domain_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            lat = [float(val) for val in domain_serializer.validated_data.pop('lat').split(',')]
            lng = [float(val) for val in domain_serializer.validated_data.pop('lng').split(',')]

            domain = domain_serializer.save()

            """
            # Add points to domain.
            # Check if this algorithm can do it in threads
            
            for y, x in zip(lat, lng):
                pnt = PointLocation.objects.create(location=GEOSGeometry('POINT ({} {})'.format(x, y), srid=4326))
                domain.points.add(pnt)
            """
            return JsonResponse({'do': 'done'})


class MetVariabletModelViewSet(viewsets.ModelViewSet):
    serializer_class = MetVariableSerializer
    queryset = MetVariable.objects.all()


class ProvincesModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProvincesSerializer
    queryset = Province.objects.all()


class MunicipalitiesModelViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipalitiesSerializer
    queryset = Municipality.objects.all()









