# Machine learning pipeline

## Brief summary of our approach

The first step in this science case was the reimplementation of a model proposed by {cite:t}`nguyen2019`, which had previously been tested on WIND data and achieved a maximum recall and precision of around 84%.

After the reimplementation of this model, the model was tested on STEREO-A and STEREO-B data as well as on WIND data. All three contain less variables than the original data set used by Nguyen et al. At a similar recall as for the original set, the precision for all three datasets was only around 30% and the accuracy in delivering start and end times was limited.

The next step was to align all three data sets in order to process more training data for a combined model. It was tested on held out datasets for WIND, STEREO-A and STEREO-B. Surprisingly, this did not sufficiently improve performance and lead us to explore other approaches.

Starting from the reimplementation, a post processing step based on YOLO v5 (ultralytics) was investigated, in order to improve performance. Even though first results seemed promising, the idea was later discarded due to unsatisfactory results and the laborious pipeline. Since the ultimate goal is an explicit and widely applicable pipeline, it was decided to abandon the general approach of using multiple basic neural networks and the similarity measure used by {cite:t}`nguyen2019` completely and compose it as a segmentation problem instead.

We proposed a pipeline using a UNet {cite:p}`ronneberger2015` including residual blocks, squeeze and excitation blocks, Atrous Spatial Pyramidal Pooling (ASPP) and attention blocks, similar to the ResUNet++ {cite:p}`jha2019`, for the automatic detection of ICMEs. Comparing it to our first results, we find that our model outperforms the baseline regarding GPU usage, training time and robustness to missing features, thus making it more usable for other data sets, as well as the three aligned data sets. The relatively fast training allows straightforward tuning of hyperparameters. Our proposed pipeline can be used for any time series segmentation problem. The straightforward implementation allows a simple extension to a multi-class classification problem and paves the way to include corotating interaction regions into the range of detectable phenomena within our pipeline.

The pipeline is open source and can be found on [GitHub](https://github.com/epn-ml/IWF-ICMEs).
