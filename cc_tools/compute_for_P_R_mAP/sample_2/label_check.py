# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:27:06 2020

@author: Administrator
"""

import os
from tqdm import tqdm
def delete_unlabeled_image(im_path,la_path):
    image_path = os.listdir(im_path)
    del_num = 0
    for i in tqdm(range(len(image_path))):
        if not os.path.exists(la_path + '/'+image_path[i].split('.')[0] +'.txt'):
            os.remove(im_path + '/'+image_path[i].split('.')[0] +'.txt')
            del_num+=1
    print('%d unlabeled images are deleted done'%del_num)
delete_unlabeled_image("./val_label_txt","./detections")





































































