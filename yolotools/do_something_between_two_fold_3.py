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


big_dir = Path("/data02/xu.fx/dataset/CARTOON_DATASET/comb_data/yolodataset_cartoon_53bs_55ks_0824/JPEGImages/val/images")
small_dir = Path("/data02/xu.fx/dataset/CARTOON_DATASET/comb_data/yolodataset_cartoon_53bs_55ks_0824/JPEGImages/val/labels")
move_to_dir = "/data01/xu.fx/dataset/CARTOON_DATASET/fordeal_test_data/val/labels_xml"
if not os.path.exists(move_to_dir):
    os.makedirs(move_to_dir)
tmp = {}
big_list = [str(p.with_suffix(".txt").name).replace(".txt","") for p in big_dir.rglob("*")]
for i in big_list:
    if i not in tmp:
        tmp[i] = 1
    else:
        print(i)
print(len(set(big_list)))
# small_list_name = [str(p.with_suffix(".txt").name).replace(".txt","") for p in small_dir.rglob("*")]
# print(len(set(small_list_name)))
# exec_num = 0
# for big_file in tqdm(big_list):
#     if big_file not in small_list_name:
#         print(big_file)
#         # if move_to_dir:
#         #     shutil.copy(big_file,os.path.join(move_to_dir,big_file.name))
#         #     print("copy to",move_to_dir)
#         # else:
#         #     os.remove(big_file)
#         exec_num += 1
# print("exec num:",exec_num)
#
