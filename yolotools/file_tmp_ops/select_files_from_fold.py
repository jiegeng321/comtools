#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from pathlib import Path

from tqdm import tqdm

from comfunc.funcxml import readxml
import cv2
import random
from comfunc.print_color import bcolors
import os
import shutil
from comfunc.check import check_dir
#voc格式目录
# yolo_dir = Path("/data01/xu.fx/dataset/comb_data/yolo_dataset_comb_173bs_294ks/")
# annotaion_dir = yolo_dir / "Annotations"
# img_dir = yolo_dir / "JPEGImages/train/images"


#voc格式目录,xml与图片在同一目录
#yolo_dir = Path("/data01/xu.fx/dataset/PATTERN_DATASET/comb_data/checked/")
be_deleted_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/white_sample_for_pattern/Versace-误检-pred/versace/"
src_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/white_sample_for_pattern/Versace-误检/"
move_to_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/white_data/pattern_white_total_2nd/versace"
dst_list = os.listdir(src_dir)
white_num = 0
for de in tqdm(os.listdir(be_deleted_dir)):
    if de in dst_list:
        if move_to_dir:
            if not os.path.exists(move_to_dir):
                os.makedirs(move_to_dir)
            white_num += 1
            shutil.copy(os.path.join(src_dir,de),os.path.join(move_to_dir,de))
        else:
            os.remove(os.path.join(be_deleted_dir,de))
print("get white num:",white_num)
