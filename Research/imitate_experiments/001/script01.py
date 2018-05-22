'''
I was inspired by this paper "Third-Person Imitation Learning", which is available on arXiv. Link: https://arxiv.org/pdf/1703.01703.pdf

There are 3 important parts, Df, Dr, Dd, which are feature extractor, performer discriminator, and domain discriminator, respectively, as mentioned in the paper.

Images are first sent into Df which will then extract features from them. These features should be domain invariant, or environment agnostic. In other words, one cannot tell from where the initial images come solely based on these features.

The extracted features are then sent into Dd. Dd will classify their source domains. A good Df will output confusing features as discussed above so that a good Dd will give any answer with equal probability.

The features are also sent into Dr. In fact, features from several time-steps will be sent to introduce temporal information. Dr will then give its judgement about whether it is the expert doing the task, or it is an amateur.

We discovered that 3 components need each other and no one can be singled out. Feature extractor Df is neccessary since dealing higher level concept is better than handling raw pixels. Domain discriminator Dd is also needed because we need to force our Df to be domain invariant. And finally, if without Dr, the Df will easily adjust to output constants to fool Dd, which is clearly not desired. Thus Dr is crucial for training Df to extract meaningful features.

So we can only implement and test 3 components all at once. If we see them as a new whole integrity then we will feel less pain (:-)
'''

import tensorflow as tf
import numpy as np

sess = tf.Session()

# Training batch
batch = 1
# image time interval
in_depth = 1
# image height
in_height = 1
# image width
in_width = 1
# Colored image typically has 3 channels
# RGB or HSI
in_channel = 3
# Construct input layer
# input: A Tensor. Must be one of the following types: half, bfloat16, float32, float64. Shape [batch, in_depth, in_height, in_width, in_channels].
input_layer = tf.placeholder('float',
                             [batch,in_depth,in_height,in_width,in_channel],
                             name='input_layer')
# Feature extractor Df
# conv-pool-conv-pool

# Convolutional Layer 1
# Use padding 
conv_layer_1 = tf.layers.conv3d(inputs = input_layer,
                                filters = 64,
                                kernel_size=[5,5,5],
                                padding = 'same',
                                activation= tf.nn.relu)

# Max Pooling Layer 1
pool_layer_1 = tf.layers.max_pooling3d(inputs=conv_layer_1,
                                      pool_size = [2,2,2],
                                      strides = [1,1,1],
                                      padding = 'same')
# Convolutional layer 2
conv_layer_2 = tf.layers.conv3d(inputs = pool_layer_1,
                               filters = 32,
                               kernel_size = [5,5,5],
                               padding = 'same',
                               activation = tf.nn.relu)
# The last max pooling layer, used as feature layer
feature_layer = tf.layers.max_pooling3d(inputs = conv_layer_2,
                                      pool_size = [2,2,2],
                                      strides = [1,1,1],
                                      padding = 'same')

# Domain Discriminator
dense_layer_1 = tf.layers.dense(inputs=feature_layer,
                                units=1024,
                                activation = tf.nn.relu)
dropout_layer_1 = tf.layers.dropout(inputs=dense_layer_1,
                           rate = 0.5,
                           training = True)
# Logits Layer
logits_layer_1 = tf.layers.dense(inputs=dropout_layer_1,
                          units=2)


