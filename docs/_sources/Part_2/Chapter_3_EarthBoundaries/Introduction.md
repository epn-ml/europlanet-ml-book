# Introduction

This chapter is about the science case proposed "Search for space plasmas boundary crossings", proposed by the Institute of Atmospheric Physics of Czech Academy of Sciences (IAP-CAS).

## Description of the science case

Planetary magnetospheres create multiple sharp boundaries, such as the bow shock, where the solar wind plasma is decelerated and compressed, or the magnetopause, a transition between solar wind field and planetary field.

The main objective is to develop an ML-based tool to identify crossings of space plasma boundaries such as the bow shock or magnetopause by a scientific spacecraft from the measured data. This work will consequently allow the identification of magnetospheric regions (foreshock, magnetosheath, and magnetosphere itself) from the spacecraft data, allowing for easier automatic data analysis and processing.  As a basis for the identification, we will use electromagnetic spectrogram and time-series data as well as particle spectra. A boundary crossing is visually recognized by sudden changes in plasma parameters, e.g., magnetic field or plasma velocity distribution moments. The identification is frequently made by a trained person tagging a time of crossing. Thus, existing large datasets of magnetopause and bow-shock crossings from spacecraft missions at the Earth are available and can be used to train the ML methods.

The resulting tool will be helpful in the scanning of large datasets (such as the Cluster or THEMIS data spanning two decades of continuous measurements) for plasma regions and their boundaries, required when extracting subsets of the data for statistical analysis of various plasma phenomena and their dependencies on the parameter regime. Another promising use is to employ this technique to identify the precise times of crossing of the same discontinuity by multiple spacecraft, which allows for triangulation and timing analysis to derive the orientation and velocity of the boundaries.

The developed tool can be trained on rich datasets from the terrestrial magnetosphere and later applied to more rare and exotic data from other solar system planets.

## Dataset

We will use a unique dataset of bow shock crossings encountered by the Cluster spacecraft over its 20 years of operation in the project. The training dataset includes 1941 bow shock crossings identified by visual inspection in magnetic field measurements from Cluster 2 between 2001 and 2013. The collection of shock crossing is a basis of a publication [Kruparova et al., 2019] where the authors present an analysis of various shock parameters calculated from the data.

In the dataset for the machine learning project, we use the magnetic field data from the FGM instrument and electric field spectrograms from the WHISPER instrument, and ion energy spectrograms and plasma moments from the CIS instrument. A combination of the multiple datasets, both in image and time-series form, shall allow for unambiguous identification.

Since Cluster is a four-spacecraft mission, the same discontinuity is crossed by multiple spacecraft in different places, and the profile is often not identical. However, the objective of the presented project is to obtain consistent timing even in the presence of some variation between the spacecraft.

All Cluster data is public and can be downloaded from the [ESA Cluster Science Archive](https://csa.esac.esa.int/csa-web/).



In the following, we present a tutorial for the pipeline, which can also be found on [GitHub](https://github.com/epn-ml/Tutorial_IAP_Boundaries).
