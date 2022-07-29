#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from pathlib import Path

from tqdm import tqdm
from pathlib import Path
from comfunc.funcxml import readxml
import cv2
import random
from comfunc.tools import is_img
import os
import shutil
from comfunc.check import check_dir
#voc格式目录
# yolo_dir = Path("/data01/xu.fx/dataset/comb_data/yolo_dataset_comb_173bs_294ks/")
# annotaion_dir = yolo_dir / "Annotations"
# img_dir = yolo_dir / "JPEGImages/train/images"


big_dir = Path("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal误检check")
small_dir = Path("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal数据check误检0719已完成")
move_to_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal误检数据20220721"
if not os.path.exists(move_to_dir):
    os.makedirs(move_to_dir)
big_list = [p for p in big_dir.rglob("*.*") if is_img(p)]
small_list_name = [p.name for p in small_dir.rglob("*.*") if is_img(p)]
exec_num = 0
for big_file in tqdm(big_list):
    if big_file.name in small_list_name:
        if move_to_dir:
            shutil.copy(big_file,os.path.join(move_to_dir,big_file.name))
            print("move to",move_to_dir)
        else:
            os.remove(big_file)
        exec_num += 1
print("exec num:",exec_num)

