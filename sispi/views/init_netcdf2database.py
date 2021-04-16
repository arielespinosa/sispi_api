from django.contrib.gis.geos import GEOSGeometry
from rest_framework import viewsets, status
from rest_framework.views import APIView
from sispi.serializers.meta import *
from scripts.netcdf import NetCDF
from sispi.models.outputs import PointLocation
import numpy as np


class NetCDF2DataBase(APIView):

    def get(self, request, *args, **kwargs):
        nc = NetCDF('wrfout_d03_2017-01-02_110000')
        data = nc.get_as_json(pvars=["XLAT", "XLONG"], reshape=True)

        # Replace data for request.GET
        lat = data.get('XLAT', None)
        lng = data.get('XLONG', None)

        """
        # Check if this algorithm can do it in threads
        if lat is not None and lng is not None:
            # Create Points Location object
            for y in lat:
                for x in lng:
                    pnt = GEOSGeometry('POINT ({} {})'.format(x, y), srid=4326)
                    PointLocation.objects.create(location=pnt)
        """

        return JsonResponse({'d':1})











