# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:27:06 2020

@author: Administrator
"""
import shutil

import numpy as np
import os
import json
import io
import PIL.Image
from tqdm import tqdm
import cv2
#设置图片和txt标注路径，转成的json格式存在图片路径下的outputs，可直接用标注精灵打开
data_path = 'traffic_light_test_img'
prelabel_path = 'traffic_light_test_img_label'

def check(img_path,label_path):
    img_list = os.listdir(img_path)
    label_list = os.listdir(label_path)
    for label in label_list:
        if not os.path.exists(img_path + '/' + label.replace('.txt', '.jpg')):
            shutil.rmtree(label_path + '/' + label)
    for img in img_list:
        if not os.path.exists(label_path + '/' + img.replace('.jpg', '.txt')):
            shutil.rmtree(img_path + '/' + img)
#check(data_path,prelabel_path)

list_im = os.listdir(data_path)
dataset_part = data_path #+ '_prelabel'
if not os.path.exists('./'+dataset_part):
    os.makedirs('./'+dataset_part)
if not os.path.exists('./' + dataset_part + '/outputs'):
    os.makedirs('./' + dataset_part + '/outputs')
data = json.load(open('./template.json'))
list_path = os.listdir(prelabel_path)

for i in tqdm(range(0,len(list_path))):
    obj = []
    data['path'] = 'C:\\Users\\Administrator\\Desktop\\txt_to_json\\'+dataset_part+'\\'+list_path[i].replace('.txt','.jpg')
    for j,line in enumerate(open(prelabel_path + '/'+list_path[i],"r")):
        if j==1:
            if line=='':
                break
        points = line.split(',')
        obj.append({"name": "traffic_light","bndbox": {"xmin": int(points[0]), "ymin": int(points[1]), "xmax": int(points[2]), "ymax": int(points[3])}})
    data['outputs']['object'] = obj
    with open('./'+dataset_part+'/outputs/'+list_path[i].replace('.txt','.json'),'w',encoding='utf-8') as f:
      json.dump(data,f,ensure_ascii=False)
































































