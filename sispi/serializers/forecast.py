from rest_framework import serializers


class ProvinceForecastSerializer(serializers.Serializer):
    min = serializers.FloatField()
    max = serializers.FloatField()
    med = serializers.FloatField()

    class Meta:
        fields = '__all__'
