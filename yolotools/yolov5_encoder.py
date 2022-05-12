#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import shutil

from comfunc.tools import check_dir, is_img
from pathlib import Path
import requests
import json, os
from tqdm import tqdm
import numpy as np
import torch
from multiprocessing import Pool, Manager
import time
resq = requests.request
def data_simple_write(img_list):
    save_json_dict = {}
    i = 0
    for image_path in tqdm(img_list):
        i += 1
        file_name = image_path.name
        try:
            payload = {'imageId': '00003'}
            file_temp = [('img', (file_name, open(image_path, 'rb'), 'image/jpeg'))]
            response = resq("POST", url, data=payload, files=file_temp)
            result = json.loads(response.text)
        except Exception as e:
            print(e)
            print(file_name)
            time.sleep(1)
            continue
        if 'res' in result and result['res'] != None:
            pred = result['res']
            save_json_dict[str(image_path)] = pred
        if i%5000==0:
            save_label_json = os.path.join(dst_json_dir, str(os.getpid()) + ".json")
            with open(save_label_json, 'w') as f:
                json.dump(dict(save_json_dict), f)
                print("saved success",i, save_label_json)
    save_label_json = os.path.join(dst_json_dir,str(os.getpid())+".json")
    with open(save_label_json, 'w') as f:
        json.dump(dict(save_json_dict), f)
        print("saved success",save_label_json)

def data_simple_read(json_dict):
    imgs_ = []
    features_ = []
    for img, feature in json_dict.items():
        features_.append(feature)
        imgs_.append(img)
    features_total=[]
    imgs_total = []
    th=70000
    if len(features_)>th:
        features_total.append(features_[:th])
        imgs_total.append(imgs_[:th])
        features_total.append(features_[th:])
        imgs_total.append(imgs_[th:])
    else:
        features_total.append(features_)
        imgs_total.append(imgs_)
    for imgs,features in zip(imgs_total,features_total):
        features = torch.as_tensor(features)
        print("start mul")
        mul = features.mm(features.t())
        similar_num = 0
        print(mul.shape)
        print("start move similar imgs")
        for index in tqdm(range(mul.shape[0])):
            if index == 0:
                continue
            try:
                if torch.any(mul[:index, index] > sim_th):
                    shutil.move(str(imgs[index]), dst_dir)
                    similar_num += 1
            except:
                continue
        del mul, features
        #similar_num_list.append(similar_num)
        print("similar num:",similar_num)
if __name__=="__main__":
    READ = True
    sim_th = 0.9988
    src_dir = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/checked"
    # src_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/yolo_model_test_img/"
    dst_dir = check_dir(os.path.join(str(Path(src_dir).parent), str(Path(src_dir).name) + "_similar"))
    dst_json_dir = check_dir(os.path.join(str(Path(src_dir).parent), str(Path(src_dir).name) + "_similar_json"))
    url = "http://192.168.6.148:1002/get_feature"
    WORKERS = 10
    if not READ:
        print("start imgs read.")
        img_list = [i for i in tqdm(Path(src_dir).rglob("*.*")) if is_img(i)]
        print("imgs read done.")
        pool = Pool(processes=WORKERS)
        img_list = sorted(img_list)
        block = int(len(img_list) / WORKERS)

        for i in range(WORKERS):
            img_list_ = img_list[i * block:(1 + i) * block]
            #imgs = img_list[i:len(img_list):WORKERS]
            pool.apply_async(data_simple_write, (img_list_,))
        pool.close()
        pool.join()
        # print("similar nums:",similar_num_list,len(similar_num_list))
        # print("total nums:", sum(similar_num_list))
    else:
        json_dict_total = {}
        for i,json_dict_path in enumerate(Path(dst_json_dir).rglob("*.json")):
            if i <2:continue
            with open(json_dict_path, 'r') as f:
                json_dict = json.load(f)
            #json_dict_total.update(json_dict)
            print("load",i,json_dict_path,"success")
            print("img-features pair num:",len(json_dict),i,json_dict_path.name)
            data_simple_read(json_dict)
            del json_dict
        #data_simple_read(json_dict_total)


