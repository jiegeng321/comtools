#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import argparse
from pathlib import Path
import requests
import json
import cv2
import os
from tqdm import tqdm
# import numpy as np
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
# import matplotlib.pyplot as plt
# import random
import warnings
import shutil
#from model.config import logo_id_to_name
#from multiprocessing import Pool, Manager
warnings.filterwarnings('ignore')
#import time
from multiprocessing import Pool, Manager
from copy import deepcopy
image_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal1012_1025_for_logo_data/brand-tm/bmw/"
out_pred_img_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal1012_1025_for_logo_data/brand-tm/bmw_logoness"
out_pred_img_crop_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal1012_1025_for_logo_data/brand-tm/bmw_logoness_crop"
WORKERS = 3

if out_pred_img_dir:
    if not os.path.exists(out_pred_img_dir):
        os.makedirs(out_pred_img_dir)
    #else:
        #shutil.rmtree(out_pred_img_dir)
        #os.makedirs(out_pred_img_dir)

base_url = 'http://10.58.10.51:38088'

BINARY_API_ENDPOINT = "{}/v2/logoness_rec".format(base_url)
image_list = [p for p in Path(image_dir).rglob('*.*')][:]
print(len(image_list))

find_num = 0
different_num = 0
total_num = len(image_list)
#random.shuffle(image_list)
def iou(box1,box2):
    x01,y01,x02,y02=box1
    x11, y11, x12, y12 = box2
    lx = abs((x01+x02)/2-(x11+x12)/2)
    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
    sax = abs(x01-x02)
    sbx = abs(x11 - x12)
    say = abs(y01 - y02)
    sby = abs(y11 - y12)
    if lx<=(sax+sbx)/2 and ly<=(say+sby)/2:
        bxmin = max(box1[0],box2[0])
        bymin = max(box1[1],box2[1])
        bxmax = min(box1[2],box2[2])
        bymax = min(box1[3],box2[3])
        bwidth = bxmax-bxmin
        bhight = bymax-bymin
        inter = bwidth*bhight
        union = (box1[2]-box1[0])*(box1[3]-box1[1])+(box2[2]-box2[0])*(box2[3]-box2[1])-inter
        return inter/union
    else:
        return 0
def yolotxt_to_voc(h,w,yolobox):
    x1 = yolobox[0] * w - yolobox[2] * w / 2
    y1 = yolobox[1] * h - yolobox[3] * h / 2
    x2 = yolobox[0] * w + yolobox[2] * w / 2
    y2 = yolobox[1] * h + yolobox[3] * h / 2
    return [x1,y1,x2,y2]
def det_server_func(image_list):

    for image_path in tqdm(image_list[:]):
        if image_path.name == ".DS_Store":
            continue
        #print(image_path)
        image_path = str(image_path)
        img = cv2.imread(image_path)
        img_copy = img.copy()
        h, w, _ = img.shape
        file_name = image_path.split('/')[-1]
        payload = {'imageId': '00003'}
        file_temp = [('img', (file_name, open(image_path, 'rb'), 'image/jpeg'))]
        resq1 = requests.request
        try:
            response = resq1("POST", BINARY_API_ENDPOINT, data=payload, files=file_temp)
        except Exception as e:
            print(e)
            print(file_name)
            continue
        result = json.loads(response.text)

        #print(result)
        if 'res' in result:
            pred = result['res']
            box_pred_list = []
            if pred==[]:
                brand_name = "empty"
            else:
                for logo_instance in pred:
                    logo = logo_instance['logo_name']
                    box = logo_instance['box']
                    score = logo_instance['score']
                    x1 = box['x1']
                    y1 = box['y1']
                    x2 = box['x2']
                    y2 = box['y2']
                    box_pred_list.append([x1,y1,x2,y2])
                    cv2.rectangle(img, (x1, y1), (x2, y2), [0, 0, 255], 2)
                    cv2.putText(img, logo, (x1, y1-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 255], 1, cv2.LINE_AA)
                    cv2.putText(img, str(round(score, 3)), (x1, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 255], 1,
                                cv2.LINE_AA)
                brand_name = logo
            if out_pred_img_crop_dir:
                if not os.path.exists(out_pred_img_crop_dir):
                    os.makedirs(out_pred_img_crop_dir)
                for index, box in enumerate(box_pred_list):
                    crop = img_copy[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                    save_name = os.path.join(out_pred_img_crop_dir, file_name + "_"+ str(index) + ".jpg")
                    try:
                        cv2.imwrite(save_name, crop)
                    except Exception as e:
                        print(e)
            if out_pred_img_dir:
                save_dir = os.path.join(out_pred_img_dir,brand_name)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                try:
                    cv2.imwrite(os.path.join(save_dir, file_name), img)
                except:
                    print("problem file: ",os.path.join(save_dir, file_name))
        else:
            print("error",result,file_name)


pool = Pool(processes=WORKERS)
for i in range(0, WORKERS):
    imgs = image_list[i:len(image_list):WORKERS]
    pool.apply_async(det_server_func, (imgs,))
pool.close()
pool.join()
