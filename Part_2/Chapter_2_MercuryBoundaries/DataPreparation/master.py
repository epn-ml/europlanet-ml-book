#!/usr/bin/env python3
from scipy.signal import argrelextrema, find_peaks
from sys import argv
import os, os.path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from io import StringIO
from sys import argv, exit

from scipy.optimize import curve_fit

import matplotlib as mp
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
mp.rcParams['font.size'] = 22
mp.rcParams['axes.labelsize'] = 32
mp.rcParams['figure.figsize'] = (15, 10)
plt.style.use('fivethirtyeight')
mp.rcParams['font.size'] = 22
mp.rcParams['axes.labelsize'] = 32
mp.rcParams['figure.figsize'] = (15, 10)

planet = {
    "Mercury": {
        "R": 2440,
        "M0": -1.96e02,  # xR**3
        "x0": 0,
        "y0": 0,
        "z0": 484
    }
}

R_M = 2440  # km
M_0 = -1.96e02 * R_M ** 3  # nT. Alexeev, Belenkaya et al 2010 doi:10.1016/j.icarus.2010.01.024
z_displacement = 484

broken_orbit_indices = [1587, 1589, 1590, 3565, 3686, 26, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 789, 957, 1033, 1740, 3732]
orbit_index_offset = 12



class DataMaster:
    def __init__(self):
        self.mag_data = None
        self.resolution = -1

    def load_data(self, resolution=60, year=None, mindoy=None, maxdoy=None):
        pass

    def prepare_data(self):
        pass


