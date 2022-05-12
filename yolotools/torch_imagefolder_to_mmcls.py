#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import os
from pathlib import Path
from comfunc.tools import is_img
from tqdm import tqdm
import random
import json
torch_imagefolder_dir = "/data02/xu.fx/dataset/PATTERN_DATASET/comb_data/clsdataset_pattern_v3/"
save_name = "clsdataset_pattern_13bs_22ks"
dataset_txt_save_dir = "/data01/xu.fx/xdcv-classification/configs/data/"
dataset_label_info_save_dir = "/data01/xu.fx/xdcv-classification/configs/label_info/"
labels = {'goyard_h': 0, 'michaelkors_h': 1, 'coach_h': 2, 'versace_h': 3, 'celine_h': 4, 'gucci_h': 5, 'issey_miyake_h': 6, 'adidas_h': 7, 'mcm_h': 8, 'christian_dior_h': 9, 'fendi_h': 10, 'lv_h_2': 11, 'burberry_h': 12, 'lv_h': 13, 'christian_dior_h_2': 14, 'normal': 15}
upper_labels = {'goyard_h': 0, 'michaelkors_h': 0, 'coach_h': 0, 'versace_h': 0, 'celine_h': 0, 'gucci_h': 0, 'issey_miyake_h': 0, 'adidas_h': 0, 'mcm_h': 0, 'christian_dior_h': 0, 'fendi_h': 0, 'lv_h_2': 0, 'burberry_h': 0, 'lv_h': 0, 'christian_dior_h_2': 0, 'normal': 1}
save_label_info_json = {"label_info":labels,"upper_label": {"label_map": upper_labels,"label_upper_name":["reject","accept"]}}
with open(os.path.join(dataset_label_info_save_dir,save_name+".json"), 'w') as f:
    json.dump(save_label_info_json, f)
print("label info json saved")
train_txt = os.path.join(dataset_txt_save_dir,save_name+"_train.txt")
val_txt = os.path.join(dataset_txt_save_dir,save_name+"_val.txt")
train_txt_w = open(train_txt,"w")
val_txt_w = open(val_txt,"w")
for train_val in ["train","val"]:
    print("process data:",train_val)
    class_dirs = os.listdir(torch_imagefolder_dir+train_val)
    for cls in tqdm(class_dirs):
        if cls in labels:
            if train_val=="train":
                imgs = [i for i in Path(os.path.join(torch_imagefolder_dir,train_val,cls)).glob("*.*") if is_img(i)]
                for img in imgs:
                    if "," in str(img): continue
                    train_txt_w.write(str(img)+","+str(labels[cls])+"\n")
            elif train_val=="val":
                imgs = [i for i in Path(os.path.join(torch_imagefolder_dir,train_val,cls)).glob("*.*") if is_img(i)]
                for img in imgs:
                    if "," in str(img): continue
                    val_txt_w.write(str(img)+","+str(labels[cls])+"\n")
        else:
            print(cls,"not in labels")
train_txt_w.close()
val_txt_w.close()
#
# img_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_labeled/michaelkors_h"
# img_dir1 = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_labeled/goyard_h"
# img_dir2 = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_labeled/issey_miyake_h/"
# img_dir3 = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_labeled/christian_dior_h/"
# class0_list = [i for i in Path(img_dir).glob("*.*") if is_img(i)]
# class1_list = [i for i in Path(img_dir1).glob("*.*") if is_img(i)]
# class2_list = [i for i in Path(img_dir2).glob("*.*") if is_img(i)]
# class3_list = [i for i in Path(img_dir3).glob("*.*") if is_img(i)]
# random.shuffle(class0_list)
# random.shuffle(class1_list)
# random.shuffle(class2_list)
# random.shuffle(class3_list)
# train_val_rate = [0.8,0.2]
# with open(os.path.join(txt_dir,"pattern_train.txt"),"w") as f:
#     total_num = len(class0_list)
#     train_num = int(total_num*train_val_rate[0])
#     #val_num = total_num - train_num
#     for path in class0_list[:train_num]:
#         f.write(str(path)+",0")
#     for path in class1_list[:train_num]:
#         f.write(str(path)+",1")
# with open(os.path.join(txt_dir,"pattern_val.txt"),"w") as f:
#     total_num = len(class0_list)
#     train_num = int(total_num*train_val_rate[0])
#     #val_num = total_num - train_num
#     for path in class0_list[train_num:]:
#         f.write(str(path)+",0")

