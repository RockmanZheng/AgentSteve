import tensorflow as tf
import numpy as np


'''
Very simple feature extractor. Basically copying anything from MNIST classifier tutorial on tensorflow website, except that we only choose first several layers since we only need features generated in the middle of neural network and the final outputs are not needed.

Architecture as follow:
conv layer 1, ReLU
pool layer 1, max pool
conv layer 2, ReLU
pool layer 2, max pool
'''



def cnn_model(feature):
    input_layer = tf.reshape(feature,[-1,28,28,1])
    # Convolutional layer 1
    conv1 = tf.layers.conv3d(inputs=input_layer,
                            filters = 32,
                            kernel_size = [5,5],
                            padding = "same",
                            activation=tf.nn.relu)
    # Pooling layer 1
    pool1 = tf.layers.max_pooling3d(inputs = conv1,
                                   pool_size=[2,2])
    # Convolutional layer2
    conv2 = tf.layers.conv3d(inputs = pool1,
                            filters = 64,
                            kernel_size = [5,5],
                            padding = "same",
                            activation = tf.nn.relu)
    # Pooling layer 2
    pool2 = tf.layers.max_pooling3d(inputs=conv2,
                                   pool_size = [2,2])
    return pool2

def model_fn(features,labels,mode):
    '''Model function'''
    # Feature extraction part, both spatial and temporal features will be extracted
    cnn_hue = cnn_model(features["hue"])
    cnn_saturation = cnn_model(features["saturation"])
    cnn_illuminance = cnn_model(features["illuminance"])

    # Flatten model
    cnn_hue_flat = tf.reshape(cnn_hue,[-1,7*7*64])
    cnn_saturation_flat = tf.reshape(cnn_saturation,[-1,7*7*64])
    cnn_illuminance_flat = tf.reshape(cnn_illuminance,[-1,7*7*64])
    # Combine features from 3 channels
    cnn_features = tf.concat([cnn_hue_flat,
                             cnn_saturation_flat,
                             cnn_illuminance_flat])
    
    # Domain discriminator
    # Dense layer, dropout regularization
    dense1 = tf.layers.dense(inputs=cnn_features,
                             units=1024,
                             activation = tf.nn.relu)
    dropout1 = tf.layers.dropout(inputs=dense1,
                               rate = 0.4,
                               training = mode==tf.estimator.Model)
    # Logits Layer
    logits1 = tf.layers.dense(inputs=dropout1,
                              units=10)
    
    # Performer discriminator
    # Dense layer, dropout regularization
    dense2 = tf.layers.dense(inputs=cnn_features,
                             units=1024,
                             activation = tf.nn.relu)
    dropout2 = tf.layers.dropout(inputs=dense2,
                               rate = 0.4,
                               training = mode==tf.estimator.Model)
    # Logits Layer
    logits2 = tf.layers.dense(inputs=dropout2,
                              units=10)
    
    predictions = {
        "domain":tf.argmax(input = logits1,axis=1),
        "domain_prob":tf.nn.softmax(logits1,name="softmax_tensor"),
        "performer":tf.argmax(input=logits2,axis=1),
        "performer_prob":tf.nn.softmax(logits2,name="softmax_tensor")
    }
    
    if mode ==tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode,predictions=predictions)
    # Domain discrimination loss
    loss1 = tf.losses.sparse_softmax_cross_entropy(labels=labels[,1],logits=logits1)
    # Performer discrimination loss
    loss2 = tf.losses.sparse_softmax_cross_entropy(labels=labels[,2],logits=logits2)
    
    if mode==tf.estimator.ModeKeys.TRAIN:
        adam_op = tf.train.AdamOptimizer()
        
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        # Train Df, Dr
        train_op1 = adam_op.minimize(loss=loss2,
                                     global_step = tf.train.get_global_step())
        train_op2 = adam_op.minimize(loss=loss2,
                                      global_step=tf.train.get_global_step())
        train_op3 = optimizer.minimize()