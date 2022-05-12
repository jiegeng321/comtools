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
be_deleted_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/brand_labeled/spibelt/"
src_dir = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/checked"
move_to_dir = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/tmp"
src_list = os.listdir(src_dir)
be_delete_list = [i.replace("checked_","") for i in os.listdir(be_deleted_dir)]
de_num = 0
for dst in tqdm(src_list):
    if dst.split(".")[-1]=="xml":continue
    if dst in be_delete_list:
        #print(dst)
        if move_to_dir:
            shutil.move(os.path.join(src_dir,dst),os.path.join(move_to_dir,dst))
            print("move to",move_to_dir)
            de_num += 1
        else:
            os.remove(os.path.join(src_dir,dst))
print(de_num)
    # for de in os.listdir(be_deleted_dir):
    #     #if dst.split(".")[0] in de.split(".")[0]:
    #
    #     #if os.path.exists(os.path.join(src_dir,de)):
    #     if dst.split("_")[-1] == de.split("_")[-1]:
    #         if move_to_dir:
    #             shutil.copy(os.path.join(src_dir,dst),os.path.join(move_to_dir,dst))
    #             print("move to",move_to_dir)
    #         else:
    #             os.remove(os.path.join(src_dir,dst))

