Some introductory words
==========================

This very basic tutorial covers a supervised classification problem. First, let's briefly discuss some general terms and approaches.

**Supervised classification problem**

Basically, you have a classification problem in ML when your target variable is categorical, e.g. a specific species (of some plant, animal, etc.). In a supervised classification problem, there are known labels in the training data, from which the classifier tries to approximate a mapping function from the input variables to the output variables.

**Splitting into training and test set**

The basic approach for ML problems is to split the data set into a training and a test set.

The **training set** is used to (surprise!) train the model. The **test set** is then used to (surprise!) test the accuracy of the trained model.

Actually, we also need a third set - the **validation set**, which is used to evaluate the performance of each classifier, and to find and fine-tune the best model. However, as is often the case in space/planetary physics, the data set is not *that* large, so splitting the *not that large* data set in even smaller data sets should probably be avoided. In such a case, validation can be done using a **cross-validation** approach.

**Cross-validation**

The basic approach here is k-fold cross-validation. Thereby, the training set is split into k smaller subsets. The model is trained on one of the k folds as training set and validated on the remaining (k-1) folds. This is done for all of the k folds. The performance measure calculated by the k-fold cross-validation is the average of the results for all k folds.

The advantage of this approach is that validation does not need an extra data set. However, k-fold cross-validation might become computationally expensive.

**Coding environment**

As already mentioned, the code in this tutorial is written in Python 3. Hereby, Jupyter notebooks are used. You can either use your local installation (e.g. in a virtual environment) or you can use one of the external providers of this service (e.g. Google colab or Binder).
