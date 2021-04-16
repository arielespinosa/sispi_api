from scripts.netcdf import NetCDF
import requests

if __name__ == '__main__':
    nc = NetCDF('files/wrfout_d03_2017-01-02_110000')
    vars_data = nc.get_as_json(pvars=["T2", "Q2", "QCLOUD"], reshape=True, as_list=True)

    forecast = []
    for i in range(72146):
        d = {
            "v_lvl": 1,
            "point": i,
            "forecast": {
                "T2": vars_data["T2"][i],
                "Q2": vars_data["Q2"][i],
                "QCLOUD": vars_data["QCLOUD"][i]
            }
        }
        forecast.append(d)

    data = {
        "utc_init_date": "1900-02-07T08:04",
        "domain": 1,
        "forecast": forecast
    }

    r = requests.post('http://127.0.0.1:8000/sispi_api/v1.0/outputs/', json=data)
    print(r.status_code, r.elapsed, r.content)
