import os
import argparse
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm
import torchvision.transforms as transforms
from utils.transforms import transform_logits
from torch.utils.data import DataLoader

import networks
from datasets.simple_extractor_dataset import SimpleFolderDataset
import cv2

import gaussianBlur


dataset_settings = {
    'lip': {
        'input_size': [473, 473],
        'num_classes': 20,
        'label': ['Background', 'Hat', 'Hair', 'Glove', 'Sunglasses', 'Upper-clothes', 'Dress', 'Coat',
                  'Socks', 'Pants', 'Jumpsuits', 'Scarf', 'Skirt', 'Face', 'Left-arm', 'Right-arm',
                  'Left-leg', 'Right-leg', 'Left-shoe', 'Right-shoe']
    },
    'atr': {
        'input_size': [512, 512],
        'num_classes': 18,
        'label': ['Background', 'Hat', 'Hair', 'Sunglasses', 'Upper-clothes', 'Skirt', 'Pants', 'Dress', 'Belt',
                  'Left-shoe', 'Right-shoe', 'Face', 'Left-leg', 'Right-leg', 'Left-arm', 'Right-arm', 'Bag', 'Scarf']
    },
    'pascal': {
        'input_size': [512, 512],
        'num_classes': 7,
        'label': ['Background', 'Head', 'Torso', 'Upper Arms', 'Lower Arms', 'Upper Legs', 'Lower Legs'],
    }
}

def get_palette(num_cls):
    """ Returns the color map for visualizing the segmentation mask.
    Args:
        num_cls: Number of classes
    Returns:
        The color map
    """
    n = num_cls
    palette = [0] * (n * 3)
    for j in range(0, n):
        lab = j
        palette[j * 3 + 0] = 0
        palette[j * 3 + 1] = 0
        palette[j * 3 + 2] = 0
        i = 0
        while lab:
            palette[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
            palette[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
            palette[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
            i += 1
            lab >>= 3
    return palette

def get_arguments():
    """Parse all the arguments provided from the CLI.

    Returns:
      A list of parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Self Correction for Human Parsing")

    parser.add_argument("--dataset", type=str, default='pascal', choices=['lip', 'atr', 'pascal'])
    parser.add_argument("--model-restore", type=str, default='./model/exp-schp-201908270938-pascal-person-part.pth',
                        help="restore pretrained model parameters.")
    parser.add_argument("--gpu", type=str, default='0', help="choose gpu device.")
    parser.add_argument("--input-dir", type=str, default='../results', help="path of input image folderal.")
    parser.add_argument("--output-dir", type=str, default='../results', help="path of output image folder.")
    parser.add_argument("--logits", action='store_true', default=False, help="whether to save the logits.")
    return parser.parse_args()


def segmentation():
    args = get_arguments()
    gpus = [int(i) for i in args.gpu.split(',')]
    assert len(gpus) == 1
    if not args.gpu == 'None':
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu

    num_classes = dataset_settings[args.dataset]['num_classes']
    input_size = dataset_settings[args.dataset]['input_size']
    label = dataset_settings[args.dataset]['label']
    print("Evaluating total class number {} with {}".format(num_classes, label))

    model = networks.init_model('resnet101', num_classes=num_classes,pretrained=None)
    state_dict = torch.load(args.model_restore)['state_dict']
    from collections import OrderedDict
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:]  # remove `module.`
        new_state_dict[name] = v
    model.load_state_dict(new_state_dict)
    model.cuda()
    model.eval()

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.406, 0.456, 0.485], std=[0.225, 0.224, 0.229])
    ])
    dataset = SimpleFolderDataset(root=args.input_dir, input_size=input_size, transform=transform)
    dataloader = DataLoader(dataset)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    palette = get_palette(num_classes)
    with torch.no_grad():
        for idx,batch in enumerate(tqdm(dataloader)):
            image,meta = batch
            img_name = meta['name'][0]
            c = meta['center'].numpy()[0]
            s = meta['scale'].numpy()[0]
            w = meta['width'].numpy()[0]
            h = meta['height'].numpy()[0]

            output = model(image.cuda())
            upsample = torch.nn.Upsample(size=input_size, mode='bilinear', align_corners=True)
            upsample_output = upsample(output[0][-1][0].unsqueeze(0))
            upsample_output = upsample_output.squeeze()
            upsample_output = upsample_output.permute(1, 2, 0)  # CHW -> HWC

            logits_result = transform_logits(upsample_output.data.cpu().numpy(), c, s, w, h, input_size=input_size)
            parsing_result = np.argmax(logits_result, axis=2)
            ## test
            img_name = dataset.file_list[idx]
            img_path = os.path.join(dataset.root, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)

            output_img = Image.fromarray(np.asarray(parsing_result, dtype=np.uint8))
            output_img.putpalette(palette)

            beta = np.where(np.array(output_img) > 0, 1, 0)

            img[:, :, 0] = np.array(img[:, :, 0]) * beta
            img[:, :, 1] = np.array(img[:, :, 1]) * beta
            img[:, :, 2] = np.array(img[:, :, 2]) * beta

            rgba = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
            a = np.where(np.array(output_img) > 0, 255, 0)
            rgba[:, :, 3] = a
            rgb = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            gaussianBlur.main(rgb, rgba, img_path, os.path.join(args.output_dir, img_name[:-4] + '.jpg'))




segmentation()
