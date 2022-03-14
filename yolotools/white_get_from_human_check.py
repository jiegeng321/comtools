#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from pathlib import Path
from comfunc.funcxml import readxml
import cv2
import random
from comfunc.print_color import bcolors
import os
import shutil
from comfunc.check import check_dir

#通过人工check，获取误检的白样本cp
checked_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/第二批10w已完成1.4"
src_dirs = ["/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/合并模型所需白样本第一批6w-check任务",
           "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/合并模型所需白样本第二批10w-check任务",
         ]
dst_dir = "/data01/xu.fx/dataset/LOGO_DATASET/white_data/logo_white_data_from_fordeal_high_quality_4th/"
white_num = 0
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)
checked_dir_list = os.listdir(checked_dir)
for checked in checked_dir_list:
    white_brand_num = 0
    if checked.split("-")[-1]=="误检":
        if checked[0]==".":
            continue
    #if checked[-2:] == "误检":
        for file in os.listdir(os.path.join(checked_dir,checked)):
            if file[0] == ".":
                continue
            white_brand_num += 1
            #src_path = os.path.join(src_dir,file.replace(file.split("_")[0]+"_",""))
            # for src in src_dirs:
            #     src_path = os.path.join(src, file)
            #     #print(src_path)
            #     if os.path.exists(src_path):
            #         white_num += 1
                    #print(src_path)
            shutil.copy(os.path.join(checked_dir,checked,file),dst_dir)
        print("%s get white sample %d"%(checked,white_brand_num))
print("get total white num %d"%white_num)

