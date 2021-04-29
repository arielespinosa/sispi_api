from django.contrib.gis.db.models.functions import Distance, Intersection
from django.http import JsonResponse
from rest_framework import viewsets, status
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from sispi.serializers.outputs import *


class ForecastModelViewSet(viewsets.ModelViewSet):
    serializer_class = ForecastSerializer
    queryset = Forecast.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()

        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)

        if lat and lng:
            pnt = GEOSGeometry('POINT ({} {})'.format(lng, lat), srid=4326)
            qs = qs.annotate(distance=Distance('location', pnt)).order_by('distance')

        return qs


class OutputModelViewSet(viewsets.ModelViewSet):
    serializer_class = RunOutputSerializer
    forecast_serializer = ForecastSerializer
    queryset = RunOutput.objects.all()

    def update_forecast_points(self, domain_pk, forecast_data):
        domain = Domain.objects.get(pk=domain_pk)
        i = 0
        for point in domain.points.all():
            forecast_data["forecast"][i].update({"point": point.pk})
            i += 1

    def create(self, request, *args, **kwargs):
        forecast_data = request.data.pop('forecast', None)

        output = RunOutput.objects.filter(utc_init_date=request.data.get('utc_init_date'), domain=request.data.get('domain')).first()

        if not output:
            output_serializer = self.serializer_class(data=request.data)

            if not output_serializer.is_valid():
                return Response(output_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                output = output_serializer.save()

        # Check if exist another var
        """
        vars = forecast_data["forecast"][0].keys()       
        met_vars = MetVariable.objects.filter(short_name__in = [vars]).distinct()
        if met_vars.count() < len(vars):
            for var in met_vars:
                pass
        """

        # Assign right point pk to forecast point key
        self.update_forecast_points(output.domain.pk, forecast_data)

        forecast_serializer = self.forecast_serializer(data=forecast_data)
        if not forecast_serializer.is_valid():
            response = {
                'msg': 'Some errors has been detected',
                'errors': forecast_serializer.errors
            }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

        forecast = forecast_serializer.save()
        output.forecast.add(forecast)

        return JsonResponse({'msg': 'All data was saved successfully'}, status=status.HTTP_201_CREATED)


