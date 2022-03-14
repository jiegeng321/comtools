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
#voc格式目录
# yolo_dir = Path("/data01/xu.fx/dataset/comb_data/yolo_dataset_comb_173bs_294ks/")
# annotaion_dir = yolo_dir / "Annotations"
# img_dir = yolo_dir / "JPEGImages/train/images"


#voc格式目录,xml与图片在同一目录
yolo_dir = Path("/data01/xu.fx/dataset/LOGO_DATASET/D15_wew/checked/")
annotaion_dir = yolo_dir
img_dir = yolo_dir

file_name = '*.xml'

fix_str = [".jpg", '.JPG', '.png', '.PNG', '.jpeg', '.JPEG']
dst_anno_files = [file for file in annotaion_dir.glob(file_name)]
random.shuffle(dst_anno_files)
print("img num: ", len(dst_anno_files))
find = 0
for index_,anno_file in enumerate(dst_anno_files):

    boxes = readxml(str(anno_file))
    #print("-" * 60)
    print("sample_index: %d/%d" % (index_, len(dst_anno_files)))
    for s in fix_str:
        img_name = anno_file.name.replace('.xml', s)
        img_path = img_dir / img_name
        if img_path.exists():
            class_names=[]
            for index,obj_i in enumerate(boxes):
                if obj_i[0]==None:
                    continue
                class_name = obj_i[0].split("-")[0]
                class_names.append(class_name)
            if class_names==[]:
                class_names.append("empty")
            class_name = max(class_names, key=class_names.count)
            if class_name=="ac/dc":
                class_name="acdc"
            class_name=class_name.lower().replace(' ', '').replace("'", "").replace("’", "").replace(".", "").replace('&', '').replace('_', '')
            shutil.copy(img_path, "/data01/xu.fx/dataset/LOGO_DATASET/D15_wew/tmp_rename/" + class_name+"_"+img_name)
            shutil.copy(anno_file, "/data01/xu.fx/dataset/LOGO_DATASET/D15_wew/tmp_rename/" + class_name+"_"+anno_file.name)
            find += 1
                #     break
                # else:
                #     pass
print(find)
            # if find==0:
            #     shutil.copy(img_path, "/data01/xu.fx/dataset/comb_data/tmp_rename/" + img_name)
            #     shutil.copy(anno_file, "/data01/xu.fx/dataset/comb_data/tmp_rename/" + anno_file.name)
            #     print(class_name)








