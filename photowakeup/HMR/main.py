from resize_img import *
from hmr import *
from smpl import SMPL


model = HMR()
smpl = SMPL('/Users/choehanjoon/PycharmProjects/HMR/neutral_smpl_with_cocoplus_reg.pkl')#SMPL('neutral_smpl_with_cocoplus_reg.pkl')


pic = 'image/200_1.jpg'

pred = model.predict(pic)[0]['theta']


cams = pred[:,:3][0]
poses = pred[:,3:(3 + 72)][0]
shapes = pred[:,(3 + 72):][0]
print(cams)

smpl.set_params(beta=shapes, pose=poses,trans=cams)#np.array([0, 0.2, 0]))
smpl.save_to_obj('./smpl_np.obj')