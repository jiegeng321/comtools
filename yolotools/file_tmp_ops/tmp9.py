#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from pathlib import Path
from func.funcxml import readxml
import cv2
import random
from func.print_color import bcolors
import os
import shutil
from func.check import check_dir
from func.tools import is_img
from func.tools import check_dir
from tqdm import tqdm
src_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/brand_labeled_old"

select_out_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/机审正确/"

dst_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/brand_labeled_old_wrong/"
check_dir(dst_dir)
src_image_list = [p for p in Path(src_dir).rglob('*.*')]
select_out_image_list = [p for p in Path(select_out_dir).rglob('*.*')]
#select_out_folder = os.listdir(select_out_dir)
for file in tqdm(src_image_list):
    for select_out_file in select_out_image_list:
        if file.name.split("_")[-1] in select_out_file.name.split("_")[-1]:
            shutil.move(file,os.path.join(dst_dir,file.name))
#     if file.name.split("_") in select_out_list2:
#         if not os.path.exists(os.path.join(dst_dir,file.split("_")[0])):
#             os.makedirs(os.path.join(dst_dir,file.split("_")[0]))
#         shutil.copy(os.path.join(src_dir, file), os.path.join(dst_dir,file.split("_")[0],file))
#
# image_list = [p for p in Path(image_dir).rglob('*.*')]