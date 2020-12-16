import cv2
import pickle
import numpy as np

class Image_extractor(object):

    def __init__(self):

        self.images = np.array([])
        self.idx = 0
        self.count = 0
        self.size = 0

    def preprocessing_image(self,img):

        if isinstance(img, (np.ndarray, np.generic) ):

            img = img
        else:
            img = cv2.imread(img,cv2.IMREAD_COLOR)

        image_size = 224

        if np.max(img.shape[:2]) != image_size:
            scale = (float(224)/np.max(img.shape[:2]))
        else:
            scale = 1.

        center = np.round(np.array(img.shape[:2])/2).astype(int)
        center = center[::-1]

        crop, proc_param = scale_and_crop(img,scale,center,image_size)

        crop = normalize(crop)

        return crop

    def select_images(self,anns,img,min_vis=5, min_max_height=60):

        points_other_than_faceshoulder = [
            16,  # R ankle
            14,  # R knee
            12,  # R hip
            11,  # L hip
            13,  # L knee
            15,  # L ankle
            10,  # R Wrist
            8,  # R Elbow
            7,  # L Elbow
            9,  # L Wrist
        ]

        for ann in anns:

            if 'keypoints' not in ann or type(ann['keypoints']) != list:
                continue

            if ann['num_keypoints'] == 0:
                continue

            else:
                kp_raw = np.array(ann['keypoints'])
                v = kp_raw[2::3]


            if 'bbox' in ann:

                x, y, w, h = ann['bbox']
                box = [x, y, w, h]

                if sum(v == 2) >= min_vis and h > min_max_height:

                    if np.all(v[points_other_than_faceshoulder] == 0):
                        continue

                    else:
                        image = self.save_img(box,ann,img)
                        image = image.reshape(-1)

                        if len(self.images)==0:
                            self.images = image
                        else:
                            self.images = np.vstack((self.images,image))
                            print(self.images.shape)
                        print('successfully saved! count : {}'.format(self.count))
                        self.count += 1
                        if self.count % 2000 == 0:
                            np.save('images_{}'.format(self.idx),self.images)
                            print('saved images_{}.npy'.format(self.idx))
                            self.images = np.array([])
                            self.idx += 1

            else:
                continue

    def save_img(self,box,ann,img):

        x_1, y_1, x_2, y_2, w, h = int(box[0]), int(box[1]), int(box[2]+box[0]), int(box[3]+box[1])\
            , int(box[2]), int(box[3])
        digit_length = len(str(ann['image_id']))
        diff = 12-digit_length
        image_id = str(0)*diff + str(ann['image_id'])

        path = '/Users/hanjoonchoe/Desktop/hmr2.0-master/coco/train2014' \
            '/COCO_train2014_{}.jpg'.format(image_id)
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = img[np.max((0,y_1-20)):y_2+20,np.max((0,x_1-20)):x_2+20]

        img = self.preprocessing_image(img)

        return img



    def person(self,annFile):

        annFile = annFile
        coco = COCO(annFile)
        catIds = coco.getCatIds(catNms=['person'])
        imgIds = coco.getImgIds(catIds=catIds)
        idx = 0
        dict = {}
        self.size = len(imgIds)
        for i in range(len(imgIds)):
            img = coco.loadImgs(imgIds[i])[0]
            annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
            anns = coco.loadAnns(annIds)
            self.select_images(anns,img)

        file = open('images_{}.pkl'.format(self.idx), 'wb')
        pickle.dump(self.dict, file)
        file.close()
        self.dict = {}
        print('saved images_{}.pkl'.format(self.idx))


def resize_img(img, scale_factor):
    new_size = (np.floor(np.array(img.shape[0:2]) * scale_factor)).astype(int)
    new_img = cv2.resize(img, (new_size[1], new_size[0]))
    # This is scale factor of [height, width] i.e. [y, x]
    actual_factor = [
        new_size[0] / float(img.shape[0]), new_size[1] / float(img.shape[1])
    ]
    return new_img, actual_factor


def scale_and_crop(image, scale, center, img_size):
    image_scaled, scale_factors = resize_img(image, scale)
    # Swap so it's [x, y]
    scale_factors = [scale_factors[1], scale_factors[0]]
    center_scaled = np.round(center * scale_factors).astype(np.int)

    margin = int(img_size / 2)
    image_pad = np.pad(
        image_scaled, ((margin, ), (margin, ), (0, )), mode='edge')
    center_pad = center_scaled + margin
    # figure out starting point
    start_pt = center_pad - margin
    end_pt = center_pad + margin
    # crop:
    crop = image_pad[start_pt[1]:end_pt[1], start_pt[0]:end_pt[0], :]
    proc_param = {
        'scale': scale,
        'start_pt': start_pt,
        'end_pt': end_pt,
        'img_size': img_size
    }

    return crop, proc_param

def normalize(img):
    img = 2 * ((img / 255.) - 0.5)
    return img