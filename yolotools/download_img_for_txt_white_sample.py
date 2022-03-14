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
txt_path = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/1229-1231.txt"
dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_white_data_for_pattern_1229-1231"
need_num = 100000
#pattern_list = ['gucci_h', 'michael_kors', 'coach_h', 'adidas_h', 'lv_h', 'fendi_h', 'nike_h', 'versace_h', 'christian dior_h', 'goyard_h', 'burberry_h', 'Issey miyake_h', 'christian dior_h', 'celine_h']

# if not os.path.exists(dst_dir):
#     os.makedirs(dst_dir)
with open(txt_path,"r") as f:
    data = f.readlines()
print("total lines:",len(data))
downloaded_images = 0
for index,line in enumerate(data):
    downloaded_per_list = 0
    dict_brand = ast.literal_eval(line)
    #if dict_brand["finalCheckResult"]=="Reject":#Reject
    img_list = dict_brand["imageCommodityData"]
    #print(index,":",img_list)

    for img in img_list:
        try:
            auto_result = img["autoCheckResult"]
            final_result = img["finalCheckResult"]

            if auto_result == "Reject" and final_result == "Accept" and "图像识别品牌【侵权/品牌" in img["ruleHit"]:
                print(img)
                url = img["textData"]
                auto_brand_raw = list(set(img["ruleHit"].split(",")))
                auto_brand = []
                for brand in auto_brand_raw:
                    if "图像识别品牌【侵权/品牌" in brand:
                        auto_brand.append(brand)

                # for b in auto_brand:
                #     #print(b.split("/")[-1].split("】")[0])
                #     if b.split("/")[-1].split("】")[0] in pattern_list:
                #         print(b)
                # continue
                print_name = auto_brand[0].split("/")[-1].split("】")[0]
                if len(auto_brand)>=2:
                    for auto in auto_brand[1:]:
                        print_name += "_"+auto.split("/")[-1].split("】")[0]
                auto_brand = max(auto_brand,key=auto_brand.count)
                auto_brand = auto_brand.split("/")[-1].split("】")[0]
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





