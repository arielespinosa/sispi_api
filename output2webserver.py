from scripts.netcdf import NetCDF
import requests
import json
from time import sleep
import Levenshtein

def post_output(f):
    nc = NetCDF(f)
    vars_data = nc.get_as_json(pvars=["T2", "Q2", "RAINC", "SLP", "WIND_S"], reshape=True, as_float_list=True)

    forecast = []
    for i in range(75213):
        d = {
            "point": 0,
            "forecast": {
                "T2": vars_data["T2"][i],
                "Q2": vars_data["Q2"][i],
                "RAINC": vars_data["RAINC"][i],
                "SLP": vars_data["SLP"][i],
                "WIND_S": vars_data["WIND_S"][i]
            }
        }
        forecast.append(d)

    data = {
        "utc_init_date": "1877-03-07T08:04",
        "domain": 1,
        "forecast":  {
            "hour": 0,
            "forecast": forecast
        }
    }

    r = requests.post('http://127.0.0.1:8000/sispi_api/v1.0/outputs/', json=data)
    print(r.status_code, r.elapsed, r.content)


def post_domain():
    nc = NetCDF('files/wrfout_d03_2017-01-02_110000')
    lat_lng = []

    for y in nc.xlat:
        for x in nc.xlon:
            lat_lng.append([float(y), float(x)])

    data = {
        "slug_name": "3km",
        "resolution": 3,
        "description": "SisPI 3 km domain",
        "model": "SisPI",
        "hour": 5,
        "lat_lng": lat_lng

    }

    #r = requests.post('http://127.0.0.1:8000/sispi_api/v1.0/meta/domains/', json=data)
    #print(r.status_code, r.elapsed, r.content)


def post_provinces_and_municipios():
    r = requests.get('http://127.0.0.1:8000/sispi_api/v1.0/init/provinces/')
    print(r.status_code, r.elapsed, r.content)


def provincias_municipios():

    with open('sispi/fixtures/provincias_y_municipios.json') as f:
        data = json.load(f)

    with open('fichero.json') as f:
        data2 = json.load(f)

    municipios_dict = {}
    i = 1
    data = data["provincias"]
    for prov_key in data.keys():
        print(data[prov_key].keys())
        municipios = data[prov_key]["municipios"]

        for municipio in municipios:
            for feature in data2["features"]:
                try:
                    if feature["Name_PROV"] == prov_key.lower() and feature["Name_MUN"] == municipio.lower():
                        geometry = feature["properties"]["geometry"]
                        mun = {'name': municipio, 'geometry': geometry}
                        municipios_dict.update({str(i):mun})
                        i += 1
                except:
                    pass


            data[prov_key]["municipios"] = municipios_dict


def to_minusculas():
    with open('/home/ariel/munic.geojson') as f:
        d = json.load(f)

    i=0
    tildes = ['á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú']
    vocales = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

    for feature in d['features']:
        try:
            prov = feature['properties']["Name_PROV"]
            mun = feature['properties']["Name_MUN"]

            j=0
            for l in tildes:
                if l in prov:
                    prov = prov.replace(l, vocales[j])
                if l in mun:
                    mun = mun.replace(l, vocales[j])
                j += 1
        except:
            print(feature.keys())
            print(feature['properties'].keys())
            print(i)
            i+=1
            continue

        feature['properties']["Name_PROV"] = prov.lower()
        feature['properties']["Name_MUN"] = mun.lower()

    with open('fichero.json', 'w') as f:
        json.dump(d, f)


def asignar_geom():
    with open('sispi/fixtures/provincias_y_municipios.json') as f:
        data = json.load(f)

    with open('fichero.json') as f:
        fichero = json.load(f)

    i = 0
    tildes = ['á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú']
    vocales = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

    for prov in data['provincias'].keys():
        if prov != '16':
            provincia = data['provincias'][prov]['name']

            j = 0
            for l in tildes:
                if l in provincia:
                    provincia = provincia.replace(l, vocales[j])
                j += 1
            provincia = provincia.lower()

            for mun in data['provincias'][prov]["municipalities"].keys():
                municipio = data['provincias'][prov]["municipalities"][mun]['name']
                j = 0
                for l in tildes:
                    if l in municipio:
                        municipio = municipio.replace(l, vocales[j])
                    j += 1
                municipio = municipio.lower()

                for feature in fichero['features']:

                    try:
                        provaux = feature['properties']["Name_PROV"]
                        munaux = feature['properties']["Name_MUN"]
                    except:
                        continue

                    try:
                        if provincia == 'pinar del rio' and municipio == 'san juan y martinez':
                            municipio = 'san juan'
                        elif provincia == 'mayabeque' and municipio == 'san nicolas de bari':
                            municipio = 'san nicolas'
                        elif provincia == 'cienfuegos' and 'lajas' in municipio:
                            municipio = 'lajas'
                        elif provincia == 'camagüey' and 'carlos' in municipio:
                            municipio = 'carlos manuel de ces'
                        elif provincia == 'las tunas' and 'amancio' in municipio:
                            municipio = 'amancio'
                        elif provincia == 'santiago de cuba' and 'mella' in municipio:
                            municipio = 'mella'

                        if Levenshtein.distance(provincia, provaux) < 4 and Levenshtein.distance(municipio, munaux) < 4:
                            data['provincias'][prov]["municipalities"][mun]['geometry'] = feature["geometry"]
                    except:
                         if provaux is None:
                             geom_aux = feature["geometry"]

            else:
                data['provincias']['16']['geometry'] = geom_aux

    with open('sispi/fixtures/provincias_y_municipios_3.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    #nc = NetCDF('/home/ariel/Trabajo/django_venv3.6/files/wrfout_d03_2017-01-02_110000')
    #print(nc.__extra_vars__('SLP'))

    #post_domain()
    #post_output('/home/ariel/Trabajo/django_venv3.6/files/wrfout_d03_2017-01-02_110000')
    #post_provinces_and_municipios()

    #provincias_municipios()

    r = requests.get('http://127.0.0.1:8000/sispi_api/v1.0/init/provinces/')
    print(r.status_code, r.elapsed, r.content)









