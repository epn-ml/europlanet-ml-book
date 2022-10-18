# Introduction

This chapter is about the science case proposed "Landform classification and mapping using Machine Learning", proposed by the GMAP work package of Europlanet 2024 RI.

The ML pipeline is open source and can be found on [GitHub](https://github.com/epn-ml/DeepLandforms).

In the following, we present a tutorial for the pipeline, which can also be found on [GitHub](https://github.com/epn-ml/DeepLandforms/tree/main/Tutorial).

## Description of the science case

This science case is focused on the detection and mapping of sinkhole-like depressions on Mars and the Moon through Deep Learning Object Detection and Instance Segmentation.

The term sinkhole refers to different morphologies that have a in common the processes of depleting materials of different type into an area within the morphology itself (Waltham, 2005). On Earth the formation of sinkholes is related to a cluster of  processes, and could occur in various type of grounds, furthermore presence of water has a key-role. On other terrestrial planets, although the mechanisms for the origin of these landforms are similar, if not the same, with the main difference that as far as we know there is no liquid water that can be involved in the formation of these landforms, and therefore the mechanisms and processes are still debated. Several authors suggested the hypothesis of formation from lava tube collapses (Greeley, 1971; Cruikshank and , 1972; Carr et al., 1977), others imply different volcanic and tectonic processes involved (Wyrick et al., 2004). In karst environment, sinkholes are called "doline" and are more related to processes connected to dissolution of carbonates and evaporites, while in volcanic environments they are called "pit craters" and are more related to process connected to lava tube stability.

Doline, pit craters, pit chains and lava tubes are well-known morphologies on Earth (Lauterbach et al., 2019; Díaz Michelena et al., 2020), Mars (Carr, 1973; Cushing et al., 2007; Cushing, 2012; Cushing et al., 2015), Moon (Chappaz et al., 2017), Venus (Ernst et al., 2015), Mercury (Gillis-Davis et al., 2009), and Ganymede and Saturnian satellites (Barlow et al., 2017). Studies suggested the presence of sinkholes both in karst (Baioni and Tramontana, 2015, 2016) and volcanic terrains of Mars (Sauro et al., 2020a), in particular thanks to HiRISE and CTX cameras on board MRO more than 1000 potential cave entrances have been identified on Mars (Cushing, 2012), while on Moon thanks to SELENE and LRO cameras more than 300 (Wagner and Robinson, 2014).

In the framework of geological exploration of terrestrial planets like Earth, those landforms - being a potential direct access to subsurface - are one of the most promising environments where to focus the research of valuable data of different kind, from planet's geological stratigraphy (Lauterbach et al., 2019; Sauro et al., 2020a) to valuable ore deposits (Blamont, 2014). They could also provide access to cave entrances where it is possible to gather even more data since caves are a natural shelter from cosmic radiation, and thus potentially provide a feasible environment for searching of life traces (Léveillé and Datta, 2010; Cushing, 2012), for the development of future human outposts (Cushing, 2012; Blamont, 2014; Carrer et al., 2018), and for the planning of future missions (Hare et al., 2018).

 Detecting, mapping, and describing sinkhole-like landform is a challenging process since a set of tedious tasks must be conducted manually, from data collection to manual analysis, mapping using Geographic Information Systems (GIS) software and extracting morphometric parameters.

For Mars, there exists a downloadable database of more than 1000 cave candidates (Cushing, 2012) and there are several other publications that analyse possible cave entrances on Mars and Moon (Cushing et al., 2007; Hong, Yi and Kim, 2014; Jung et al., 2016; Sauro et al., 2020a). Also, for the Moon there is an online database, but it is not downloadable. Both of the databases are region specific or with preferred planetary spots, are created with manual or semi-automated methods and are not updated that regularly. Starting from literature, five classes have been identified:

    * Type-1: Skylight with possible cave entrance, flat rim, no ejecta blankets, almost perfect circular shape and no visible bottom.
    * Type-2: Pit crater with possible relation to lava tube, flat rim, no ejecta blankets, almost circular shape and visible bottom.
    * Type-3: Depression with flat rim, no ejecta blankets, elongated shape and visible bottom. Possible connection to lava tubes.
    * Type-4: Depression with flat rim, no ejecta blankets, shallow to very shallow depth. Circular to elongated shapes and usually aligned with other similar shapes.
    * Type-5: Impact crater with always visible non-flat rim. Often visible ejecta blankets and remnants.

As many of these landforms are extremely similar, a crucial role is the labelling of all classes and the creation of a modest initial data set to be used for training, validating and testing.
There are different challenges in this science case:

    * the identification and definition of unique characteristics that differentiate the classes, e.g. the shape of the rim,
    * the identification of the algorithms to be used,
    * the development of open-source tools and pipelines for all of the activities to be performed, and
    * the training and validation of all of the obtained results.

## Dataset

Mars optical images are provided by the Martian Reconnaissance Orbiter (MRO), and are composed of:

    * HiRISE images: a very high spatial resolution instrument with 0.3 m/pixel and a swath of approximately 30 km-wide. This instrument provides the highest quality images captured of Mars, designed for retrieving fine details from surface. The dataset used for preliminary tests consist of approx. 900 images.
    * CTX images: a mid-high spatial resolution instrument with 6 m/pixel resolution and a swath of approximately 30-km wide. This instrument provides more contextual images useful to understand the surround condition of HiRISE images, maintaining a high quality of detail retrieval.

Lunar optical images are provided by the LRO spacecraft, and are composed of:

    * LROC Narrow Angle Cameras (NACs): very-high resolution panchromatic cameras with 0,5 m/pixel and approx. 5 km swath
    * LROC Wide Angle Camera (WAC): a high resolution 7-color camera with 100 m/pixel and approx. 60 km swath

All data can be accessed through NASA PDS Geoscience Node ODE Portal.
