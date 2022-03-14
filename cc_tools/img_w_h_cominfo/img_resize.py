# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:27:06 2020

@author: Administrator
"""

import numpy as np
import os
from tqdm import tqdm
import cv2
import pandas as pd

percent = 0.9
img_path = 'G:\COMDATA\insurance_train_data_ocr_paddle_add_gen\img'
list_im = os.listdir(img_path)
w_h_ratio = []
for im in tqdm(list_im):
    img = cv2.imread(img_path+'/'+im,1)
    w_h_ratio.append(img.shape[1]/img.shape[0])
df = pd.Series(w_h_ratio)
quant = df.quantile(q=percent)
print(df.describe())
print('%0.2f quantile num: %f'%(percent,quant))
print('suggest width %d , suggest height %d'%(32,np.ceil(quant)*32))





















































