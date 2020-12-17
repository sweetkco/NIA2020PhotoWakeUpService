import argparse
import os
from hpe import get_rect
from hpe.models.with_mobilenet import PoseEstimationWithMobileNet
from hpe.modules.keypoints import extract_keypoints, group_keypoints
from hpe.modules.load_state import load_state
import torch
from hpe.get_rect import get_rect
from pifuhd.apps.recon import recon
from pifuhd.apps.clean_mesh import meshcleaning
from HMR.hmr import HMR
from HMR.smpl import SMPL
import numpy as np
from pifuhd.lib.options import BaseOptions
from image_proc import image_processing,blurring
import cv2
from segmentation import segmentation
import trimesh

class Options(object):
    def __init__(self):
        self.dict = {'input_folder': './input_images', 'save_folder': './results', 'device': 'cpu',
                     'pose_checkpoint': './checkpoints/checkpoint_iter_370000.pth',
                     'pifu_checkpoint': './checkpoints/pifuhd.pt', 'hmr_checkpoint': './checkpoints/model.ckpt-667589',
                     'smpl_params': './checkpoints/neutral_smpl_with_cocoplus_reg.pkl', 'out_path': './results',
                     'use_rect': 'True', 'dataset': 'renderppl', 'dataroot': './input_images', 'loadSize': 1024,
                     'name': '', 'debug': False, 'mode': 'inout', 'tmp_id': 0, 'gpu_id': 0, 'batch_size': 32,
                     'num_threads': 1, 'serial_batches': False, 'pin_memory': False, 'learning_rate': 0.001,
                     'num_iter': 30000, 'freq_plot': 100, 'freq_mesh': 20000, 'freq_eval': 5000, 'freq_save_ply': 5000,
                     'freq_save_image': 100, 'resume_epoch': -1, 'continue_train': False, 'finetune': False,
                     'resolution': 512, 'no_numel_eval': False, 'no_mesh_recon': False, 'num_sample_inout': 6000,
                     'num_sample_surface': 0, 'num_sample_normal': 0, 'num_sample_color': 0, 'num_pts_dic': 1,
                     'crop_type': 'fullbody', 'uniform_ratio': 0.1, 'mask_ratio': 0.5, 'sampling_parts': False,
                     'sampling_otf': False, 'sampling_mode': 'sigma_uniform', 'linear_anneal_sigma': False,
                     'sigma_max': 0.0, 'sigma_min': 0.0, 'sigma': 1.0, 'sigma_surface': 1.0, 'z_size': 200.0,
                     'norm': 'batch', 'netG': 'hgpifu', 'netC': 'resblkpifu', 'num_stack': 4, 'hg_depth': 2,
                     'hg_down': 'ave_pool', 'hg_dim': 256, 'mlp_norm': 'group',
                     'mlp_dim': [257, 1024, 512, 256, 128, 1], 'mlp_dim_color': [1024, 512, 256, 128, 3],
                     'mlp_res_layers': [2, 3, 4], 'merge_layer': -1, 'random_body_chop': False, 'random_flip': False,
                     'random_trans': False, 'random_scale': False, 'random_rotate': False, 'random_bg': False,
                     'schedule': [10, 15], 'gamma': 0.1, 'lambda_nml': 0.0, 'lambda_cmp_l1': 0.0,
                     'occ_loss_type': 'mse', 'clr_loss_type': 'mse', 'nml_loss_type': 'mse', 'occ_gamma': None,
                     'no_finetune': False, 'val_test_error': False, 'val_train_error': False, 'gen_test_mesh': False,
                     'gen_train_mesh': False, 'all_mesh': False, 'num_gen_mesh_test': 4,
                     'load_netG_checkpoint_path': None, 'load_netC_checkpoint_path': None,
                     'checkpoints_path': './checkpoints', 'results_path': './results', 'load_checkpoint_path': None,
                     'single': '', 'mask_path': None, 'img_path': None, 'load_netMR_checkpoint_path': None,
                     'loadSizeBig': 1024, 'loadSizeLocal': 512, 'train_full_pifu': False, 'num_local': 1,
                     'load_netFB_checkpoint_path': None, 'load_netF_checkpoint_path': None,
                     'load_netB_checkpoint_path': None, 'use_aio_normal': False, 'use_front_normal': False,
                     'use_back_normal': False, 'no_intermediate_loss': False, 'aug_alstd': 0.0, 'aug_bri': 0.2,
                     'aug_con': 0.2, 'aug_sat': 0.05, 'aug_hue': 0.05, 'aug_gry': 0.1, 'aug_blur': 0.0, 'start_id': -1,
                     'end_id': -1}

    def initialize(self):
        dict = self.ToNameSpace(self.dict)
        return dict

    class ToNameSpace(object):
        def __init__(self, dict):
            self.__dict__.update(dict)


