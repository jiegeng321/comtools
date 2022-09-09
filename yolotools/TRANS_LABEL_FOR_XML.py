#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from pathlib import Path
from comfunc.funcxml import readxml
import cv2
import random
from comfunc.print_color import bcolors
import os
import shutil
from comfunc.tools import check_dir,is_img
from tqdm import tqdm
import numpy as np
from pascal_voc_writer import Writer
from multiprocessing import Pool, Manager

WORKERS = 32

anno_list = [i for i in Path("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/标注任务-圣诞老人补标圣诞帽 已完成").rglob("*.xml")]

# trans_dict = {"armani-":"ARMANI-","balmain-":"BALMAIN-","chanel-":"CHANEL-","coach-":"COACH-","fendi-":"FENDI-",
#               "gucci-":"GUCCI-","nba-":"NBA-","nike-":"NIKE-","nfl-":"NFL-","puma-":"PUMA-","versace-":"VERSACE-",
#               "burberry-":"BURBERRY-","balenciaga-":"BALENCIAGA-","prada-":"PRADA-","lacoste-":"LACOSTE-",
#               "supreme-":"SUPREME-"}
# trans_dict = {"Spider-Man":"Spider Man","yoda":"Yoda","宗教-上帝-十字架":"上帝十字架","宗教-犹太教-六角形":"犹太教六角形","宗教-南瓜灯":"南瓜灯",
#               "宗教-圣诞树":"圣诞树","宗教-圣诞老人":"圣诞老人","宗教-圣诞帽子":"圣诞帽子"}
trans_dict = {"圣诞帽":"圣诞帽子"}
in_or_eq = "eq"
def trans_label_func(anno_list,trans_num):
    print("img num: ", len(anno_list))
    for anno_file in tqdm(anno_list):
        # anno_file = anno_file.with_suffix('.xml')
        if not anno_file.exists(): continue
        boxes,width,height = readxml(str(anno_file))
        # print(boxes,width,height)
        if not boxes or boxes==[]: continue
        find = 0
        info = []
        for box in boxes:
            if len(box)<5:continue
            class_name = box[0]
            for k,v in trans_dict.items():
                if in_or_eq=="in":
                    if k in class_name:
                        find = 1
                        class_name = class_name.replace(k,v)
                        if v in trans_num:
                            trans_num[v] += 1
                        else:
                            trans_num[v] = 1
                else:
                    if k == class_name:
                        find = 1
                        class_name = class_name.replace(k, v)
                        if v in trans_num:
                            trans_num[v] += 1
                        else:
                            trans_num[v] = 1
            info.append([class_name, box[1], box[2], box[3], box[4]])
        if find == 1:
            try:
                # img = cv2.imread(str(anno_file))
                # h, w, _ = img.shape
                writer = Writer(anno_file.name.replace("&", ''), width,height)
                for i in info:
                    writer.addObject(*i)
                writer.save(anno_file)
            except Exception as e:
                print(e)
                continue

trans_num = Manager().dict()
pool = Pool(processes=WORKERS)
for i in range(0, WORKERS):
    imgs = anno_list[i:len(anno_list):WORKERS]
    pool.apply_async(trans_label_func, (imgs,trans_num,))
pool.close()
pool.join()
# trans_num = {}
# trans_label_func(anno_list,trans_num)
print("has trans num",trans_num)
