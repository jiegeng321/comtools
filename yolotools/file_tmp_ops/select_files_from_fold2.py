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
from pathlib import Path
#voc格式目录
# yolo_dir = Path("/data01/xu.fx/dataset/comb_data/yolo_dataset_comb_173bs_294ks/")
# annotaion_dir = yolo_dir / "Annotations"
# img_dir = yolo_dir / "JPEGImages/train/images"


#voc格式目录,xml与图片在同一目录
#yolo_dir = Path("/data01/xu.fx/dataset/PATTERN_DATASET/comb_data/checked/")
be_deleted_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_labeled"
src_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/fordeal_0930_raw_data"
move_to_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/tmp/"
dst_list = os.listdir(src_dir)
white_num = 0

src_list = [i for i in Path(src_dir).rglob("*.*")]

be_deleted = [i for i in Path(be_deleted_dir).rglob("*.*")]
for de in tqdm(be_deleted):
    #print(de)
    get = 0
    #if de.name in
    for sr in src_list:
        #print(de.name,de.name)
        if de.name == sr.name:
            print(de.name,de.name)
            shutil.copy(str(sr),str(de))
            get = 1
            break
    if get==0:
        shutil.move(str(de), move_to_dir)

