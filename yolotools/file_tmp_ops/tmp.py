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
from tqdm import tqdm
#voc格式目录
# yolo_dir = Path("/data01/xu.fx/dataset/comb_data/yolo_dataset_comb_173bs_294ks/")
# annotaion_dir = yolo_dir / "Annotations"
# img_dir = yolo_dir / "JPEGImages/train/images"


#voc格式目录,xml与图片在同一目录
yolo_dir = Path("/data01/xu.fx/dataset/CARTOON_DATASET/fordeal_test_data/val/images").rglob("*.*")
for i in tqdm(yolo_dir):
    if len(i.name.split("_"))<2:
        mid = "other"
    else:
        mid = i.name.split("_")[0]
    if not (Path("/data01/xu.fx/dataset/CARTOON_DATASET/fordeal_test_data/val/images_tmp") / mid).exists():
        (Path("/data01/xu.fx/dataset/CARTOON_DATASET/fordeal_test_data/val/images_tmp") / mid).mkdir()
    shutil.copy(str(i),str(Path("/data01/xu.fx/dataset/CARTOON_DATASET/fordeal_test_data/val/images_tmp") / mid))
# annotaion_dir = yolo_dir
# img_dir = yolo_dir
#
# file_name = '*.xml'
#
# fix_str = [".jpg", '.JPG', '.png', '.PNG', '.jpeg', '.JPEG']
# dst_anno_files = [file for file in annotaion_dir.glob(file_name)]
# random.shuffle(dst_anno_files)
# print("img num: ", len(dst_anno_files))
#
# for index_,anno_file in enumerate(dst_anno_files):
#     find = 0
#     boxes = readxml(str(anno_file))
#     print("-" * 60)
#     print("sample_index: %d/%d" % (index_, len(dst_anno_files)))
#     for s in fix_str:
#         img_name = anno_file.name.replace('.xml', s)
#         img_path = img_dir / img_name
#         if img_path.exists():
#             for index,obj_i in enumerate(boxes):
#                 class_name = obj_i[0]
#                 if class_name.split("-")[0]=="PIAGET":
#                     shutil.copy(img_path,"/data01/xu.fx/dataset/comb_data/tmp_rename/Piaget_"+img_name.split("_")[-1])
#                     shutil.copy(anno_file, "/data01/xu.fx/dataset/comb_data/tmp_rename/Piaget_" + anno_file.name.split("_")[-1])
#                     print(class_name)
#                     find = 1
#                     break
#                 else:
#                     pass
#             if find==0:
#                 shutil.copy(img_path, "/data01/xu.fx/dataset/comb_data/tmp_rename/" + img_name)
#                 shutil.copy(anno_file, "/data01/xu.fx/dataset/comb_data/tmp_rename/" + anno_file.name)
#                 print(class_name)
#
#
#
#
#
#
#
#
