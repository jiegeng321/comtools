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
src_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/标注任务-圣诞老人补标圣诞帽 已完成"
renamed_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/标注任务-圣诞老人补标圣诞帽_rename"
check_dir(renamed_dir,delete=False)
for file in tqdm(os.listdir(src_dir)):
    if file[0]==".":
        continue
    # for char in donot_need_char:
    #     renamed = renamed.replace(char,"")
    # rename_file = "baumeetmercier_"+renamed
    if "checked_" in file:
        rename_file = file.replace("checked_","")
    else:
        rename_file = file
    shutil.copy(os.path.join(src_dir,file),os.path.join(renamed_dir,rename_file))