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
src_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_white_data_for_logo"
select_out_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal测试集整合 1129"
dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/logo_white_data_from_fordeal_high_quality"

select_out_folder = os.listdir(select_out_dir)
for folder in tqdm(os.listdir(select_out_dir)):
    if os.path.isdir(os.path.join(select_out_dir,folder)):
        for file in os.listdir(os.path.join(src_dir,folder)):
            if not is_img(file):
                continue
            if file in os.listdir(os.path.join(select_out_dir,folder)):
                continue
            else:
                dst_path = os.path.join(dst_dir,folder)
                check_dir(dst_path)
                shutil.copy(os.path.join(src_dir,folder,file),dst_path)

