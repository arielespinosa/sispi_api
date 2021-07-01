from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import viewsets, status
from sispi.serializers.meta import *
from threading import Thread
import os
import json
from sispi_api.settings import BASE_DIR
import Levenshtein
from django.contrib.gis.geos import MultiPolygon
import numpy as np


def init_provinces(request, *args, **kwargs):
    # Seek how update geom too

    file = os.path.join(BASE_DIR, 'sispi/fixtures/provincias_y_municipios.json')
    data = json.load(open(file))

    for key in data.keys():
        if key == 'provincias':
            for key2 in data[key].keys():
                province = Province.objects.create(name=data[key][key2]['nombre'], short_name=data[key][key2]['codigo'])

                if key2 != '16':
                    for nombre in data[key][key2]['municipios']:
                        Municipality.objects.create(name=nombre, province=province)
                        
    return JsonResponse({'msg': 'All data was saved successfully'}, status=status.HTTP_200_OK)


def init_provinces_2(request, *args, **kwargs):
    # Seek how update geom too
    file = os.path.join(BASE_DIR, 'sispi/fixtures/provinces.json')

    with open(file, 'r') as f:
        data = json.load(f)
    f.close()

    for key in data.keys():
        if key == 'provincias':
            for key2 in data[key].keys():
                province = Province.objects.get(short_name=data[key][key2]['code'])

                poligons = data[key][key2]['geom']["coordinates"][0] = [x[:-1] for x in data[key][key2]['geom']["coordinates"][0]]
                geometry = {"type": "MultiPolygon", "coordinates": poligons}
                province.geom = GEOSGeometry(str(geometry))
                province.save()

                if key2 != '16':
                    for pk in data[key][key2]['municipalities'].keys():
                        nombre = data[key][key2]['municipalities'][pk]['name']
                        municipality = Municipality.objects.get(name=nombre, province=province)
                        n_poligons = len(data[key][key2]['municipalities'][pk]['geometry']['coordinates'])
                        poligons = []

                        for i in range(n_poligons):
                            points = np.array(data[key][key2]['municipalities'][pk]['geometry']['coordinates'][i][0])
                            poligons.append(points[:, :2].tolist())

                        geometry = {"type": "MultiPolygon", "coordinates": poligons}
                        municipality.geom = GEOSGeometry(str(geometry))
                        municipality.save()

    return JsonResponse({'msg': 'All data was saved successfully'}, status=status.HTTP_200_OK)


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


def check_domain_points_on_municipality(request, *args, **kwargs):
    d = Domain.objects.get(pk=1)
    points = Municipality.objects.get(pk=1, geom__contains=d.points)
    print(points)


