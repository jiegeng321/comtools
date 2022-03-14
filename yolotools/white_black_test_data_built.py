#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import os
import random
import shutil
from comfunc.check import check_dir
from tqdm import tqdm

white_dir = "/data01/xu.fx/dataset/OPEN_DATASET/white_sample_factory/white_images_checked"
test_dir = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/yolo_dataset_comb_364bs_634ks/JPEGImages/test"
white_black_test_dir = test_dir.replace("test","white_black_test")


#若black_samples_num=None，则取测试集中全部数据，若白样本库按比例不足，则取白羊本库所有数据
black_samples_num = None
white_black_ratio = [0.7, 0.3]
random_seed = 2

check_dir(white_black_test_dir)
check_dir(os.path.join(white_black_test_dir, "images"))
check_dir(os.path.join(white_black_test_dir, "labels"))

test_files = os.listdir(os.path.join(test_dir,"images"))
if black_samples_num:
    test_num = black_samples_num
else:
    test_num = len(test_files)

empty_files = os.listdir(white_dir)
empty_num = len(empty_files)

need_empty_num = int(test_num*(white_black_ratio[0]/white_black_ratio[1]))
if empty_num<need_empty_num:
    need_empty_num=empty_num

random.seed(random_seed)
random.shuffle(test_files)
random.seed(random_seed)
random.shuffle(empty_files)
print("white samples num:", need_empty_num)
print("black samples num:", test_num)
print("coping white samples")
for i in tqdm(range(need_empty_num)):
    shutil.copy(os.path.join(white_dir,empty_files[i]),os.path.join(white_black_test_dir,"images"))
    with open(os.path.join(white_black_test_dir,"labels",empty_files[i][:-(len(empty_files[i].split('.')[-1]))]+'txt'),'w') as f:
        pass
print("coping black samples")
for j in tqdm(range(test_num)):
    if os.path.exists(os.path.join(test_dir,"images", test_files[j])) and os.path.exists(os.path.join(test_dir,"labels", test_files[j][:-(len(test_files[j].split('.')[-1]))]+'txt')):
        shutil.copy(os.path.join(test_dir,"images", test_files[j]), os.path.join(white_black_test_dir, "images"))
        shutil.copy(os.path.join(test_dir,"labels", test_files[j][:-(len(test_files[j].split('.')[-1]))]+'txt'), os.path.join(white_black_test_dir, "labels"))
    else:
        print("%s is not exist"%test_files[j])
