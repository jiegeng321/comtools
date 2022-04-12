#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
from comfunc.tools import check_dir
import os
import shutil
from tqdm import tqdm

donot_need_char = [","," ","_","(",")","。","'","’","&","-","~"]
src_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/已标注 /BaumeetMercier"
renamed_dir = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/D11/checked/"
check_dir(renamed_dir,delete=False)
for file in tqdm(os.listdir(src_dir)):
    if file[0]==".":
        continue
    renamed = file
    for char in donot_need_char:
        renamed = renamed.replace(char,"")
    rename_file = "baumeetmercier_"+renamed
    shutil.copy(os.path.join(src_dir,file),os.path.join(renamed_dir,rename_file))