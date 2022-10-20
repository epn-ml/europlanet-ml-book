# Introduction

This chapter is about the science case proposed "Automatic detection and classification of mounds on Mars", proposed by the GMAP work package of Europlanet 2024 RI.

In the following, we present a tutorial for our ML pipeline, which can also be found on [GitHub](https://github.com/epn-ml/Workshop-GMAP).

## Description of the science case

The GMAP Mounds identification science case aims to develop a generalised machine learning pipeline for the localisation and characterisation of specific geomorphological features (mounds) that are present on the surface of Mars. Mounds are positive relief features that can be ascribed to a variety of phenomena {cite:p}`detoffoli2019`. They can be related to monogenic edifices due to spring or mud volcanism, rootless cones on top of lava flows, pingos and so on. The focus of the investigation is related to the sedimentary/spring case of mud extrusion or sulphate oversaturated fluids. These objects are usually widespread regionally and/or contained in large complex craters (i.e., tens of km in diameter) often in populations of several hundred/thousands. Previously, automatic detections were performed in some of these cases {cite:p}`pozzobon2019` using topographic data in limited areas (i.e., Digital Terrain Models (DTMs) as rasters whose cells represent height values) in order to discriminate these objects in terms of pre-trained morphometric parameters and map them. Due to the scarcity of high-resolution DTMs and poor area coverage, the ML WP challenge is to reach the ability to detect such mound features by using simple grayscale panchromatic images at mid-high resolution with no need of topographic information.


## Dataset

The data is obtained from the Mars Reconaissance Orbiter (MRO) mission. The MRO spacecraft is designed to study the geology and climate of Mars, provide reconnaissance of future landing sites, and relay data from surface missions back to Earth. The data was collected by the High Resolution Imaging Science Experiment, also known as HIRISE. HiRISE is the most powerful camera ever sent to another planet, one of six instruments on board the MRO. The data is in the format of Digital Elevation Model (DEM). Detailed description of the data can be found on the University of Arizona HiRISE website.


