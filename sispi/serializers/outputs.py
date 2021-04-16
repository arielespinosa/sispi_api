from rest_framework import serializers
from sispi.models.outputs import *


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = '__all__'


class OutputSerializer(serializers.ModelSerializer):
    forecast = ForecastSerializer(many=True, read_only=True)

    class Meta:
        model = Output
        fields = '__all__'
