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
from comfunc.tools import check_dir
from pathlib import Path
#voc格式目录
# yolo_dir = Path("/data01/xu.fx/dataset/comb_data/yolo_dataset_comb_173bs_294ks/")
# annotaion_dir = yolo_dir / "Annotations"
# img_dir = yolo_dir / "JPEGImages/train/images"

import random
#voc格式目录,xml与图片在同一目录
#yolo_dir = Path("/data01/xu.fx/dataset/PATTERN_DATASET/comb_data/checked/")
be_deleted_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/已完成-白样本误检测试check任务-花纹/"
src_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/white_test_labeled/empty"
move_to_dir = check_dir("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/tmp3/")
dst_list = os.listdir(src_dir)
white_num = 0


src_list = [i for i in Path(src_dir).rglob("*.*")]
get = 0
get1 = 0
be_deleted = [i for i in Path(be_deleted_dir).rglob("*.*")]
for de in tqdm(be_deleted):
    #print(de)
    if "误检" in str(de.parent.name):
        #get+=1
        continue
    #get1+=1
    #print(str(de))
    # #print(de)

    #if de.name in
    for sr in src_list:
        #print(de.name,de.name)
        if de.name == sr.name:
            if random.random()<=100:
            #print(de.name,sr.name)
                shutil.move(str(sr),str(move_to_dir))
                get += 1
    print(get)


