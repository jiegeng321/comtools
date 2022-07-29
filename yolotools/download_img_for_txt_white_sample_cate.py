#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from pathlib import Path

import requests

from comfunc.funcxml import readxml
import cv2
import random
from comfunc.print_color import bcolors
import os
import shutil
from comfunc.check import check_dir
import ast
txt_paths = [
    "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0417-0424.txt",
            "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0410-0417.txt",
"/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0401-0409.txt",
             ]
txt_paths = txt_paths[::-1]
dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_white_data_for_pattern_0621"
need_num = 100000
#pattern_list = ['gucci_h', 'michael_kors', 'coach_h', 'adidas_h', 'lv_h', 'fendi_h', 'nike_h', 'versace_h', 'christian dior_h', 'goyard_h', 'burberry_h', 'Issey miyake_h', 'christian dior_h', 'celine_h']

# if not os.path.exists(dst_dir):
#     os.makedirs(dst_dir)
data = []
for txt_path in txt_paths:
    with open(txt_path, "r") as f:
        print(txt_path)
        data += f.readlines()
print("total lines:",len(data))
downloaded_images = 0
for index,line in enumerate(data[10010:]):
    downloaded_per_list = 0
    dict_brand = ast.literal_eval(line)
    if "imageCommodityData" not in dict_brand or "category" not in dict_brand or "finalCheckResult" not in dict_brand:
        continue
    #if dict_brand["finalCheckResult"]=="Reject":#Reject
    img_list = dict_brand["imageCommodityData"]
    #print(index,":",img_list)
    #if ("凉鞋" in dict_brand["category"] or "拖鞋" in dict_brand["category"] or "高跟鞋" in dict_brand["category"]) \
    #        and dict_brand["finalCheckResult"]=="Reject":
    if "鞋" in dict_brand["category"] and dict_brand["finalCheckResult"] == "Reject":
        for img in img_list:
            try:
                url = img["textData"]
                print_name = "empty"
                auto_brand = "empty"
                img_name = url.split("/")[-1]
                resq = requests.get(url)
                if len(resq.content) > 250:
                    img_out = os.path.join(dst_dir,auto_brand)
                    if not os.path.exists(img_out):
                        os.makedirs(img_out)
                    open(os.path.join(img_out,print_name+"_"+img_name), 'wb').write(resq.content)
                    downloaded_images += 1
                    downloaded_per_list += 1
                    if downloaded_images>=need_num:
                        print("images is enough %d"%downloaded_images)
                        exit()
                else:
                    continue
            except Exception as e:
                print(e)
                continue
    print(index,"this list has %d images,have downloaded %d/%d,total need download %d/%d" %(len(img_list),downloaded_per_list,len(img_list),downloaded_images,need_num))