config = Options().initialize()

class PhotoWakeUp(object):
    def __init__(self):
        if torch.cuda.is_available():
            self.device = 'cuda'
            print('Use gpu')
        else:
            print(config.device)
            self.device = config.device
        self.input_lists = [list for list in os.listdir(config.input_folder)]
        self.PoseEstimationWithMobileNet = PoseEstimationWithMobileNet().to(self.device)
        self.pose_checkpoint = torch.load(config.pose_checkpoint, map_location=self.device)
        load_state(self.PoseEstimationWithMobileNet, self.pose_checkpoint)
        self.HMR = HMR(config)
        self.smpl = SMPL(config.smpl_params,config.out_path)

    def PoseEstimation(self):
        file_lists = [file for file in self.input_lists if file.split('.')[-1] in ['png', 'jpeg', 'jpg', 'PNG', 'JPG', 'JPEG']]
        for idx ,file in enumerate(file_lists):
            print(file)
            file_path = os.path.join(config.input_folder,file)
            get_rect(self.PoseEstimationWithMobileNet,[file_path],512)
            result_512,result_1024 = image_processing(file_path)
            print("./results/{}.png".format(file.split(".")[0]))
            cv2.imwrite("./results/{}_512.png".format(file.split(".")[0]), np.array(result_512))
            cv2.imwrite("./results/{}_1024.png".format(file.split(".")[0]), np.array(result_1024))

    def Reconstruction(self):
        recon(config,config.use_rect)
        print('Clean Mesh...')
        self.Clean_Mesh()

    def Clean_Mesh(self):
        print(config.save_folder)
        meshcleaning(config.save_folder)

    def KeyPoints(self):
        file_lists = [file for file in self.input_lists if file.split('.')[-1] in ['png', 'jpeg', 'jpg', 'PNG', 'JPG', 'JPEG']]
        for idx , file in enumerate(file_lists):
            file_path = os.path.join(config.input_folder, file)
            if 'front' in file:
                pred1 = self.HMR.predict(file_path)[0]
                #pred = pred1['theta']
                print("joints",pred1['joints'].shape)
                print("joints 3d" , pred1['joints3d'].shape)
                #poses = pred[:,3:(3+72)][0]
                #shapes = pred[:,(3+72):][0]
                joints3d = np.dot(pred1['joints3d'].reshape(-1,3), np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
                np.save(os.path.join(config.out_path, '{}_joints.npy'.format(file.split('.')[0])), joints3d)
                #self.smpl.set_params(beta=shapes,pose=poses,trans=np.array([0, 0, 0]))
                #self.smpl.save_to_obj(os.path.join(config.out_path, 'test_smpl.obj'))
                #mesh = trimesh.load(os.path.join(config.out_path, 'test_smpl.obj'))
                #print(os.path.join(config.out_path, 'test_smpl.obj'))
                #scale_matrix = trimesh.transformations.scale_matrix(100)
                #change_axis = [[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
                #mesh = mesh.apply_transform(scale_matrix)
                #mesh = mesh.apply_transform(change_axis)

                #self.save_obj(mesh.vertices, mesh.faces,file_name=os.path.join(config.out_path, 'test_smpl.obj'))
                #self.smpl.save_keypoints(file.split('.')[0])
            else:
                continue
    def Segmentation(self):
        segmentation()

    def save_obj(self,v, f, file_name):
        obj_file = open(file_name, 'w')
        for i in range(len(v)):
            obj_file.write('v ' + str(v[i][0]) + ' ' + str(v[i][1]) + ' ' + str(v[i][2]) + '\n')
        for i in range(len(f)):
            obj_file.write('f ' + str(f[i][0] + 1) + '/' + str(f[i][0] + 1) + ' ' + str(f[i][1] + 1) + '/' + str(
                f[i][1] + 1) + ' ' + str(f[i][2] + 1) + '/' + str(f[i][2] + 1) + '\n')
        obj_file.close()

#pwu=PhotoWakeUp()
#pwu.PoseEstimation()
#pwu.Reconstruction()
#pwu.KeyPoints()
#pwu.Segmentation()