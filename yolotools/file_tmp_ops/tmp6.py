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
import subprocess
src_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/check_fx数据已完成1217/"
#select_out_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal测试集整合 1129"
#dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/logo_white_data_from_fordeal_high_quality"

subprocess.call(f"cd {src_dir}", shell=True)
#select_out_folder = os.listdir(select_out_dir)
for folder in tqdm(os.listdir(src_dir)):
    if "误检" in folder:
        print(folder)
        #print(subprocess.call(f"cp {src_dir}{folder}_pred/Annotations/* {src_dir}{folder}/", shell=True))

        print(subprocess.call(f"trash-put {src_dir}{folder}", shell=True))