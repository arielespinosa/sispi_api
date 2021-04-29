from rest_framework import serializers
from sispi.models.outputs import *


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = '__all__'


class RunOutputSerializer(serializers.ModelSerializer):
    forecast = ForecastSerializer(many=True, read_only=True)

    class Meta:
        model = RunOutput
        fields = '__all__'
