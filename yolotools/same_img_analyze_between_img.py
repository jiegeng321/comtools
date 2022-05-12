#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import random
from tqdm import tqdm
import hashlib
from PIL import Image
import shutil
from multiprocessing import Pool, Manager
import os
import warnings
from comfunc.tools import is_img
import cv2
import numpy as np
from pathlib import Path
warnings.filterwarnings("error", category=UserWarning)

def dHash(img, hash_size):
    width, high = hash_size
    img = cv2.imread(img)
    img = cv2.resize(img, (width+1, high), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    for i in range(high):
        for j in range(high):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

def aHash(img, hash_size):
    width, high = hash_size
    img = cv2.imread(img)
    img = cv2.resize(img, (width, high), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    s = 0
    hash_str = ''
    for i in range(width):
        for j in range(high):
            s = s + gray[i, j]
    avg = s / (width*high)
    for i in range(width):
        for j in range(high):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str
def pHash(img_file, hash_size):
    width, high = hash_size
    img = cv2.imread(img_file, 0)
    img = cv2.resize(img, (width, high), interpolation=cv2.INTER_CUBIC)
    img = np.float32(img)
    vis1 = cv2.dct(cv2.dct(img))
    img_list = vis1.flatten()
    avg = sum(img_list) * 1. / len(img_list)
    avg_list = ['0' if i > avg else '1' for i in img_list]
    #return ''.join(['%x' % int(''.join(avg_list[x:x + 4]), 2) for x in range(0, width * high, 4)])
    return ''.join(avg_list)

def campHash(hash1, hash2):
    n = 0
    if len(hash1) != len(hash2):
        return -1
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n
def same_md5(files):
    md5_list = []
    same_num = 0
    try:
        for file_i in files:
            fr = open(str(file_i), 'rb')
            data = fr.read()
            md5 = hashlib.md5(data).hexdigest().strip()
            if md5 in md5_list:
                same_num += 1
                #print("%s is same md5" % file_i.name)
                continue
            else:
                md5_list.append(md5)
    except:
        return None
    return same_num
def same_mv_func(files):
    same_num = 0
    dhash_list = []
    try:
        for file_i in files:
            if hash_th!=None and hashs!=None:
                if hashs == "dhash":
                    dhas = dHash(str(file_i), hash_size)
                elif hashs == "phash":
                    dhas = pHash(str(file_i), hash_size)
                elif hashs == "ahash":
                    dhas = aHash(str(file_i), hash_size)
                else:
                    dhas = aHash(str(file_i), hash_size) + dHash(str(file_i), hash_size) + pHash(str(file_i), hash_size)
                #print("hash:",dhas)
                add_dhas = 1
                if len(dhash_list) == 0:
                    dhash_list.append(dhas)
                else:
                    for dhas_ex in dhash_list:
                        diff = campHash(dhas_ex,dhas)
                        if diff <= hash_th:
                            same_num += 1
                            add_dhas = 0
                            break
                    if add_dhas:
                        dhash_list.append(dhas)
    except:
        return None
    return same_num

if __name__ == "__main__":
    hashs = "phash"  # ahash,dhash,phash,totalhash
    hash_th = 2
    hash_size = (16, 16)
    total_num = []
    same_md5_num = []
    same_hash_num = []
    for dir in tqdm(os.listdir("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_data_list_clean/")):#fordeal_data_list_clean
        src_dir = Path("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_data_list_clean") / dir
        files = [p for p in src_dir.rglob("*.*") if is_img(p)]
        same_md5_num_ = same_md5(files)
        same_hash_num_ = same_mv_func(files)
        if same_md5_num_ is not None and same_hash_num_ is not None:
            total_num.append(len(files))
            same_md5_num.append(same_md5(files))
            same_hash_num.append(same_mv_func(files))
    print(len(total_num),np.mean(total_num),np.mean(same_md5_num),np.mean(same_hash_num))
