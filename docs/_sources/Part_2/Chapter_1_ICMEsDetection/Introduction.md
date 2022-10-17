# Introduction

This chapter is about the science case proposed by the Space Research Institute (IWF) of the Austrian Academy of Sciences, entitled "Detection and classification of ICMEs in in situ solar wind data".

The publication about this project can be found [here](https://doi.org/10.1029/2022SW003149):

*  Rüdisser H.T., Windisch A., Amerstorfer U.V., Möstl C., Amerstorfer T., Bailey R.L., and Reiss M.A. (2022), Automatic detection of interplanetary coronal mass ejections in solar wind in situ data, Space Weather 20, e2022SW003149, doi:10.1029/2022SW003149.

## Description of the science case

In general, the term space weather describes disturbances of the near-Earth environment. Such disturbances can lead to failures of satellites affecting communication and navigation, increase the radiation affecting manned space flight and air traffic, and can lead to power outages. The scientific community tries to understand the processes that lead to intense disturbances of the Earth's magnetic field, so-called geomagnetic storms.

Coronal mass ejections (CMEs) launched at the Sun are the dominant triggers of geomagnetic storms. CMEs are large plasma and magnetic field eruptions originating in the solar corona with speeds of several hundred up to thousands of kilometers per second. They occur from once a day at solar minimum to a couple of times per day at solar maximum. The interaction of CMEs with the Earth's magnetosphere often causes strong geomagnetic storms (see {numref}`sketchCMEMag`).

```{figure} ./images/cme_mag.png
---
height: 250px
name: sketchCMEMag
---
Sketch of a CME hitting Earth (not to scale). Left: CME with shock, sheath, magnetic flux rope (MFR), and the core. Right: near-Earth environment with bow shock, magnetosheath, magnetosphere and parts of the magnetotail (figure courtesy by T. Amerstorfer).
```

An interplanetary CME (ICME) is the whole in situ structure disturbing the quiet solar wind {cite:p}`rouillard2011`, i.e. the shock, sheath, solar wind pile-up, compression regions, magnetic field structure, driver gas, ejecta wake and/or legs of magnetic loops. Magnetic flux ropes (MFRs) are a subgroup of ejecta with specific properties, and magnetic clouds (MCs) again are a subgroup of MFRs. An MC has the following observed characteristic properties {cite:p}`burlaga1981`: Inside the MC (i) the magnetic field exhibits a smooth and large rotation, (ii) the plasma $\beta$ is lower than in the surrounding solar wind (i.e.~small plasma pressure and high magnetic field), (iii) the proton temperature is lower than in the solar wind. The magnetic field structure is the important part of an ICME regarding its geoeffectiveness.

One of the main problems when identifying ICMEs in in situ observations is the fact that not every ICME exhibits all of the aforementioned features: some have shocks and sheath regions, some don't; some show a clear rotation of the magnetic field and have a magnetic cloud, some don't; sometimes two CMEs interact during their propagation from the Sun to the Earth and then the signature can also look different; etc.

Another problem lies in the duration of the ICME signature. Roughly speaking, the average duration of an ICME lies around 21 hours, but there are ICMEs that last only 4 hours, and some that exhibit signatures for even more than 48 hours.

## Main aim

The main aim of this science case is to develop/implement an algorithm to automatically detect ICME signatures in in situ solar wind data.

Interplanetary coronal mass ejections (ICMEs) are one of the main drivers for space weather disturbances. In the past, different machine learning approaches have been used to automatically detect events in existing time series resulting from solar wind in situ data (e.g., Nguyen et al., 2019). However, classification, early detection and ultimately forecasting still remain challenging when faced with the large amount of data from different instruments. While CNNs are often used to discover objects or patterns in images or data series, there are two main problems when facing our specific task: high duration variability and a rather ambiguous definition of start and end time.

## Brief summary of our approach

The first step in this science case was the reimplementation of a model proposed by {cite:t}`nguyen2019`, which had previously been tested on WIND data and achieved a maximum recall and precision of around 84%.

After the reimplementation of this model, the model was tested on STEREO-A and STEREO-B data as well as on WIND data. All three contain less variables than the original data set used by Nguyen et al. At a similar recall as for the original set, the precision for all three datasets was only around 30% and the accuracy in delivering start and end times was limited.

The next step was to align all three data sets in order to process more training data for a combined model. It was tested on held out datasets for WIND, STEREO-A and STEREO-B. Surprisingly, this did not sufficiently improve performance and lead us to explore other approaches.

Starting from the reimplementation, a post processing step based on YOLO v5 (ultralytics) was investigated, in order to improve performance. Even though first results seemed promising, the idea was later discarded due to unsatisfactory results and the laborious pipeline. Since the ultimate goal is an explicit and widely applicable pipeline, it was decided to abandon the general approach of using multiple basic neural networks and the similarity measure used by {cite:t}`nguyen2019` completely and compose it as a segmentation problem instead.

We proposed a pipeline using a UNet {cite:p}`ronneberger2015` including residual blocks, squeeze and excitation blocks, Atrous Spatial Pyramidal Pooling (ASPP) and attention blocks, similar to the ResUNet++ {cite:p}`jha2019`, for the automatic detection of ICMEs. Comparing it to our first results, we find that our model outperforms the baseline regarding GPU usage, training time and robustness to missing features, thus making it more usable for other data sets, as well as the three aligned data sets. The relatively fast training allows straightforward tuning of hyperparameters. Our proposed pipeline can be used for any time series segmentation problem. The straightforward implementation allows a simple extension to a multi-class classification problem and paves the way to include corotating interaction regions into the range of detectable phenomena within our pipeline.

The pipeline is open source and can be found on [GitHub](https://github.com/epn-ml/IWF-ICMEs).

In the following, we present a tutorial for the pipeline, which can also be found on [GitHub](https://github.com/epn-ml/Tutorial_IWF-ICMEs).


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
