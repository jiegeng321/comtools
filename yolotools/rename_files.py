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
src_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/reebok花纹收集+标注"
renamed_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/reebok花纹收集+标注_rename"
check_dir(renamed_dir,delete=True)
for file in tqdm(os.listdir(src_dir)):
    if file[0]==".":
        continue
    rename_file = "rebook_"+file.replace(",","").replace("。","").replace(" ","").replace("_","")
    shutil.copy(os.path.join(src_dir,file),os.path.join(renamed_dir,rename_file))