class MessengerMaster(DataMaster):
    def __init__(self):
        # Manually chosen after careful examination of the resulting plot
        super().__init__()
        self.outlier_threshold = 550  # nT
        self.checkout = None
        self.mercury_se = None

    @staticmethod
    def load_messenger_data(resolution, year=None, mindoy=None, maxdoy=None):
        if resolution not in [1, 5, 10, 60]:
            print("Resolution not available, using 60sec averages")
            resolution = 60

        columns = [
            'YEAR', 'DAY_OF_YEAR', 'HOUR', 'MINUTE', 'SECOND',
            'TIME_TAG', 'NAVG', 'X_MSO', 'Y_MSO', 'Z_MSO', 'BX_MSO',
            'BY_MSO', 'BZ_MSO', 'DBX_MSO', 'DBY_MSO', 'DBZ_MSO'
        ]

        data_files = []
        path = os.path.join('full', "%02d" % resolution)
        for file in sorted(os.listdir(path)):
            if not file.endswith("TAB"):
                continue
            if year is None or file.startswith("MAGMSOSCIAVG" + str(year % 2000)):
                xyear = file[12:14]
                doy = int(file.split("_")[0].replace("MAGMSOSCIAVG" + xyear, ""), 10)
                if (mindoy is None or doy >= mindoy) and (maxdoy is None or doy <= maxdoy):
                    data_files.append(pd.read_table(os.path.join(path, file),
                                                    delim_whitespace=True,
                                                    header=None,
                                                    names=columns,
                                                    parse_dates={"DATE": ['YEAR', 'DAY_OF_YEAR', 'HOUR', 'MINUTE', 'SECOND']},
                                                    date_parser=lambda year, day_of_year, hour, minute, second: datetime.strptime(f"{year}-{day_of_year}_{hour}:{minute}:{second}", "%Y-%j_%H:%M:%S.000")))
        print("Loaded", datetime.now())
        data = pd.concat(data_files, ignore_index=True)
        print("Concat", datetime.now())
        data.drop_duplicates(inplace=True)
        print("dedupped", datetime.now())
        data = data.set_index('DATE')
        print("indexed", datetime.now())
        data.sort_index(inplace=True)
        print("sorted", datetime.now())
        print(data)
        return data

    @staticmethod
    def load_checkout_dates(filename, first, last):
        res = []
        for l in open(filename).readlines():
            start, end = l[0:9], l[-15:-6]
            start = datetime.strptime(start + "-00:00:00", '%d%b%Y-%H:%M:%S')
            end = datetime.strptime(end + "-23:59:59", '%d%b%Y-%H:%M:%S')
            if (end > first and start < last) or (start < last and start > first):
                res.append((start, end))
        return res

    @staticmethod
    def load_mercury_horizons(resolution=60, year=None, mindoy=None, maxdoy=None):
        dateparse = lambda x: datetime.strptime(x, '%Y-%b-%dZ%H:%M:%S.0000')
        data = pd.read_table("mercury-pos-min.txt", delim_whitespace=True, engine='python', parse_dates=[0],
                             date_parser=dateparse)
        data.columns = ["DATE", "X", "Y", "Z", "VX", "VY", "VZ"]
        data = data.set_index('DATE')

        if year is not None:
            data = data[data.index.year == year]
        if mindoy is not None:
            data = data[data.index.dayofyear >= mindoy]
        if maxdoy is not None:
            data = data[data.index.dayofyear <= maxdoy]
            # These are not true interpolations, we just fill out one resolution
            # bin's worth of the same value for correct merging
        interpolations = []
        if resolution < 60:
            stuff_secs = range(0, 60, resolution)
            for i in stuff_secs:
                tmpdata = data.copy(True)
                tmpdata["VZ"] += 0.0001 * np.random.random()
                tmpdata.index = tmpdata.index + pd.DateOffset(seconds=i)
                interpolations.append(tmpdata)
            data = pd.concat(interpolations)

        data['VABS'] = np.sqrt(data.VX ** 2 + data.VY ** 2 + data.VZ ** 2)
        data['D'] = np.sqrt(data.X ** 2 + data.Y ** 2 + data.Z ** 2)
        data.drop_duplicates(inplace=True)
        data.sort_index(inplace=True)
        print(data)
        return data

    def load_data(self, resolution=60, year=None, mindoy=None, maxdoy=None):
        self.resolution = resolution
        self.mag_data = self.load_messenger_data(resolution, year, mindoy, maxdoy)
        print("mag_data done", datetime.now())
        self.checkout = self.load_checkout_dates('checkout.dat', self.mag_data.index[0], self.mag_data.index[-1])
        print("checkout done", datetime.now())
        self.mercury_se = self.load_mercury_horizons(resolution, year, mindoy, maxdoy)
        print("mercury_se done", datetime.now())

    def filter_checkouts(self, data, checkout):
        payload_columns = ["BX_MSO", "BY_MSO", "BZ_MSO"]
        for c in checkout:
            outlier_indices = np.where(
                data.loc[c[0]:c[1]]['BX_MSO'] ** 2 + data.loc[c[0]:c[1]]['BY_MSO'] ** 2 + data.loc[c[0]:c[1]][
                    'BZ_MSO'] ** 2 > self.outlier_threshold ** 2)[0]
            for i in outlier_indices:
                iprev, inext, i = data.loc[c[0]:c[1]].index[i - 1], data.loc[c[0]:c[1]].index[i + 1], \
                                  data.loc[c[0]:c[1]].index[i]
                for col in payload_columns:
                    for j in [iprev, i, inext]:
                        data.at[j, col] = np.nan

    def insert_gaps(self, data):
        payload_columns = ["X_MSO", "Y_MSO", "Z_MSO", "BX_MSO", "BY_MSO", "BZ_MSO"]
        default_delta = np.timedelta64(self.resolution * 10 ** 9, 'ns')  # 1 minute
        gap_indices = np.where(np.diff(data.index) > default_delta)[0]
        for i in gap_indices:
            for c in payload_columns:
                data.iat[i, data.columns.get_loc(c)] = np.nan

    def dipole_field(self, data):
        x, y, z = data.X_MSO, data.Y_MSO, (data.Z_MSO - z_displacement)
        data["RHO_DIPOLE"] = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        data["PHI_DIPOLE"] = np.arctan(y / x)
        data["THETA_DIPOLE"] = np.arcsin(z / data.RHO_DIPOLE)
        data["BABS_DIPOLE"] = np.abs(M_0) / data.RHO_DIPOLE ** 4 * np.sqrt(3 * z ** 2 + data.RHO_DIPOLE ** 2)
        psi = 0.0
        p = z * np.cos(psi) - x * np.sin(psi)
        Br = M_0 / data["RHO_DIPOLE"] ** 5
        data["BX_DIPOLE"] = -Br * (- data["RHO_DIPOLE"] ** 2 * np.sin(psi) - 3. * x * p)
        data["BY_DIPOLE"] = Br * (3. * y * p)
        data["BZ_DIPOLE"] = -Br * (data["RHO_DIPOLE"] ** 2 * np.cos(psi) - 3. * z * p)

    def distances(self, data):
        data['RHO'] = np.sqrt((data.X_MSO ** 2 + data.Y_MSO ** 2 + data.Z_MSO ** 2))
        data['RXY'] = np.sqrt((data.X_MSO ** 2 + data.Y_MSO ** 2))

    def aberration(self, data):
        # The distribution of solar wind speeds during solar minimum: Calibration for numerical solar wind
        # modeling constraints on the source of the slow solar wind
        # S. L. McGregor  W. J. Hughes  C. N. Arge  M. J. Owens  D. Odstrcil
        # https://doi.org/10.1029/2010JA015881

        sw_velocity = 350  # km/s

        # TODO: this is a crude approximation; investigate ways to improve it

        def rotation_matrix(theta):
            c, s = np.cos(theta.values), np.sin(theta.values)
            np.ndarray(shape=(c.shape[0], 3, 3), dtype=float, order='F')
            R = np.vstack([[c, -s, [0] * c.shape[0]],
                           [s, c, [0] * c.shape[0]],
                           [[0] * c.shape[0], [0] * c.shape[0], [1] * c.shape[0]]
                           ])
            return R

        data.ABERRATION_ANGLE = - np.arctan2(data.VABS, sw_velocity)

        data_size = data.shape[0]
        rot = rotation_matrix(data.ABERRATION_ANGLE[:data_size]).reshape(3, 3, data_size).transpose(2, 0, 1)

        triads = [
            ['X_MSO', 'Y_MSO', 'Z_MSO'],
            ['BX_MSO', 'BY_MSO', 'BZ_MSO'],
            ['DBX_MSO', 'DBY_MSO', 'DBZ_MSO']
        ]

        for t in triads:
            vec = np.array([data[t].values[:data_size]]).transpose(0, 2, 1)
            resx = np.matmul(rot, vec.T).reshape(data_size, 3)
            for i in range(len(t)):
                data[(t[i].split("_")[0] + "_AB")] = resx.T[i]

        data['RHO_AB'] = np.sqrt((data.X_AB ** 2 + data.Y_AB ** 2 + data.Z_AB ** 2))
        data['RXY_AB'] = np.sqrt((data.X_AB ** 2 + data.Y_AB ** 2))

    def find_extrema(self, data):
        extrema = pd.DataFrame(index=data.index)
        extrema['TYPE'] = 0
        x, y, z, rho, rxy = 'X_MSO', 'Y_MSO', 'Z_MSO', 'RHO', 'RXY'

        apoapsis = find_peaks(data[rho].values[~np.isnan(data[rho].values)].round(0))[0]
        periapsis = find_peaks(1 / data[rho].values[~np.isnan(data[rho].values)].round(0))[0]

        xy_edges = find_peaks(data[rxy].round(0).values[~np.isnan(data[rxy].values)])[0]

        if xy_edges[0] < periapsis[0] and xy_edges[1] > periapsis[0]:
            xy_edges = xy_edges[1:]
        xy1, xy2 = xy_edges[1::2], xy_edges[0::2]

        extrema.iloc[xy1] = 1
        extrema.iloc[xy2] = -1
        extrema.iloc[apoapsis] = 2
        extrema.iloc[periapsis] = -2

        cosine_array = pd.DataFrame(index=data.index)
        cosine_array['VALUE'] = np.nan

        size = np.min([len(data[x].iloc[xy1].values), len(data[x].iloc[xy2].values)])

        dx = np.abs(data[x].iloc[xy1].values[:size] - data[x].iloc[xy2].values[:size])
        dx *= np.sign(data[x].iloc[xy1].values[:size] - data[x].iloc[xy2].values[:size])
        dy = data[y].iloc[xy1].values[:size] - data[y].iloc[xy2].values[:size]
        cosine = np.cos(np.arctan2(dy, dx))

        max_delta_cosine = 0.06  # Empirically chosen to cut off rogue data points
        cosine_diff = np.abs(np.diff(np.abs(cosine)))
        cosine[np.append(cosine_diff > max_delta_cosine, False)] = np.nan

        i_from, i_to = extrema.iloc[periapsis].index, extrema.iloc[periapsis].index[1:]
        try:
            for i in range(min(len(i_from), len(i_to))):
                cosine_array.loc[i_from[i]: i_to[i]]['VALUE'] = cosine[i]
        except:
            print(i, len(i_from), len(i_to), len(cosine))
        cosine_array.loc[i_to[-1]:]['VALUE'] = cosine[-1]
        return extrema, cosine_array


