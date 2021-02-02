import numpy as np
import cv2
from Boundary_Renderer import SMPLRenderer

def visualize(img, proc_param, joints, verts, cam, img_path):
    """
    Renders the result in original image coordinate frame.

    """
    cam_for_render, vert_shifted, joints_orig = get_original(
        proc_param, verts, cam, joints, img_size=img.shape[:2])


    renderer = SMPLRenderer(face_path='/Users/choehanjoon/PycharmProjects/HMR/smpl_faces.npy')


    rend_img = renderer(
        vert_shifted, cam=cam_for_render, img_size=img.shape[:2])
    rend_img_vp2 = renderer.rotated(
        vert_shifted, 180, cam=cam_for_render, img_size=img.shape[:2])

    smplPath = 'SMPL.png'
    print("Saving SMPL picture to:")
    print(smplPath)

    rend_img = np.logical_and(rend_img[:, :, 0] == 255, rend_img[:, :, 1] == 255, rend_img[:, :, 2] == 255)
    rend_img = abs(rend_img*255-255)

    cv2.imwrite(smplPath, rend_img)

    smplPath = 'SMPLBack.png'
    print("Saving Depth Map to:")
    print(smplPath)

    rend_img_vp2 = np.logical_and(rend_img_vp2[:, :, 0] == 255, rend_img_vp2[:, :, 1] == 255, rend_img_vp2[:, :, 2] == 255)
    rend_img_vp2 = abs(rend_img_vp2 * 255 - 255)

    cv2.imwrite(smplPath, rend_img_vp2)



def get_original(proc_param, verts, cam, joints, img_size):
    img_size = proc_param['img_size']
    print(img_size)
    undo_scale = 1. / np.array(proc_param['scale'])

    cam_s = cam[0]
    cam_pos = cam[1:]
    principal_pt = np.array([img_size, img_size]) / 2.
    flength = 500.
    tz = flength / (0.5 * img_size * cam_s)

    trans = np.hstack([cam_pos, tz])
    vert_shifted = verts + trans

    start_pt = proc_param['start_pt'] - 0.5 * img_size
    final_principal_pt = (principal_pt + start_pt) * undo_scale
    cam_for_render = np.hstack(
        [np.mean(flength * undo_scale), final_principal_pt])

    # This is in padded image.
    # kp_original = (joints + proc_param['start_pt']) * undo_scale
    # Subtract padding from joints.
    margin = int(img_size / 2)
    kp_original = (joints + proc_param['start_pt'] - margin) * undo_scale

    return cam_for_render, vert_shifted, kp_original

from resize_img import *
from model import *
from smpl import SMPL

model = HMR()
smpl = SMPL('/Users/choehanjoon/PycharmProjects/HMR/neutral_smpl_with_cocoplus_reg.pkl')
pic = '/Users/choehanjoon/PycharmProjects/HMR/coco0.png'

pred,proc_param,img = model.predict(pic)
print(pred.keys())
joints = pred['joints']
verts = pred['verts']
cams = pred['cams']
img_path = pic

visualize(img, proc_param, joints[0], verts[0], cams[0], img_path)