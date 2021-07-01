from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import viewsets, status
from sispi.serializers.meta import *
from threading import Thread
import os
import json
from sispi_api.settings import BASE_DIR
import Levenshtein


def init_provinces(request, *args, **kwargs):
    # Seek how update geom too
    file = os.path.join(BASE_DIR, 'sispi/fixtures/provincias_y_municipios.json')

    with open(file, 'r') as f:
        data = json.load(f)
    f.close()

    for key in data.keys():
        if key == 'provincias':
            for key2 in data[key].keys():
                province = Province.objects.create(name=data[key][key2]['nombre'], short_name=data[key][key2]['codigo'])

                if key2 != '16':
                    for nombre in data[key][key2]['municipios']:
                        Municipality.objects.create(name=nombre, province=province)
                        
    return JsonResponse({'msg': 'All data was saved successfully'}, status=status.HTTP_200_OK)

# delete on production
def update_municipality(request, *args, **kwargs):

    munc = []
    municipios = [m.municipio for m in Municipios.objects.all()]

    for m in Municipality.objects.filter(name="Caimanera", geom__isnull=True):

        ml = m.name.lower()

        for municipio in municipios:
            munl = municipio.lower()

            d = Levenshtein.distance(ml, munl)

            if d < 4:
                try:
                    if municipio == "San Luis":
                        muni = Municipios.objects.get(municipio=municipio, provincia=m.province.name)
                    else:
                        muni = Municipios.objects.get(municipio=municipio)
                    m.geom = muni.geom
                    m.save()
                    continue
                except:
                    munc.append(municipio)

    return JsonResponse({'msg': munc}, status=status.HTTP_200_OK)
# //------------------------------------------------------------------------------------------------


class DomainModelViewSet(viewsets.ModelViewSet):
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()

    def points_to_db(self, domain, lat_lng):
        for p in lat_lng:
            pnt = PointLocation.objects.create(location=GEOSGeometry('POINT ({} {})'.format(p[1], p[0]), srid=4326))
            domain.points.add(pnt)

    def add_points(self, domain, lat_lng, thr):
        spl = int(len(lat_lng) / thr)
        threads = []

        for i in range(thr-1):
            threads.append(Thread(target=self.points_to_db, args=(domain, lat_lng[i*spl:(i+1)*spl])))

        if len(lat_lng) > spl*thr:
            threads.append(Thread(target=self.points_to_db, args=(domain, lat_lng[spl*(thr-1):])))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def create(self, request, *args, **kwargs):
        thr = request.data.pop('threads', 8)
        lat_lng = request.data.pop('lat_lng', None)

        domain_serializer = self.serializer_class(data=request.data)

        if not domain_serializer.is_valid():
            return Response(domain_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            domain = domain_serializer.save()

            if lat_lng:
                # Build grid atrib for domain using lat_lng
                # domain.grid = grid
                domain.save()
                self.add_points(domain, lat_lng, thr)

            return JsonResponse({'msg': 'Domain was saved successfully'}, status=status.HTTP_201_CREATED)


class MetVariabletModelViewSet(viewsets.ModelViewSet):
    serializer_class = MetVariableSerializer
    queryset = MetVariable.objects.all()


class ProvincesModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProvincesSerializer
    queryset = Province.objects.all()


class MunicipalitiesModelViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipalitiesSerializer
    queryset = Municipality.objects.all()












