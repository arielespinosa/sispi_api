from scripts.netcdf import NetCDF
import requests


def post_output():
    nc = NetCDF('files/wrfout_d03_2017-01-02_110000')
    vars_data = nc.get_as_json(pvars=["T2", "Q2", "QCLOUD"], reshape=True, as_float_list=True)

    forecast = []
    for i in range(75213):
        d = {
            "point": 0,
            "forecast": {
                "T2": vars_data["T2"][i],
                "Q2": vars_data["Q2"][i],
                "QCLOUD": vars_data["QCLOUD"][i]
            }
        }
        forecast.append(d)

    data = {
        "utc_init_date": "1927-02-07T08:04",
        "domain": 1,
        "forecast":  {
            "hour": 0,
            "forecast": forecast
        }
    }

    print("post")
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


if __name__ == '__main__':
    nc = NetCDF('/home/ariel/Trabajo/django_venv3.6/files/wrfout_d03_2017-01-02_110000')
    print(nc.__extra_vars__('SLP'))
    print(nc.__extra_vars__('SLP'))
    #post_domain()
    #post_output()
    #post_provinces_and_municipios()

    pass
