import cv2
import numpy as np
from matplotlib import pyplot as plt
a = cv2.imread('SMPL.png')

b = a[:,:,0]==255
c = a[:,:,1]==255
d = a[:,:,2]==255

b = np.logical_and(a[:,:,0]==255,a[:,:,1]==255,a[:,:,2]==255)

cv2.imwrite('ds.png',abs(b*255-255))
