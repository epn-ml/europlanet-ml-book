# Introduction

This chapter is about the science case proposed by the Space Research Institute (IWF) of the Austrian Academy of Sciences, entitled "Detection and classification of ICMEs in in situ solar wind data".

The publication about this project can be found [here]( https://doi.org/10.1029/2022SW003149):

*  Rüdisser H.T., Windisch A., Amerstorfer U.V., Möstl C., Amerstorfer T., Bailey R.L., and Reiss M.A. (2022), Automatic detection of interplanetary coronal mass ejections in solar wind in situ data, Space Weather 20, e2022SW003149, doi:10.1029/2022SW003149.

## Description of the science case

In general, the term space weather describes disturbances of the near-Earth environment. Such disturbances can lead to failures of satellites affecting communication and navigation, increase the radiation affecting manned space flight and air traffic, and can lead to power outages. The scientific community tries to understand the processes that lead to intense disturbances of the Earth's magnetic field, so-called geomagnetic storms.

Coronal mass ejections (CMEs) are the dominant triggers of geomagnetic storms at the Sun. The interaction of CMEs with the Earth's magnetosphere that often causes strong geomagnetic storms. An interplanetary CME (ICME) is the whole in situ structure disturbing the quiet solar wind, i.e. the shock, sheath, solar wind pile-up, compression regions, magnetic field structure, driver gas, and ejecta wake.

One of the main problems when identifying ICMEs in in situ observations is the fact that not every ICME exhibits all of the aforementioned features: some have shocks and sheath regions, some don't; some show a clear rotation of the magnetic field and have a magnetic cloud, some don't; sometimes two CMEs interact during their propagation from the Sun to the Earth and then the signature can also look different; etc.

Another problem lies in the duration of the ICME signature. Roughly speaking, the average duration of an ICME lies around 21 hours, but there are ICMEs that last only 4 hours, and some that exhibit signatures for even more than 48 hours.

## Main aim

The main aim of this science case is to develop/implement an algorithm to automatically detect ICME signatures in in situ solar wind data.

Interplanetary coronal mass ejections (ICMEs) are one of the main drivers for space weather disturbances. In the past, different machine learning approaches have been used to automatically detect events in existing time series resulting from solar wind in situ data (e.g., Nguyen et al., 2019). However, classification, early detection and ultimately forecasting still remain challenging when faced with the large amount of data from different instruments. While CNNs are often used to discover objects or patterns in images or data series, there are two main problems when facing our specific task: high duration variability and a rather ambiguous definition of start and end time.


**Useful links and resources**

1. In situ solar wind data (only numbers in numpy structured arrays): https://doi.org/10.6084/m9.figshare.12058065.v7

2. The same in situ solar wind data as datetime objects in recarrays: https://doi.org/10.6084/m9.figshare.11973693.v7

3. Jupyther notebook for reading the data of (2) and from an ICME catalogue (first two code cells): https://github.com/cmoestl/heliocats/blob/master/cme_rate.ipynb

4. To install the conda environment to run the code for (3): https://github.com/cmoestl/heliocats/blob/master/README.md

5. The ICMECAT catalogue in different formats (see section below ICME CATALOGUE v2.0): https://helioforecast.space/icmecat

6. Solar wind forecast: https://helioforecast.space/solarwind

**Further literature:**

*  Luhmann J.G., Gopalswamy N., Jian L.K., and Lugaz N. (2020), ICME evolution in the inner heliosphere, Solar Phys. 295:61, doi:s11207-020-01624-0
*  Möstl C., Farrugia C.J., Temmer M., Miklenic C., Veronig A.M., Galvin A.B., Leitner M., and Biernat H.K. (2009), Linking Remote Imagery of a Coronal Mass Ejection to Its In Situ Signatures at 1 AU,
      Astrophys. J. Lett. 705, L180-L185, doi:10.1088/0004-637X/705/2/L180
*  Möstl C., Temmer M., Rollett T., Farrugia C.J., Liu Y., Veronig, A.M., Leitner M., Galvin, A.B., and Biernat H.K. (2010), STEREO and Wind observations of a fast ICME flank triggering a prolonged geomagnetic storm on 5-7 April 2010, Geophys. Res. Letters 37, L24103, doi:10.1029/2010GL045175
*  Richardson I.G. (2018), Solar wind stream interaction regions throughout the heliosphere, Living Reviews in Solar Physics 15, doi:10.1007/s41116-017-0011-z
*  Zurbuchen T.H. and Richardson I.G. (2006), In-Situ Solar Wind and Magnetic Field Signatures of Interplanetary Coronal Mass Ejections, Space Sci. Rec. 123, 31-43, doi:10.1007/s11214-006-9010-4
