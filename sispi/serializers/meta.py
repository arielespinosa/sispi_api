from rest_framework import serializers
from sispi.models.meta import *


class DomainSerializer(serializers.ModelSerializer):
    lat = serializers.CharField(max_length=2000, required=False)
    lng = serializers.CharField(max_length=2000, required=False)

    class Meta:
        model = Domain
        exclude = ['grid', 'points']


class MetVariableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MetVariable
        fields = '__all__'
        # fields = ['domain', 'date', 'variables', 'nc_file']

        """
        def create(self, validated_data):
            print("hola")
            ncfile = NetCDF("/home/ariel/Trabajo/django_env/SisPI_API/wrfout_d03_2017-01-02_110000")
            #netcdf_file = NetCDF(validated_data['nc_file'].name)
            variables = ncfile.get_as_json(["RAINC", "RAINNC"])

            domain = validated_data['domain']
            date = validated_data['date']

            sispi_output =SisPIOutput(
                domain=domain,
                date=date
                )

            sispi_output.save()
            return validated_data
        """


class ProvincesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Province
        fields = '__all__'


class MunicipalitiesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Municipality
        fields = '__all__'
