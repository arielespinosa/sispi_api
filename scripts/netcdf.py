import numpy as np
import os
from pickle import dump, load
from scipy.io import netcdf as nc
from wrf import getvar


class NetCDF:
    filename, data, dataset = None, dict(), None

    def __init__(self, filename=None):
        self.filename = filename
        if self.filename is not None:
            if self.filename[-4:] != '.dat':
                try:
                    self.dataset = nc.netcdf_file(self.filename, 'r')
                except ValueError or FileNotFoundError:
                    pass
            else:
                self.__load_from_file__(self.filename)

    @property
    def xlon(self):
        return np.array(self.dataset.variables['XLONG'][0, 0])

    @property
    def xlat(self):
        return np.array(self.dataset.variables['XLAT'][0, :, 0])

    def vars(self, var_list, round_to=3):
        """
        var_list: Python array whit var required name
        round: Number of decimal to round vars value
        return: A python dict with shape {var_key: value}
        """
        #data = dict()

        try:
            for var in var_list:
                value = self.dataset.variables[var][:].reshape((183, 411))

                value = value[-1::-1, :]
                value = np.around(value, decimals=round_to)

                var_key = dict({var: value})
                self.data.update(var_key)
                del value, var_key

            return self.data
        except KeyError:
            raise KeyError

    def dupms_to_file(self, filename):
        with open(filename, "wb") as f:
            dump(self.data, f, protocol=2)

    def __extra_vars__(self, var):

        if var == 'WIND_S':
            u10 = self.dataset.variables['U10'][:]
            v10 = self.dataset.variables['V10'][:]
            return np.sqrt(u10**2 + v10**2)

        elif var == 'SLP':
            return getvar(self.dataset, "slp")

    def save(self, filename):
        if filename.find("/") == -1:
            with open(filename, "wb") as f:
                dump(self.data, f, protocol=2)
        else:
            if os.path.exists(filename):
                with open(filename, "wb") as f:
                    dump(self.data, f, protocol=2)
            else:
                try:
                    os.mkdir(filename[:filename.rfind('/') + 1])
                except FileExistsError:
                    pass

                with open(filename, "wb") as f:
                    dump(self.data, f, protocol=2)

    # Carga los datos desde un fichero el cual se indica su nombre. Los datos son devueltos
    def __load_from_file__(self, filename):
        with open(filename, "rb") as f:
            self.data = load(f)
        self.dataset = self.data

    # Dado el indice de un punto, devuelve los valores de latitud y longitud
    def Localization(self, i_lat, i_long):
        longitud = self.dataset.variables['XLONG'][0][i_long][i_lat]
        latitud = self.dataset.variables['XLAT'][0][i_long][i_lat]
        return [longitud, latitud]

    # Devuelve en forma de diccionario los valores minimos y maximos
    # del las variables que se leen del fichero
    def min_max_values(self):
        data = dict()
        for key in self.data.keys():
            var_key = dict({key: {"min": np.amin(self.dataset[key]), "max": np.amax(self.dataset[key])}})
            data.update(var_key)
            del var_key
        return data

    def get_as_json(self, pvars, f="json", reshape=False, as_float_list=False):
        if f == "json":
            data = dict()
            for var in pvars:
                try:
                    value = np.array(self.dataset.variables[var][:])
                except:
                    value = self.__extra_vars__(var)

                if value.shape == (1, 183, 411):
                    value = value[0]

                if reshape:
                    value = value.reshape(-1, )

                if as_float_list:
                    value = [float(v) for v in value]

                var_key = dict({var: value})
                data.update(var_key)
                del var_key
        return data



