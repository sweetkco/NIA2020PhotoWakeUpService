import tensorflow.compat.v1 as tf
from .regressor import *
from .resnet_v2 import *
from .resize_img import *

from .util import image as img_util
from .util import openpose as op_util

import cv2

from .tf_smpl import SMPL

class HMR:

    def __init__(self,config,sess=None):

        tf.disable_eager_execution()
        self.final_thetas = []
        self.total_params = 85
        self.batch_size = 1
        self.num_stage=3
        self.img_size = 224
        input_size = (self.batch_size, self.img_size, self.img_size, 3)
        self.images = tf.placeholder(tf.float32, shape=input_size)
        self.thetas = tf.placeholder(tf.float32, shape=(1,85))
        self.load_path = config.hmr_checkpoint
        self.smpl = SMPL(config.smpl_params)

        self.ext = Image_extractor()

        if sess is None:
            self.sess = tf.Session()

        else:
            self.sess = sess

        self.build_model()
        self.saver = tf.train.Saver()
        self.prepare()


    def build_model(self):

        self.mean_var = tf.Variable(tf.zeros((1, self.total_params)), name="mean_param", dtype=tf.float32)

        self.feature = encoder(self.images, is_training=False, reuse=False)

        self.all_verts = []
        self.all_kps = []
        self.all_cams = []
        self.all_Js = []
        self.final_thetas = []
        self.all_weights = []
        theta_prev = tf.tile(self.mean_var, [self.batch_size, 1])


        for i in range(self.num_stage):

            state = tf.concat([self.feature, theta_prev],1)

            if i == 0:
                delta_theta = regressor(state,num_output=self.total_params,
                                        is_training=False,
                                        reuse=False)
            else:
                delta_theta = regressor(state,num_output=self.total_params,
                                        is_training=False,
                                        reuse=True)

            theta = theta_prev+delta_theta

            cams = theta[:, :3]
            poses = theta[:, 3:(3 + 72)]
            shapes = theta[:, (3 + 72):]

            verts, Js, weights = self.smpl(shapes, poses)
            print("-"*80)
            print(Js)
            print("-" * 80)


            pred_kp = batch_orth_proj_idrot(Js,cams)
            self.all_verts.append(verts)
            self.all_kps.append(pred_kp)
            self.all_cams.append(cams)
            self.all_Js.append(Js)
            self.all_weights.append(weights)
            self.final_thetas.append(theta)

            theta_prev = theta

    def prepare(self):

        self.saver.restore(self.sess, self.load_path)
        self.mean_value = self.sess.run(self.mean_var)

    def predict(self,images):

        images,proc_param,img = self.preprocess_image(images)
        images = np.expand_dims(images,0)

        results = self.predict_dict(images)

        return results,proc_param,img

    def predict_dict(self,images):

        feed_dict = {
            self.images: images,
        }

        fetch_dict = {
            'joints': self.all_kps[-1],
            'verts': self.all_verts[-1],
            'cams': self.all_cams[-1],
            'joints3d': self.all_Js[-1],
            'theta': self.final_thetas[-1],
            'weights': self.all_weights[-1]
        }

        results = self.sess.run(fetch_dict,feed_dict)

        #joints = results['joints']
        #results['joints'] = ((joints + 1) * 0.5) * self.img_size

        return results

    def preprocess_image(self,img_path, json_path=None):

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if img.shape[2] == 4:
            img = img[:, :, :3]

        if json_path is None:
            if np.max(img.shape[:2]) != self.img_size:
                scale = (float(self.img_size) / np.max(img.shape[:2]))
            else:
                scale = 1.
            center = np.round(np.array(img.shape[:2]) / 2).astype(int)
            # image center in (x,y)
            center = center[::-1]
        else:
            scale, center = op_util.get_bbox(json_path)

        crop, proc_param = img_util.scale_and_crop(img, scale, center,
                                                   self.img_size)

        # Normalize image to [-1, 1]
        crop = 2 * ((crop / 255.) - 0.5)

        return crop, proc_param, img


def batch_orth_proj_idrot(X, camera, name=None):
    """
    X is N x num_points x 3
    camera is N x 3
    same as applying orth_proj_idrot to each N
    """
    with tf.name_scope(name, "batch_orth_proj_idrot", [X, camera]):
        # TODO check X dim size.
        # tf.Assert(X.shape[2] == 3, [X])

        camera = tf.reshape(camera, [-1, 1, 3], name="cam_adj_shape")

        X_trans = X[:, :, :2] + camera[:, :, 1:]

        shape = tf.shape(X_trans)
        return tf.reshape(
            camera[:, :, 0] * tf.reshape(X_trans, [shape[0], -1]), shape)



