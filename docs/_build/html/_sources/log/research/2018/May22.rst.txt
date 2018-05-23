Tue May 22 2018
===============

Current progress: working on imitation module.

I was inspired by this paper *Third-Person Imitation Learning*, which is available on arXiv. `Link <https://arxiv.org/pdf/1703.01703.pdf>`_

There are 3 important parts in the imitation module, namely Df, Dr, Dd, which are feature extractor, performer discriminator, and domain discriminator, respectively, as mentioned in the paper.

Images are first sent into Df which will then extract features from them. These features should be domain invariant (environment agnostic). In other words, one cannot tell from where the initial images come solely based on these features.

The extracted features are then sent into Dd. Dd will classify their source domains. A good Df will output confusing features as discussed above so that a good Dd cannot tell the difference and will give any answer with equal probability.

The features are also sent into Dr. In fact, features from several time-steps will be sent to introduce temporal information. Dr will then give its judgement about whether it is the expert doing the task, or it is an amateur. The environment agnostic natrue of the features should improve the accuracy of discrimination result.

We discovered that 3 components need each other and no one can be singled out. Feature extractor Df is neccessary since dealing higher level concept is better than handling raw pixels. Domain discriminator Dd is also needed because we need to force our Df to be domain invariant. And finally, if without Dr, the Df will easily adjust to output constant value to fool Dd, which is clearly not desired. Thus Dr is crucial for training Df to extract meaningful features.

So we can only implement and test 3 components all at once. If we see them as a new whole integrity then we will feel less pain (:-)

Coding
------

I had stated a new experiment under the directory *Research/imitate_experiments*, coded 001. And add a few new files, including:

* *domain_discriminator.py*
* *feature_extractor.py*
* *imitateOptimizer.py*
* *performer_discriminator.py*
* *script01.py*

Currently I have made a draft version of algorithm structure in *script01.py*. It merely outlines all elements that I thought of, and cannot be run. Other files are useless for the moment.

In *script01.py* I basically just put some TensorFlow layers API in there, and exposing their function signatures for later development. 

Here is the architecture that I am thinking of.

First of all, we will need an input layer. We will use video stream to train our imitator instead of simple images. So the input layer would be a 5 dimension tensor, with dimension [batches,depth,height,width,channels]. Here *batches* refers to the number of training batches, *depth* is the number of frames. And *height* and *width* is the size the our input images. And *channels* typically equals to 3 for colored images, for example those in RGB or HSI format, and equals to 1 for gray scale images.

Df, the feature extractor, can be implemented as the first few layers in a neural network based discriminator. So after replicating a simple MINST discriminator (see  this `tutorial <https://www.tensorflow.org/tutorials/layers>`_), we choose the first 4 layers of it to play the role of a feature extractor. Namely:

* Convolutional layer #1, with ReLU activation
* Max pooling layer #1
* Convolutional layer #2, with ReLU activation
* Max pooling layer #2, also named feature layer, since we are constructing a feature extractor

Then we will send output of the last layer into both Dd and Dr.

Dd and Dr, the domain and performer discriminators, will have same structure (at least for now), since they are both classifier and both using output of Df as input. The structure is:

* Dense layer #1, with ReLU activation
* Dropout layer
* logits layer #2 (dense), with 2 units, outputing logits for 2 classes. For Dd, they represent expert domain and amateur domain. For Dr, they represent expert and amateur.

Finally we will use sigmoid function to convert logits to values within [0,1), and view them as probability. Probabilities of 2 units should sum up to 1.

Future Works
------------

Training procedure needs to be constructed. And input feed needs to be prepared.



