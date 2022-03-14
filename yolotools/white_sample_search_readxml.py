#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

# 给定src_dir的标注文件夹，以8:2的形式自动划分训练集和测试集，进入dst_dir的制定目录，只分图片，后续结合yololabels制作训练集

import os
import random
import glob
import shutil
from pathlib import Path
from func.path import ospathjoin
from func.check import check_dir
from tqdm import tqdm
import pandas as pd
from xml.etree import ElementTree as ET
def read_xml_label(annotion_path):
    res = []

    try:
        root = ET.parse(annotion_path).getroot()
    except:
        assert "the file is not found."
    else:
        bboxes = root.find("object")
        for index, subtree in enumerate(root.iter('object')):
            label = subtree.find("name").text
            res.append(label)
    return res

annotion_path = "/data01/xu.fx/dataset/open_dataset/openlogo/Annotations"
dst_dir = "/data01/xu.fx/dataset/white_sample_factory/raw_white_images_from_open_dataset/openlogo/"
open_dataset_dir = "/data01/xu.fx/dataset/open_dataset/openlogo/JPEGImages/"

files = os.listdir(annotion_path)
check_dir(dst_dir)
logo1000 = pd.read_csv("/data01/xu.fx/dataset/open_dataset/LOGO1000.csv")
logo1000_list = logo1000["品牌"].tolist()
logo1000_list_low = []
for i in logo1000_list:
    logo1000_list_low.append(i.replace(" ","").replace("'","").replace("-","").replace("&","").replace("\n","").replace(".","").lower())
print(logo1000_list_low)
need_logo = []
for f in tqdm(files):
    exist = 0
    logos = read_xml_label(os.path.join(annotion_path,f))
    for logo in logos:
        #print(label)
        #for logo in label:
        if logo.split("_")[0].replace(" ","").replace("'","").replace("-","").replace("&","").replace("\n","").replace(".","").lower() in logo1000_list_low or logo=="adidas1":
            exist = 1
            break
    if exist != 1:
        need_logo.append(logos[0])
        print(logos[0])
        shutil.copy(os.path.join(open_dataset_dir,f.replace("xml","jpg")),os.path.join(dst_dir,logos[0].split("_")[0]+"_"+f.replace("xml","jpg")))
print(len(set(need_logo)))

