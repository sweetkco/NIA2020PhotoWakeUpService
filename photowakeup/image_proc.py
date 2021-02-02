import cv2
import os
from PIL import Image
import numpy as np

def crop_image(img, rect):
    x, y, w, h = rect[0]

    left = abs(x) if x < 0 else 0
    top = abs(y) if y < 0 else 0
    right = abs(img.shape[1] - (x + w)) if x + w >= img.shape[1] else 0
    bottom = abs(img.shape[0] - (y + h)) if y + h >= img.shape[0] else 0

    if img.shape[2] == 4:
        color = [0, 0, 0, 0]
    else:
        color = [0, 0, 0]
    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    x = x + left
    y = y + top

    return new_img[y:(y + h), x:(x + w), :]


def image_processing(img):

    rect_path = img.replace('.%s' % (img.split('.')[-1]), '_rect.txt')
    rects = np.loadtxt(rect_path, dtype=np.int32)
    print(rects)

    if len(rects.shape) == 1:
        rects = rects[None]

    im = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    if im.shape[2] == 4:
        im = im / 255.0
        im[:,:,:3] /= im[:,:,3:] + 1e-8
        im = im[:,:,3:] * im[:,:,:3] + 0.5 * (1.0 - im[:,:,3:])
        im = (255.0 * im).astype(np.uint8)

    im = crop_image(im, rects)

    image_512 = cv2.resize(im, (512, 512))
    image_1024 = cv2.resize(im, (1024, 1024))

    return image_512,image_1024

def blurring(image):
    blurred_img = cv2.GaussianBlur(image, (21, 21), 0)
    mask = np.zeros(image.shape, np.uint8)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(gray.shape)
    thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(mask, contours, -1, (255, 255, 255), 2)
    output = np.where(mask == np.array([255, 255, 255]), blurred_img, image)
    return output

