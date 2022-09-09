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


big_dir = Path("/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/brand_labeled/empty")
#big_dir = Path("/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/brand_labeled/empty")
small_dir = Path("/data01/xu.fx/dataset/CARTOON_DATASET/fordeal_test_data/val/empty/")
move_to_dir = "/data01/xu.fx/dataset/CARTOON_DATASET/fordeal_test_data/val/tmp"
if not os.path.exists(move_to_dir):
    os.makedirs(move_to_dir)
big_list = [p for p in big_dir.rglob("*.*") if is_img(p)]
small_list_name = [p.name for p in small_dir.rglob("*.*") if is_img(p)]
exec_num = 0
for big_file in tqdm(big_list):
    if big_file.name in small_list_name:
        if move_to_dir:
            # shutil.move(big_file,os.path.join(move_to_dir,big_file.name))
            # shutil.move(big_file.with_suffix(".xml"), os.path.join(move_to_dir, big_file.with_suffix(".xml").name))
            print(big_file.name)
            print("copy to",move_to_dir)
        else:
            os.remove(big_file)
        exec_num += 1
print("exec num:",exec_num)

