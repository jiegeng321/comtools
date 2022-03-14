# coding:utf-8
##添加文本方向 检测模型，自动检测文字方向，0、90、180、270
from math import *

import numpy as np
from PIL import Image
import os, sys
from glob import glob
from tqdm import tqdm
sys.path.append("ocr")
from angle.predict import predict as angle_detect  ##文字方向检测


test_img_path = 'final_test/*.jpg'
save_path = test_img_path.split('/')[0] + '_rotated'
if not os.path.exists(save_path):
    os.makedirs(save_path)
paths = glob(test_img_path)
print('----------start rotating imgs----------')
for pic in tqdm(paths[:]):
    im = Image.open(pic)
    for i in range(2):
        img = np.array(im.convert('RGB'))
        angle = angle_detect(img=np.copy(img))  ##文字朝向检测
        #print('The angel of this character is:', angle)
        im = Image.fromarray(img)
        #print('Rotate the array of this img!')
        if angle == 90:
            im = im.transpose(Image.ROTATE_90)
        elif angle == 180:
            im = im.transpose(Image.ROTATE_180)
        elif angle == 270:
            im = im.transpose(Image.ROTATE_270)
    im.save(save_path+'/'+ pic.split('/')[-1].split('.')[0]+'_2.jpg', quality=100)





