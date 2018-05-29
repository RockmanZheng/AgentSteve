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

# Hyperparameters
_lambda = 1.0

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
                             name='Input')


# Feature extractor Df
df_train_var = []
# conv-pool-conv-pool

# Convolutional Layer 1
# Use padding 
conv_layer_1 = tf.layers.Conv3D(filters = 64,
                                kernel_size=[5,5,5],
                                padding = 'same',
                                activation= tf.nn.relu,
                               name = 'Df_Conv_1')

# Max Pooling Layer 1
pool_layer_1 = tf.layers.MaxPooling3D(pool_size = [2,2,2],
                                      strides = [1,1,1],
                                      padding = 'same',
                                     name = 'Df_Pool_1')


# Convolutional layer 2
conv_layer_2 = tf.layers.Conv3D(filters = 32,
                               kernel_size = [5,5,5],
                               padding = 'same',
                               activation = tf.nn.relu,
                               name = 'Df_Conv_2')
# The last max pooling layer, used as feature layer
feature_layer = tf.layers.MaxPooling3D(pool_size = [2,2,2],
                                      strides = [1,1,1],
                                      padding = 'same',
                                      name = 'Feature')


# Construct feature extractor
df = conv_layer_1(input_layer)
df = pool_layer_1(df)
df = conv_layer_2(df)
df = feature_layer(df)

# Domain Discriminator
dd_train_var = []
dense_layer_1 = tf.layers.Dense(units=1024,
                                activation = tf.nn.relu,
                               name = 'Dd_Dense')
dropout_layer_1 = tf.layers.Dropout(rate = 0.5,
                                   name = 'Dd_Dropout')
# Logits Layer
logits_layer_1 = tf.layers.Dense(units=2,
                                name = 'Dd_Logits')


# Construct domain discriminator
dd = dense_layer_1(df)
dd = dropout_layer_1(dd)
dd = logits_layer_1(dd)

# Performer Discriminator
dr_train_var = []
dense_layer_2 = tf.layers.Dense(units=1024,
                                activation = tf.nn.relu,
                               name = 'Dr_Dense')
dropout_layer_2 = tf.layers.Dropout(rate = 0.5,
                                   name = 'Dr_Dropout')
# Logits Layer
logits_layer_2 = tf.layers.Dense(units=2,
                                name = 'Dr_Logits')

# Construct performer discriminator
dr = dense_layer_2(df)
dr = dropout_layer_2(dr)
dr = logits_layer_2(dr)


labels = np.array([[1,2]])
# Domain discrimination loss
##dd_loss = tf.losses.softmax_cross_entropy(onehot_labels=labels,logits=dd_logits_layer)
# Performer discrimination loss
##dr_loss = tf.losses.softmax_cross_entropy(onehot_labels=labels,logits=dr_logits_layer)
# Total loss used to train a domain invariant Df and corresponding Dr
##loss = dr_loss-_lambda*dd_loss


dd_loss = tf.losses.softmax_cross_entropy(onehot_labels=[[[[[1,2]]]]],
                                          logits = dd)
dr_loss = tf.losses.softmax_cross_entropy(onehot_labels=[[[[[1,2]]]]],
                                          logits = dr)
total_loss = dr_loss - _lambda*dd_loss
adam_op = tf.train.AdamOptimizer()

# Variables in layers are created only after we initialize them!
init = tf.global_variables_initializer()
sess.run(init)

# Gather all trainable variables into one single list
df_train_var += conv_layer_1.trainable_variables
df_train_var += pool_layer_1.trainable_variables
df_train_var += conv_layer_2.trainable_variables
df_train_var += feature_layer.trainable_variables
# Gather all trainable variables into one single list
dd_train_var += dense_layer_1.trainable_variables
dd_train_var += dropout_layer_1.trainable_variables
dd_train_var += logits_layer_1.trainable_variables
# Gather all trainable variables into one single list
dr_train_var +=dense_layer_2.trainable_variables
dr_train_var +=dropout_layer_2.trainable_variables
dr_train_var +=logits_layer_2.trainable_variables

# Pretraining
pretrain_op = adam_op.minimize(loss=dr_loss,
                              var_list = df_train_var+dr_train_var,
                              name = 'Pretrain')

# Fix feature extractor and train Dd
dd_train_op = adam_op.minimize(loss = dd_loss,
                              var_list = dd_train_var,
                              name = 'Train_Dd')
# Fix domain discriminator and train Df and Dr
train_op = adam_op.minimize(loss=total_loss,
                           global_step = tf.train.get_global_step(),
                           var_list = df_train_var+dr_train_var,
                           name = 'Train_Df_Dr')

init = tf.global_variables_initializer()
sess.run(init)

# Run pretraining
sess.run(pretrain_op,feed_dict = {input_layer:[[[[[255,255,255]]]]]})

def is_converge():
    return True

# Begin train loop
while True:
    sess.run(dd_train_op,feed_dict = {input_layer:[[[[[255,255,255]]]]]})
    sess.run(train_op,feed_dict = {input_layer:[[[[[255,255,255]]]]]})
    if is_converge():
        break

writer = tf.summary.FileWriter("./model/", sess.graph)

writer.close()