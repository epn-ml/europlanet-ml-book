# Introduction

This chapter is about the science case proposed "Search for magnetopause/shockwave crossings on Mercury based on MESSENGER data", proposed by the Moscow State University (SINP/LMSU).

The publication about this project can be found [here](https://2022.ecmlpkdd.org/wp-content/uploads/2022/09/sub_1177.pdf):

*  Julka S., Kirschstein N., Granitzer M., Lavrukhin A., and Amerstorfer U. (2022), Deep Active Learning for Detection of Mercury’s
Bow Shock and Magnetopause Crossings, Proceedings ECMl PKDD 2022.

Our ML pipeline is open source and can be found on [GitHub](https://github.com/epn-ml/Freddie).

In the following, we present a tutorial for the pipeline, which can also be found on [GitHub](https://github.com/epn-ml/EPSC2021-MercuryBoundaries-workshop).

## Description of the science case

The interplanetary medium is filled with the solar wind and the interplanetary magnetic field (IMF). When the supersonic solar wind plasma flow finds an obstacle on its way out, such as a magnetosphere, a shock wave arises upstream of the obstacle. In case of a magnetospheric interaction it is called the bow shock. The bow shock slows the solar wind to subsonic speeds, so that the solar wind can flow around the magnetopause, which is the surface enclosing the magnetosphere. The magnetosphere is the region, where the inner planetary magnetic field plays the main role.

The magnetopause boundary is determined by the equation of balance of the magnetic field and plasma pressure sum inside and outside of the magnetopause:

IMF pressure + solar wind plasma pressure = planetary and magnetospheric magnetic field pressure + magnetospheric plasma pressure

In the case of Mercury, in front of the magnetopause the solar wind ram pressure, and inside it the magnetospheric magnetic field pressure play the main roles. Mercury's weak internal magnetic field, combined with its proximity to the Sun, means that the magnetosphere of the innermost planet is small and highly dynamic. Specifically, the magnetopause subsolar standoff distance is estimated to be 1.4 – 1.6 RM, where RM is the radius of Mercury. Sometimes, during a high-density plasma flow, the magnetopause can appear closer to the Hermean surface, or even disappear. The bow shock changes its shape and stands closer or farther from the planet in response to variations in the solar wind speed and, to a lesser extent, IMF direction. The magnetopause location and shape are determined principally by the pressure exerted on the magnetopause by the shocked solar wind plasma, which scales with the solar wind ram pressure, balanced by the magnetospheric magnetic ﬁeld pressure.


## Main aim

The MESSENGER (MErcury Surface, Space ENvironment, GEochemistry, and Ranging) spacecraft has completed over 4000 orbits around Mercury. The initial orbit had a 200 km periapsis altitude, 82.5 inclination, 15300 km apoapsis altitude, and 12 h period. The MESSENGER’s orbit around Mercury was approximately ﬁxed in inertial space so that the orbit completes a local time rotation once every Mercury year (88 Earth days). The periapsis altitude and latitude of the orbit also drifted during every Mercury year, and the MESSENGER orbit varied between two extremes, the dawn-dusk terminator and noon-midnight orbits.

During each orbit, MESSENGER typically spent 1–2 h inside the magnetosphere; the rest of the time was spent in the magnetosheath and in the interplanetary medium. The interplanetary magnetic field (IMF) magnitude assigned to each crossing can be evaluated as a 1 hour average of magnetometer (MAG) data upstream of the outermost bow shock encounter.

Magnetic ﬁeld data are analyzed in Mercury solar orbital (MSO) coordinates. In MSO coordinates, X_MSO is positive sunward, Z_MSO is positive northward, Y_MSO is positive duskward and completes the right-handed system, and the origin is at the center of the planet.

The goal of this case is to improve our understanding of Mercury's magnetosphere and its dynamics. We utilise the data recorded by the MESSENGER spacecraft, which collected vast amounts of heterogeneous data during its approximately 4000 orbit voyage, most interestingly the magnetic field data from the magnetometer. A typical orbit involved passing from the interplanetary magnetic field through the bow shock, the magnetosheath, the magnetopause, the magnetosphere of Mercury, and thereupon the same sequence in reverse. Since a mercurial year is about 88 Earth days, several years' worth of magnetometer data was recorded. This is nice because several variations in environmental configurations are recorded, which is useful to build automatic models for event recognition. The resulting data set of crossing times and positions is to be used in conjunction with the paraboloid magnetosphere model to compute the magnetic field lines in the magnetosphere; these can subsequently be used to perform modelling of trajectories of particles sputtered from the surface of the planet by space radiation.


## Brief summary of our approach

Based on data from the mission, several global models of the magnetosphere were proposed {cite:p}`johnson2012,winslow2013,zhong2015,philpott2020`. However, they could only describe an average shape of the bow shock and magnetopause crossings and can be prone to missing the statistical nuances in the data.  Given large data, Neural Networks can be expected to approximate complex functions, which often surpass deterministic and rule-based methods, in a variety of time series tasks like classification {cite:p}`ismail2019`, time series forecasting {cite:p}`lim2021` and rare time series event detection {cite:p}`nguyenvq2018`. We leverage these to develop a predictor, that can be used in real-time during orbit, to predict magnetic region for each step in a short window of observation. Figure 2 illustrates the different crossing labels for an exemplary orbit.

The use of statistical neural networks allows us to explore another aspect: with the help of active learning, it is possible to add samples to the training process incrementally. With this, we can examine how the model scales its predictive capacity with increasing data, and thus study how the variations such as changing solar wind and environmental conditions affects the manifestation of boundary signatures. To begin with, different orbits can be expected to have some element of similarity in the magnetic field structure, yet would have large variations in the same segments at different conditions. It is also interesting to study what the minimal amount is for the data needed to be able to generalise these phenomena for future missions such as the BepiColombo.

### Dataset

The dataset was manually labelled with the boundary crossings. To identify bow shocks, we first subtracted planetary dipole magnetic field components from the magnetometer measurements, computed the magnitude of the remainder attributed to external sources, applied the Savitzky-Golay filter to smooth the time profile of the remainder and computed its second derivative. The first and the last second derivative spikes as determined by z-score are assumed to be the enter and exit bow shock crossings respectively. Magnetopause boundaries were eyeballed using the cartesian components of the magnetic fields in the Mercury Solar Orbital coordinate system. During magnetopause crossings at least one of the components in the magnetogram experiences a sharp growth; the exact component depends on the spacecraft position. The beginning and ending points of this growth region are assumed to determine the magnetopause crossing edges. To supplement these, we also used the boundaries marked by {cite:t}`philpott2020` for a few orbits.

The distribution of the different magnetic regions, after annotation, is reported in the table below. The boundaries of critical interest- Bow-shock and Magnetopause are minorities with only 3.7 and 2.3 % representation. The table highlights the data imbalance issue that requires investigating special techniques to ensure the predictor does not bias towards the overrepresented classes.


| Label | Region                        | Statistical distribution (%)  |
| ----- |-------------------------------| -----|
| 0     | Interplanetary magnetic field | 65.4 |
| 1     | Bow shock crossing            |  3.7 |
| 2     | Magnetosheath                 | 14.5 |
| 3     | Magnetopause crossing         |  2.3 |
| 4     | Magnetosphere                 | 14.1 |



### Pre-processing

As a first step in pre-processing, feature selection was performed to assess the contribution of available features in the estimation of the output. Based on statistical correlations, the Magnetic Flux features (BX_MSO. BY_MSO, BZ_MSO), Aircraft position coordinates (X_MSO, Y_MSO, Z_MSO) and planetary velocity components (VX, VY, VZ) were found to be most informative. In addition, three meta features namely EXTREMA, COSALPHA and RHO_DIPOLE were selected.

In the feature preparation stage, a sliding window of variable sizes (3 seconds to 3 minutes) with a hop size of 1 second was computed on the time series signal to obtain feature vectors. Finally, the features were normalised to have mean of 0 and a standard deviation of 1. No other pre-processing, or engineering was applied in order to allow the deep learning model to engineer features implicitly.

The windowed features are fed first into a block of 3 Convolutional layers with 1D filters, each followed by Batch Normalisation and ReLu activations. The activations obtained at the end of the CNN block are then passed to the Recurrent block with two layers of LSTMs. The final activations are then passed to a fully connected layer with softmax activations. The objective function used for training is Categorial cross entropy, with Adam optimizer.

The window size used in these experiments is 30 seconds. Overall, the predictor achieves a macro F1 score of about 80% on the bow shock and the magnetopause crossings on a randomly sampled test of 300 orbits. None of the orbits overlap in the train and test sets.


