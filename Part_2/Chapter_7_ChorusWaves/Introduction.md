# Introduction

This chapter is about the science case introducing "The identification of the Chorus wave emission", proposed by the Institute of Atmospheric Physics of Czech Academy of Sciences (IAP-CAS).

In the following, we present a tutorial for an ML pipeline, which can also be found on [GitHub](https://github.com/epn-ml/Chorus-Wave).


## Description of the science case

Planetary magnetospheres trap energetic electrons and ions in regions called radiation belts. The trapped particles interact with electromagnetic waves gaining or losing their kinetic energy. Ongoing studies of the Chorus wave emissions are pointing to their significant role in the wave-particle interaction within planetary magnetospheres. The Chorus is the whistler-mode emission at frequencies of several kHz and may be split into two bands around half of the equatorial electron cyclotron frequency. The Chorus is typically composed of short sub-second elements rising or falling in frequency. This emission is not exclusive to the terrestrial magnetosphere, but it has also been observed at Jupiter or Saturn playing a significant role in particle energization at their magnetospheres.

The main objective is to develop an ML-based tool to identify the Chorus wave emission in the terrestrial magnetosphere from the measured Cluster mission data. This work will consequently allow the identification of time-frequency intervals and individual elements with intense Chorus wave emissions from the spacecraft data, allowing for further automatic detailed data analysis and processing. As a basis for the identification, we will use an electric time-frequency spectrogram. The identification is frequently made by a trained person tagging the time and frequency of individual elements. Thus, existing large datasets of Chorus time intervals from spacecraft missions at the Earth are available and can be used to train the ML methods.

The resulting tool will be helpful in the scanning of large datasets (such as the Cluster or THEMIS data spanning two decades of continuous measurements) for plasma wave emissions, required when extracting subsets of the data for statistical analysis of various plasma phenomena and their dependencies on the parameter regime. Another promising use is to employ this technique to identify the precise times of the same wave emissions by multiple spacecraft, which allows for spatial-temporal analysis.

The developed tool can be trained on rich datasets from the terrestrial magnetosphere and later might be applied to more rare data from other solar system planets such as Jupiter or Saturn.

## Dataset

This science case targets plasma wave identification from the color-coded time-frequency spectrograms. The wave emissions typically occur as structured or unstructured features with visible boundaries in the time-frequency domain. For this science case, we have focused on the whistler-mode chorus emission that propagates at frequencies around half of electron cyclotron frequency in the inner magnetosphere. a list of time-frequency spectrograms as observed by the Wideband receiver on board four Cluster spacecraft. There are more than 4000 thousand events irregularly observed while spacecraft crossed the terrestrial inner-magnetosphere and the nearby solar wind. In file names, we have flagged if the chorus emission is presented (82% of events) or not (18% of events). The number of the frequency row of local cyclotron electron frequency for easier identification is also included in the file name. The dataset can be used for both supervised and unsupervised machine learning. 

In the dataset for the machine learning project, we use the electric field spectrograms from the Cluster Wideband instrument. An example of the above data with the intense Chorus emission is shown in {numref}`chorusExample`.

```{figure} ./images/chorus.png
---
width: 600px
name: chorusExample
---
An example of the Chorus wave emission as observed in the data from the Cluster spacecraft showing the electric field spectrogram from the Wideband instrument. The Chorus emission appears as an intense bursty structured emission. The white dashed line presents half of the equatorial electron cyclotron frequency.
```

All Cluster data is public and can be downloaded from the [ESA Cluster Science Archive](https://csa.esac.esa.int/csa-web/).