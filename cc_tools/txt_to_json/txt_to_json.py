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

data_path = 'idcard_get_box_img'
prelabel_path = 'idcard_get_box_label'

list_im = os.listdir(data_path)
dataset_part = data_path + '_json_prelabel'
if not os.path.exists('./'+dataset_part):
    os.makedirs('./'+dataset_part)
#if not os.path.exists('./' + dataset_part + '/outputs'):
#    os.makedirs('./' + dataset_part + '/outputs')
data = json.load(open('./template.json'))
list_path = os.listdir(prelabel_path)

#print('resize images:')
#for im in tqdm(list_im):
#    img = cv2.imread(data_path+'/'+im,1)
#    img_re = resize_im(img, scale = 900, max_scale=1500)
#    cv2.imwrite('./'+data_path+'/'+im, img_re)

#print('txt to json:')

#for ctpn to json 01236745
for i in tqdm(range(0,len(list_path))):
    obj = []
    data['path'] = 'C:\\Users\\Administrator\\Desktop\\txt_to_json\\'+dataset_part+'\\'+list_path[i].split('.')[0] +'.jpg'
    for j,line in enumerate(open(prelabel_path + '/'+list_path[i].split('.')[0] +'.txt',"r",encoding='utf-8')): #设置文件对象并读取每一行文件
        points = line.split(',')
        obj.append({"name": "Chinese_ocr","polygon": {"x1": int(float(points[0])), "y1": int(float(points[1])),
                                                      "x2": int(float(points[2])), "y2": int(float(points[3])),
                                                      "x3": int(float(points[4])), "y3": int(float(points[5])),
                                                      "x4": int(float(points[6])), "y4": int(float(points[7]))


                                                      }})
    data['outputs']['object'] = obj
    with open('./'+dataset_part+'/'+list_path[i].split('.')[0]+'.json','w',encoding='utf-8') as f:
      json.dump(data,f,ensure_ascii=False)

'''
for i in tqdm(range(0,len(list_path))):
    obj = []
    data['path'] = 'C:\\Users\\Administrator\\Desktop\\txt_to_json\\'+dataset_part+'\\'+list_path[i].split('.')[0] +'.jpg'
    for j,line in enumerate(open(prelabel_path + '/'+list_path[i].split('.')[0] +'.txt',"r")): #设置文件对象并读取每一行文件
        points = line.split(',')
        obj.append({"name": "Chinese","polygon": {"x1": int(points[0]), "y1": int(points[1]), "x2": int(points[2]), "y2": int(points[3]), "x3": int(points[4]), "y3": int(points[5]), "x4": int(points[6]), "y4": int(points[7])}})
    data['outputs']['object'] = obj
    with open('./'+dataset_part+list_path[i].split('.')[0]+'.json','w',encoding='utf-8') as f:
      json.dump(data,f,ensure_ascii=False)
'''































