#- orbit files 12 thru 960 should each have an ID one less
#- orbit files 3578 thru 3697 should each have an ID one less
#- orbit files 3699 thru 4105 should each have an ID two less

    def save_orbits(self, data):
        mask = data[data.EXTREMA == 2].index
        i = 0
        for bounds in zip(mask[:-1], mask[1:]):
            i += 1
            diff = bounds[1] - bounds[0]
            if bounds[0] < pd.Timestamp(datetime(2012, 4, 8)):
                period = timedelta(hours=13)  # +1 hr for error tolerance
            else:
                period = timedelta(hours=9)
            while diff > timedelta(hours=12, minutes=30):  # +1 hr for error tolerance
                diff -= period
                i += 1
                print(diff, bounds)
            xdata = data[bounds[0]:bounds[1]]
            if i not in broken_orbit_indices:
                j = i + orbit_index_offset
                if j >= 12 and j <= 960:
                  j -= 1
                elif j >= 3578 and j <= 3697:
                  j -= 1
                elif j >= 3699:
                  j -= 2
                xdata.to_csv(os.path.join("orbit", "messenger-{:04d}.csv".format(j)))
                print("Orbit #{} complete".format(j))
            else:
                print("Orbit #{} complete".format(j))

    def prepare_data(self):
        self.mag_data = self.mag_data.groupby(level=0).last()
        self.insert_gaps(self.mag_data)
        print("insert_gaps done", datetime.now())
        self.filter_checkouts(self.mag_data, self.checkout)
        print("filter_checkouts done", datetime.now())
        self.dipole_field(self.mag_data)
        print("dipole_field done", datetime.now())
        self.distances(self.mag_data)
        print("distances done", datetime.now())
        self.mag_data = pd.concat([self.mag_data, self.mercury_se], axis=1, join='inner')
        del self.mercury_se
        print("concat done", datetime.now())
        extrema, cosalpha = self.find_extrema(self.mag_data)
        self.mag_data["COSALPHA"] = cosalpha
        self.mag_data["EXTREMA"] = extrema
        self.aberration(self.mag_data)
        self.save_orbits(self.mag_data)


