#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import cv2
from pathlib import Path
from func.tools import *
import shutil
src_dir = Path("/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/brand_total_raw_data")
img_list = [i for i in src_dir if is_img(i)]
size_th = 2000
dst_dir = "/data01/xu.fx/comtools/content_security_tools/locust_load_test/big_size"
for img in img_list:
    image = cv2.imread(img)
    if min(image.shape)<size_th:
        print(min(image.shape))
        check_dir(dst_dir)
        shutil.move(img,dst_dir)


