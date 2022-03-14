#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

# 检查文件名去除特殊字符,并放到新的目录下，图片和xml一起

import os
import random
import sys
import shutil
from pathlib import Path
from func.path import ospathjoin
from func.check import check_dir
from tqdm import tqdm

src_dir = "/data01/xu.fx/dataset/LOGO_DATASET/D15_wew/WewData"
dst_dir = "/data01/xu.fx/dataset/LOGO_DATASET/D15_wew/checked"
show_exist_brands = False

if show_exist_brands:
    file_list = os.listdir(dst_dir)
    exist_brand = []
    for f in tqdm(file_list):
        if f.split("_")[0] not in exist_brand:
            exist_brand.append(f.split("_")[0])
    print("checked dir exist brand:",len(exist_brand))
    sys.exit()

print("src_dir: ", src_dir)
def walk_file(find_dir='./', find_str=".xml"):
    for root, dirs, files in os.walk(find_dir, topdown=False):
        for name in files:
            file_str = os.path.join(root, name)
            if os.path.exists(file_str) and file_str.endswith(find_str):
                yield file_str
    return

src_list = os.listdir(src_dir)
for dir in src_list:
    if os.path.isdir(src_dir+'/'+dir):
        for f in os.listdir(src_dir+'/'+dir):
            if not os.path.exists(src_dir+'/'+f) and os.path.isfile(src_dir+'/'+dir+'/'+f):
                shutil.move(src_dir+'/'+dir+'/'+f, src_dir)
        shutil.rmtree(src_dir+'/'+dir)
dst_dir = Path(dst_dir)
check_dir(dst_dir)
file_num = len(os.listdir(src_dir))
print("file num is: ", file_num)
files = [file_xml for file_xml in walk_file(src_dir, ".xml")]
random.shuffle(files)
xml_nums = len(files)
print("xml num is: ", xml_nums)

# cp files
#val_nums = int(all_nums*0.2)
if xml_nums != (file_num)/2:
    print("is not pair")
else:
    print("is pair")
#print("val_num is: ", val_nums)
not_find_img_num = 0
for index, file_i in tqdm(enumerate(files)):

    xml_file = Path(file_i)
    file_i = file_i.split('/')[-1]
    if file_i[0]==".":
        print("find garbege ._*** file !!!")
        continue
    annotiaon_file = xml_file
    # annotiaon_file = ospathjoin([src_dir, file_i])
    fr = open(annotiaon_file, 'rb')
    data = fr.read()
    dst_annotion_file = ospathjoin([dst_dir, xml_file.parent.name.replace(' ', '').replace("'", "").replace("’", "").replace(".", "").replace('&', '').replace('_', '') +
                                    "_" + file_i[:-(len(file_i.split(".")[-1]))].replace('.', '').replace('-', '').replace('_', '').replace(',', '').replace(' ', '').replace('!', '').replace('&', '').replace('~', '').replace("'", "").replace("’", "")+"."+file_i.split(".")[-1]])
    # cp images
    xml_file_temp = str(xml_file)
    if os.path.exists(xml_file_temp.replace('.xml', '.jpg')):
        img_path = xml_file_temp.replace('.xml', '.jpg')
    elif os.path.exists(xml_file_temp.replace('.xml', '.jpeg')):
        img_path = xml_file_temp.replace('.xml', '.jpeg')
    elif os.path.exists(xml_file_temp.replace('.xml', '.JPG')):
        img_path = xml_file_temp.replace('.xml', '.JPG')
    elif os.path.exists(xml_file_temp.replace('.xml', '.JPEG')):
        img_path = xml_file_temp.replace('.xml', '.JPEG')
    elif os.path.exists(xml_file_temp.replace('.xml', '.png')):
        img_path = xml_file_temp.replace('.xml', '.png')
    elif os.path.exists(xml_file_temp.replace('.xml', '.PNG')):
        img_path = xml_file_temp.replace('.xml', '.PNG')
    else:
        print('Image File Not Found For ',xml_file_temp)
        not_find_img_num += 1
        continue
    #print(dst_annotion_file)
    with open(dst_annotion_file, 'wb') as fw:
        fw.write(data)
    fr.close()
    fimg = open(img_path, 'rb')
    img_data = fimg.read()
    dst_img_path = ospathjoin([dst_dir, xml_file.parent.name.replace(' ', '').replace("'", "").replace("’", "").replace(".", "").replace('&', '').replace('_', '') +
                               "_" + img_path.split('/')[-1][:-(len(img_path.split('/')[-1].split(".")[-1]))].replace('.', '').replace('-', '').replace('_', '').replace('!', '').replace(',', '').replace(' ', '').replace('&', '').replace('~', '').replace("'", "").replace("’", "")+"."+img_path.split('/')[-1].split(".")[-1]])
    with open(dst_img_path, 'wb') as fw:
        fw.write(img_data)
    fimg.close()
print("not find images: ",not_find_img_num)