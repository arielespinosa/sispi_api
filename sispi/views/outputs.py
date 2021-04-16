from django.contrib.gis.db.models.functions import Distance, Intersection
from django.http import JsonResponse
from rest_framework import viewsets, status
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from sispi.serializers.outputs import *
from threading import Thread
import time


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
    serializer_class = OutputSerializer
    forecast_serializer = ForecastSerializer
    queryset = Output.objects.all()

    def forecast_2_db(self, output, forecast_data, forecast_with_errors, i):
        for forecast in forecast_data:
            forecast_serializer = self.forecast_serializer(data=forecast)

            if not forecast_serializer.is_valid():
                forecast_with_errors.update({str(i): (forecast, forecast_serializer.errors)})
            else:
                output.forecast.add(forecast_serializer.save())

    def create(self, request, *args, **kwargs):
        forecast_data = request.data.pop('forecast')
        output_data = request.data

        output_serializer = self.serializer_class(data=output_data)

        if not output_serializer.is_valid():
            return Response(output_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            output = output_serializer.save()

            forecast_with_errors, i = {}, 0
            """
            for forecast in forecast_data:
                forecast_serializer = self.forecast_serializer(data=forecast)

                if not forecast_serializer.is_valid():
                    forecast_with_errors.update({str(i): (forecast, forecast_serializer.errors)})
                else:
                    output.forecast.add(forecast_serializer.save())
            """
            h = request.POST.get('h', 8)
            s = int(len(forecast_data)/h)
            data = []

            # Build data small piece for each thread
            for i in range(h-1):
                data.append(forecast_data[i*s:(i+1)*s])
            if h*s < len(forecast_data):
                data.append(forecast_data[h*s:])

            # Creating threads list
            threads = [Thread(target=self.forecast_2_db, args=(output, d, forecast_with_errors, i)) for d in data]

            # Launch threads
            for t in threads:
                t.start()

            for t in threads:
                t.join()

            if len(forecast_with_errors) is 0:
                return JsonResponse({'msg': 'All data was saved succesfully'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({
                    'msg': 'Some forecast data have problems and was not saved to database',
                    'forecast_with_errors': forecast_with_errors
                }, status=status.HTTP_206_PARTIAL_CONTENT)


