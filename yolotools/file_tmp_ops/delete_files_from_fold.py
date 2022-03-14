#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from pathlib import Path

from tqdm import tqdm

from func.funcxml import readxml
import cv2
import random
from func.print_color import bcolors
import os
import shutil
from func.check import check_dir
#voc格式目录
# yolo_dir = Path("/data01/xu.fx/dataset/comb_data/yolo_dataset_comb_173bs_294ks/")
# annotaion_dir = yolo_dir / "Annotations"
# img_dir = yolo_dir / "JPEGImages/train/images"


#voc格式目录,xml与图片在同一目录
#yolo_dir = Path("/data01/xu.fx/dataset/PATTERN_DATASET/comb_data/checked/")
be_deleted_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/tmp"
src_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/brand_labeled/van_cleef_arpels"
move_to_dir = None#"/data01/xu.fx/dataset/PATTERN_DATASET/white_data/pattern_white_total_2nd/adidas"
src_list = os.listdir(src_dir)
for dst in tqdm(src_list):
    for de in os.listdir(be_deleted_dir):
        #if dst.split(".")[0] in de.split(".")[0]:

        #if os.path.exists(os.path.join(src_dir,de)):
        if dst.split("_")[-1] == de.split("_")[-1]:
            if move_to_dir:
                shutil.copy(os.path.join(src_dir,dst),os.path.join(move_to_dir,dst))
            else:
                os.remove(os.path.join(src_dir,dst))

