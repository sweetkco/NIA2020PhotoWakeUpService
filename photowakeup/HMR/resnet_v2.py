import tensorflow.compat.v1 as tf
import tf_slim as slim
from tf_slim.nets import resnet_v2

def encoder(x, is_training=True, weight_decay=0.001,reuse=False):

    with tf.name_scope("encoder", values=[x]):
        with slim.arg_scope(
                resnet_v2.resnet_arg_scope(weight_decay=weight_decay)):
            net, _ = resnet_v2.resnet_v2_50(
                x,
                num_classes = None,
                is_training = is_training,
                reuse = reuse,
                scope = 'resnet_v2_50'
            )

            net = tf.squeeze(net,axis=[1,2])

    return net
