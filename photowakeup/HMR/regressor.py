import tensorflow.compat.v1 as tf
import tf_slim as slim

def regressor(x, num_output=85, is_training=True, reuse=False ,name="3D_module"):

    with tf.variable_scope(name, reuse=reuse) as scope:

        net = slim.fully_connected(x, 1024, scope='fc1')
        net = slim.dropout(net, 0.5, is_training=is_training, scope='dropout1')
        net = slim.fully_connected(net, 1024, scope='fc2')
        net = slim.dropout(net, 0.5, is_training=is_training, scope='dropout2')
        small_xavier = tf.keras.initializers.VarianceScaling(
            scale=.01, mode='fan_avg', distribution='uniform')

        net = slim.fully_connected(
            net,
            num_output,
            activation_fn=None,
            weights_initializer=small_xavier,
            scope='fc3')

    return net
