# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:27:06 2020

@author: Administrator
"""

import numpy as np
import os
import json
import io
import PIL.Image
from tqdm import tqdm
import cv2
def resize_im(im, scale, max_scale=None):
    f = float(scale) / min(im.shape[0], im.shape[1])
    if max_scale != None and f * max(im.shape[0], im.shape[1]) > max_scale:
        f = float(max_scale) / max(im.shape[0], im.shape[1])
    return cv2.resize(im, None, None, fx=f, fy=f, interpolation=cv2.INTER_LINEAR)

data_path = 'test_with_ten_pic'
list_im = os.listdir(data_path)
for im in tqdm(list_im):
    img = cv2.imread(data_path+'/'+im,1)
    img_re = resize_im(img, scale = 900, max_scale=1500)
    cv2.imwrite('./'+data_path+'/'+im, img_re)


























































