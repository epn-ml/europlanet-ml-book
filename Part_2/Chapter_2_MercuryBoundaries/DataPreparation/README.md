# Data preparation

Link to prepared dataset:

https://zenodo.org/record/6417492#.YsQsK9JByEL


## Introduction
The goal of this project is to provide a framework for acquiring and pre-processing magnetic field data collected by the MESSENGER mission to Mercury in 2011-2015, and make this data suitable for analytical analysis and machine learning projects.

The original datasets and the accompanying metadata files are hosted by [NASA PDS PPI](https://pds-ppi.igpp.ucla.edu/search/view/?f=yes&id=pds://PPI/MESS-E_V_H_SW-MAG-4-SUMM-CALIBRATED-V1.0/DATA/MSO).

The following pre-processing steps are performed by the present project:
* Elimination of calibration signals. As a part of maintenance procedures, the MESSENGER magnetometer needed to be occasionally calibrated. However, the measurements of the magnetometer collected while a calibration signal was applied to it are still present in the original datasets. These signals are located and removed by us so that subsequent analysis is not biased by them.
* Enrichment with Mercury information. For a number of scientific purposes it may be useful to possess information not only on the magnetic field and the position of the spacecraft in the space around Mercury, but also information on the position of the planet around the Sun. We acquire this information from the [NASA Horizons](https://ssd.jpl.nasa.gov/horizons/) application and merge it with the main dataset.
* Restructurization. The original data files are split according to UTC-based day boundaries. However, for many scientific purposes it is preferable to possess data split according to orbit boundaries. We use MESSENGER orbit apoapsis points as markers to separate individual orbits. We also enumerate the orbits in the same manner as [Philpott et al., 2020](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019JA027544); this enumeration has some differences from the enumeration of orbits as calculated according to the orbital correction maneuver table.
* Enrichment with auxiliary information. To simplify subsequent analysis, we also include the estimated planetary dipole magnetic field contribution for each point, planetocentric distance of the spacecraft and several other items explained in detail further.


## Setting up
To initialize the workspace, simply run `bash setup.sh` in the project directory. This will initialize the Python virtual environment, download and unpack the magnetic field files, Mercury orbital information and magnetometer checkout information. 

## Usage
The main workload is performed by the `master.py` Python script. First, activate the Python virtual environment in the project's directory:
```bash
$ source venv/bin/activate
```
This will ensure that the dependencies installed during setup are available to it.
Now, simply run the main script as follows:
```bash
$ python3 master.py [RESOLUTION] [YEAR] [DOY_START] [DOY_END]
```

Here:
* `RESOLUTION` is the temporal resolution of the magnetometer data that you are interested in (valid options are 1, 5, 10, 60 seconds; default is 60)
* `YEAR` is the year to process (when not provided, process all years by default)
* `DOY_START` is the first day of the year to process (Jan.1st  by default)
* `DOY_END` is the last day of the year to process (Dec.31st by default)

## Data format description
* DATE 
* TIME_TAG: A derived value for the timetag associated with the center time of the averaging interval of the Bx,By,Bz samples in each record. The derived value is created by the following formula: `MET + 0.05 * delta_ts + (dt_sample)*(I-1) - latency`. MET is the mission elapsed time for the entire science packet. `delta_ts` is the delta time in seconds between the MET and the first sample in the downloaded science packet. `dt_sample` is the time between samples in seconds and given by `dt_sample = 1/sample_rate` where sample_rate is the reported sample rate in samples per second. `I` is the incremental counter for each data sample in the science packet. `I=1` is the first sample in the packet. `Latency` is the sample rate-dependent delay of the time stamp  recording relative to the actual time of observation.
* NAVG: Number of samples in averaging interval
* X_MSO: Average X position of MESSENGER in Mercury solar orbital (MSO) coordinates (km)
* Y_MSO: Average Y position of MESSENGER in Mercury solar orbital (MSO) coordinates (km)
* Z_MSO: Average Z position of MESSENGER in Mercury solar orbital (MSO) coordinates (km)
* BX_MSO: Average X axis magnetic field value in Mercury solar orbital (MSO) coordinates (nanoTesla)
* BY_MSO: Average Y axis magnetic field value in Mercury solar orbital (MSO) coordinates (nanoTesla)
* BZ_MSO: Average Z axis magnetic field value in Mercury solar orbital (MSO) coordinates (nanoTesla)
* DBX_MSO: Standard deviation of X axis magnetic field values in Mercury solar orbital (MSO) coordinates (nanoTesla)
* DBY_MSO: Standard deviation of Y axis magnetic field values in Mercury solar orbital (MSO) coordinates (nanoTesla)
* DBZ_MSO: Standard deviation of Z axis magnetic field values in Mercury solar orbital (MSO) coordinates (nanoTesla)
* RHO_DIPOLE: Radial distance of MESSENGER's position vector (km) wrt the position of the planetary magnetic dipole
* PHI_DIPOLE: Polar angle of MESSENGER's position vector (km)
* THETA_DIPOLE: Azimuthal angle of MESSENGER's position vector (km)
* BABS_DIPOLE: Magnitude of the estimated planetary dipole field (nanoTesla)
* BX_DIPOLE: X axis magnetic field value of the estimated planetary dipole field in Mercury solar orbital (MSO) coordinates (nanoTesla)
* BY_DIPOLE: Y axis magnetic field value of the estimated planetary dipole field in Mercury solar orbital (MSO) coordinates (nanoTesla)
* BZ_DIPOLE: Z axis magnetic field value of the estimated planetary dipole field in Mercury solar orbital (MSO) coordinates (nanoTesla)
* RHO: Planetocentric distance of MESSENGER (km)
* RXY: MESSENGER planetocentric distance projection magnitude onto the `XY` plane (km)
* X: X-component of Mercury's position vector (km)
* Y: Y-component of Mercury's position vector (km)
* Z: Z-component of Mercury's position vector (km)
* VX: X-component of Mercury's velocity vector (km/sec)                           
* VY: Y-component of Mercury's velocity vector (km/sec)                           
* VZ: Z-component of Mercury's velocity vector (km/sec) 
* VABS: Magnitude of Mercury's velocity vector (km/sec)
* D: Magnitude of Mercury's position vector (km)
* COSALPHA: `cos` of the angle between the MESSENGER orbital plane projection onto the `XY` plane and the `X` axis in Mercury solar orbital (MSO) coordinates
* EXTREMA: Flag value. `2` at the apoapsis of MESSENGER orbit; `-2` at the periapsis of MESSENGER orbit; `1` and `-1` at the extrema of MESSENGER planetocentric distance projection onto the `XY` plane, `0` otherwise.
* X_AB: Average X position of MESSENGER in aberrated Mercury solar orbital (MSO) coordinates in units of kilometers
* Y_AB: Average Y position of MESSENGER in aberrated Mercury solar orbital (MSO) coordinates in units of kilometers
* Z_AB: Average Z position of MESSENGER in aberrated Mercury solar orbital (MSO) coordinates in units of kilometers
* BX_AB: Average X axis magnetic field value in aberrated Mercury solar orbital (MSO) coordinates in units of nano-Tesla
* BY_AB: Average Y axis magnetic field value in aberrated Mercury solar orbital (MSO) coordinates in units of nano-Tesla
* BZ_AB: Average Z axis magnetic field value in aberrated Mercury solar orbital (MSO) coordinates in units of nano-Tesla
* DBX_AB: Standard deviation of X axis magnetic field values in aberrated Mercury solar orbital (MSO) coordinates and units of nano-Tesla
* DBY_AB: Standard deviation of Y axis magnetic field values in aberrated Mercury solar orbital (MSO) coordinates and units of nano-Tesla
* DBZ_AB: Standard deviation of Z axis magnetic field values in aberrated Mercury solar orbital (MSO) coordinates and units of nano-Tesla
* RHO_AB: `<ignore>`
* RXY_AB: `<ignore>`


## Reference frame and coordinate systems

The Mercury Solar Orbital (MSO) coordinate system centered at Mercury’s centre of mass, where the `+x` axis is pointing to the Sun, the `+y` axis is opposite to the orbital motion of Mercury and points toward dusk, and the `+z` axis is pointing to the north (normal to the `xy`-plane) and completes the right-handed coordinate system.

Mercury coordinates are specified as follows:
* Reference epoch: J2000.0
* X-Y plane: adopted Earth orbital plane at the reference epoch (Note: IAU76 obliquity of 84381.448 arcseconds wrt ICRF X-Y plane)
* X-axis   : ICRF
* Z-axis   : perpendicular to the X-Y plane in the directional (+ or -) sense of Earth's north pole at the reference epoch.
  
Mercury's position is calculated at the specified time points of the Barycentric Dynamical Time, or TDB. This continuous relativistic coordinate time is equivalent to the relativistic proper time of a clock at rest in a reference frame comoving with the solar system barycenter but outside the system's gravity well. It is the independent variable in the solar system relativistic equations of motion. TDB runs at a uniform rate of one SI second per second and is independent of irregularities in Earth's rotation.
  
The aberrated MSO coordinate system can be explained as follows. Since the magnetosphere's orientation responds to the general direction of the solar wind arrival, we may wish to account for the fact that the solar wind does not arrive directly along the `X` axis, since the planet's orbital velocity is non-negligible relative to the solar wind speed. Thus, if we multiply the unit vectors in the MSO coordinate system by a rotation matrix so that the solar wind arrives along the `X` axis, the resulting unit vectors will define the aberrated MSO system. While we make a very rough approximation and take solar wind velocity as a constant 350km/s, we take into account that Mercury's velocity varies widely over time due to its highly elliptical orbit.
