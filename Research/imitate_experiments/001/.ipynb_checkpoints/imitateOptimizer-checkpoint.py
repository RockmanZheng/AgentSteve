from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from tensorflow.python.eager import context
from tensorflow.python.framework import ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import resource_variable_ops
from tensorflow.python.training import optimizer
from tensorflow.python.training import training_ops
from tensorflow.python.util.tf_export import tf_export

class ImitateOptimizer(optimizer.Optimizer):
    '''
    Optimizer that is used in third person imitation
    '''