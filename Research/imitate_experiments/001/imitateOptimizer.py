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
    
    def __init__(self,learning_rate,use_locking=False,name="Imitate"):
        '''
        Construct a new imitate optimizer
        
        Args:
         learning_rate: A Tensor or a floating point value. The learning rate to use
         use_locking: If True use locks for update operations.
         name: Optional name prefix for the operations created when applying gradients. Defaults to "Imitate".
        '''
        super(ImitateOptimizer,self).__init__(use_locking,name)
        self._learning_rate = learning_rate
        self._learning_rate_tensor = None
        
        def _apply_dense(self,grad,var):
            
        