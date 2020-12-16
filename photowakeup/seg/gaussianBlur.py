import cv2
import numpy as np
import os

def second_contours(src , img):
    contours,_ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    print('contours num : {}'.format(len(contours)))

    for i, c in enumerate(contours):
        # Calculate the area of each contour
        area = cv2.contourArea(c)

        # Ignore contours that are too small or too large
        if area < 1e2: #or 1e5 < area:
            continue

        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.drawContours(src, contours, i, (1, 1, 1), 3)
        #cv.drawContours(src, [box], 0, (255, 0, 0), 1)

        # cv.imwrite('output.jpg', src)

    return src

def compare_concat(img, src):
    idx = np.array((src[:, :, 0] + src[:, :, 1] + src[:, :, 2]) == 0, dtype=int)
    img = np.multiply(np.expand_dims(idx, 2), img)
    img = np.array(img + src, dtype=np.uint8)

    return img

def main(img_seg_rgb , img_seg_rgba, input_path , output_path):

    gray = cv2.cvtColor(img_seg_rgb, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    #edges = cv2.Canny(bw, 50, 150, apertureSize=3)
    src = np.zeros(img_seg_rgb.shape)
    print(img_seg_rgb.shape)
    src = second_contours(src, bw)  # edge 추출 1

    # blur
    img2 = cv2.imread(input_path)
    blur = cv2.GaussianBlur(img2, (5, 5), 5)
    img2 = blur * src
    img_test = img_seg_rgb
    img2 = compare_concat(img_test, img2)

    rgba = cv2.cvtColor(img2, cv2.COLOR_RGB2RGBA)
    cv2.imwrite(output_path, rgba)

