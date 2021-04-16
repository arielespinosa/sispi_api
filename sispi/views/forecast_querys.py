from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView

from sispi.models.meta import Province
from sispi.serializers.forecast import ProvinceForecastSerializer

# http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class ForecastViewSet(APIView):
    province_serializer = ProvinceForecastSerializer

    def get(self, request, *args, **kwargs):
        province_name = kwargs.get('province', None)

        if province_name:
            province = Province.objects.get(name='Villa Clara')
            return province.forecast()

        return JsonResponse({'d':1})