if len(argv) > 1:
    resolution = int(argv[1])
else:
    resolution = 60

if len(argv) > 2:
    year = int(argv[2])
else:
    year = None

if len(argv) > 3:
    doy_start = int(argv[3])
else:
    doy_start = None

if len(argv) > 4:
    doy_end = int(argv[4])
else:
    doy_end = None

messenger_master = MessengerMaster()
messenger_master.load_data(resolution, year, doy_start, doy_end)
messenger_master.prepare_data()


class MessengerIllustrator:
    def checkout_magnitude_distro(self, data, checkout):
        bms = []
        for c in checkout:
            bms.append(np.array(np.sqrt(
                data.loc[c[0]: c[1]]['BX_MSO'] ** 2 +
                data.loc[c[0]: c[1]]['BY_MSO'] ** 2 +
                data.loc[c[0]: c[1]]['BZ_MSO'] ** 2)
            ))
            bmx = bms[-1][~np.isnan(bms[-1])]
        if len(bms) > 0:
            bm = np.concatenate(bms)
            bm = bm[~np.isnan(bm)]
        else:
            bm = np.array([])
        plt.hist(bm, 100, log=True)
        plt.xlabel('$|B|$')
        plt.ylabel('$\log\,N$')


    def orbital_dynamics(self, data):
        max_alt, min_alt = data.RHO.iloc[argrelextrema(data.RHO.values, np.greater)], data.RHO.iloc[
            argrelextrema(data.RHO.values, np.less)]
        plt.xlabel("Date")
        plt.figure(1).autofmt_xdate()
        plt.ylabel("Altitude [km]")
        plt.plot(max_alt, label='Apoapsis altitude')
        plt.plot(min_alt, label='Periapsis altitude')
        plt.legend()


    def mercury_orbit_hgi(self, data):
        start = 0
        stop = 88 + 1  # 88 = Hermean year duration

        au = data["AU"][start:stop]
        hgi_lon = data["HGI_LON"][start:stop] * np.pi / 180
        hgi_lat = (90 - data["HG_LAT"][start:stop]) * np.pi / 180
        hgi_x, hgi_y, hgi_z = au * np.cos(hgi_lon) * np.sin(hgi_lat), au * np.sin(hgi_lon) * np.sin(
            hgi_lat), au * np.cos(hgi_lat)

        ax = plt.subplot()
        ax.plot(hgi_x, hgi_y)
        ax.scatter(0, 0, color='r', s=240)  # Position of the Sun
        plt.xlabel("HGI X [а.е.]")
        plt.ylabel("HGI Y [а.е.]")
        ax.set_aspect('equal', adjustable='box')

        ax = plt.subplot()
        ax.plot(hgi_x, hgi_z)
        ax.scatter(0, 0, color='r', s=240)  # Position of the Sun
        plt.xlabel("HGI X [а.е.]")
        plt.ylabel("HGI Z [а.е.]")
        ax.set_aspect('equal', adjustable='box')


    def zjumps(self, data):
        data['DELTA_BZ'] = np.append(np.abs(np.diff(data.BZ_MSO)), np.nan)
        plt.xlabel(r"$dB_Z$ [нТл]")
        plt.ylabel(r"$\log\,N$")
        plt.hist(data[data['DELTA_BZ'] < 100].DELTA_BZ, log=True, bins=100, normed=False);

        zjumps = data[(data['DELTA_BZ'] > 38) & (data['DELTA_BZ'] < 42) & (np.abs(data["RXY"] / R_M > 1.0))]
        zj = zjumps[(np.abs(zjumps['Z_MSO']) / R_M < 1.0)]
        print(zj.shape)
        plt.scatter(zj.X_MSO / R_M, zj.Y_MSO / R_M, color='r')
        plt.scatter(0, 0, s=R_M * 11, edgecolor='k', linewidth=2, zorder=0)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel(r"$X_{MSO}\,[R_M$]")
        plt.ylabel(r"$Y_{MSO}\,[R_M$]")

        zj = zjumps[(zjumps['Z_MSO'] / R_M < 0.1 + z_displacement / R_M) &
                    ((zjumps['Z_MSO'] / R_M > -0.1 + z_displacement / R_M))]
        print(zj.shape)
        plt.scatter(zj.X_MSO / R_M, zj.Y_MSO / R_M, color='r')
        plt.scatter(0, 0, s=R_M * 18, edgecolor='k', linewidth=2, zorder=0)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel(r"$X_{MSM}\,[R_M$]")
        plt.ylabel(r"$Y_{MSM}\,[R_M$]")

        zj = data[(data['DELTA_BZ'] > 38) & (data['DELTA_BZ'] < 42) & (np.abs(data['Y_MSO']) < R_M)]
        print(zj.shape)
        plt.scatter(zj.X_MSO / R_M, zj.Z_MSO / R_M, color='g', s=3)  # , color='r')
        plt.scatter(0, 0, s=R_M * 7, edgecolor='k', zorder=0)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel(r"$X_{MSO}\,[R_M$]")
        plt.ylabel(r"$Z_{MSO}\,[R_M$]")


    def show_paraboloid(self, zj, target_phase):
        R1, gamma = 1., 1.

        def func_paraboloid(rho, R1, s):
            # s = 1
            # res = R1 - (s**2 + 1)/(2*R1)*rho**2
            # res = R1 - (gamma*2 + 1)/(4*R1)*rho**2     # Winslow
            res = R1 - (s ** 2 + 1) / (4 * R1) * rho ** 2  # Winslow
            if R1 < 1.0:
                res = [-9999] * res.shape[0]
            return res

        cos_spread = 0.3  # 134 # 30 degrees either way
        zj = zj[np.abs(target_phase - zj.COSALPHA) < cos_spread]

        # Only approximately true in this coord system
        target_phase *= np.pi / 180
        zj = zj[np.abs(np.arctan2(zj.Y, zj.X) - target_phase) < 0.6]

        rho = np.sqrt(zj.Y_MSO ** 2 + (zj.Z_MSO - z_displacement) ** 2) / R_M

        # if False:
        rho = rho[zj.X_MSO > 0]
        zj = zj[zj.X_MSO > 0]

        zjt = zj.copy(deep=True)
        zj = zj[~((zjt.X_MSO / R_M < 0) & (rho < 2.0))]
        rho = rho[~((zjt.X_MSO / R_M < 0) & (rho < 2.0))]

        zjt = zj.copy(deep=True)
        zj = zj[~((zjt.X_MSO / R_M > 1) & (rho > 2.0))]
        rho = rho[~((zjt.X_MSO / R_M > 1) & (rho > 2.0))]

        zj = zj[rho < 2.5]
        rho = rho[rho < 2.5]

        zj = zj[zjt.X_MSO / R_M < 2.5]
        rho = rho[zjt.X_MSO / R_M < 2.5]

        popt, pcov = curve_fit(func_paraboloid, rho, zj.X_MSO.values / R_M, bounds=((-np.inf, 0), (np.inf, np.inf)))
        D, dD = np.mean(zj.D / 149597871), np.std(zj.D / 149597871)
        print(popt)
        plt.scatter(zj.X_MSO / R_M, rho, marker="X", label=r"$D=%.2f\pm%.3fAU$" % (D, dD))
        xxx = np.arange(0, plt.ylim()[1] * 0.8, 0.05)
        plt.plot(func_paraboloid(xxx, *popt), xxx)
        plt.scatter(0, 0, s=R_M * 12, edgecolor='k', zorder=0, color='y')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.legend()
        plt.xlabel(r"$X_{MSO}\,[R_M$]")
        plt.ylabel(r"$r\,[R_M$]")
        return zj
