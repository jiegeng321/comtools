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
from comfunc.tools import is_img
from comfunc.tools import check_dir
from tqdm import tqdm
src_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_test_data_labeled/empty/"
select_out_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/tmp/"
# dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/check_wew_by_fx_raw"
# if not os.path.exists(dst_dir):
#     os.makedirs(dst_dir)

select_out_folder = os.listdir(select_out_dir)
for file in tqdm(os.listdir(src_dir)):
    if file in [i.split("_")[-1] for i in select_out_folder]:
        print(file)
        os.remove(os.path.join(src_dir, file))
    #
    #
    # exist = 0
    # for dir in select_out_folder:
    #     if dir == "empty":
    #         continue
    #     if os.path.exists(os.path.join(select_out_dir,dir,file)):
    #         exist = 1
    #         break
    # if not exist:
    #     shutil.copy(os.path.join(src_dir, file), os.path.join("/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_test_data_labeled/empty/", file))
    #         #os.remove(os.path.join(src_dir, file))
    #     print(os.path.join(src_dir, file))
            #shutil.copy(os.path.join(src_dir, file),os.path.join(dst_dir, file))


# select_out_folder = os.listdir(select_out_dir)
# for file in tqdm(os.listdir(src_dir)):
#     if not os.path.exists(os.path.join(select_out_dir, file)):
#         shutil.copy(os.path.join(src_dir, file), dst_dir)


# select_out_folder = os.listdir(select_out_dir)
# for folder in tqdm(os.listdir(src_dir)):
#     if os.path.isdir(os.path.join(src_dir,folder)):
#         if os.path.exists(os.path.join(select_out_dir,folder)):
#             continue
#         dst_path = os.path.join(dst_dir, folder)
#         shutil.copytree(os.path.join(src_dir,folder),dst_path)


