#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import pandas as pd
import os

import requests

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
#data_path = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/仿品样本库图片.csv"
crop_path = "/data01/xu.fx/dataset/LOGO_DATASET/high_imitation_test/total"
ori_images_path = "/data01/xu.fx/dataset/LOGO_DATASET/high_imitation_test/total_original_images"
# data = pd.read_csv(data_path)
# print(data)
def download(name,dir):
    try:
        img_name = name.split("_")[1]
    except Exception as e:
        print(e)
        return
    for end in ['.jpg','.png','.jpeg']:
        try:
            url = "https://s3.forcloudcdn.com/item/images/dmc/"+img_name+end
            resq = requests.get(url)
            if len(resq.content) > 500:
                img_out = os.path.join(ori_images_path,dir,dir+"_"+img_name+end)
                if not os.path.exists(os.path.join(ori_images_path,dir)):
                    os.mkdir(os.path.join(ori_images_path,dir))
                open(img_out, 'wb').write(resq.content)
                print(img_out)
        except Exception as e:
            print(e)
            continue
for dir in os.listdir(crop_path)[54:]:
    if dir==".DS_Store":
        continue
    for di in os.listdir(os.path.join(crop_path,dir)):
        if di == ".DS_Store":
            continue
        if os.path.isdir(os.path.join(crop_path,dir,di)):
            for d in os.listdir(os.path.join(crop_path,dir,di)):
                if d == ".DS_Store":
                    continue
                download(d,dir.lower().replace(" ","_"))
        else:
            download(di, dir.lower().replace(" ", "_"))
