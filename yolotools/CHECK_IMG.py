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
import sys
sys.path.append("..")
from comfunc.tools import is_img
import cv2
import numpy as np
from pathlib import Path
warnings.filterwarnings("error", category=UserWarning)
from skimage import io

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

def same_mv_func(files,md5_list,dhash_list,same_md5_num,same_hash_num):
    for file_i in tqdm(files):
        file_dir = os.path.join(src_dir,file_i)
        fr = open(str(file_i), 'rb')
        data = fr.read()
        md5 = hashlib.md5(data).hexdigest().strip()
        if md5 in md5_list:
            if not os.path.exists(same_dir):
                os.makedirs(same_dir)
            shutil.move(str(file_i), same_dir)
            print("%s is same md5" % file_i.name)
            same_md5_num.value += 1
            continue
        else:
            md5_list.append(md5)
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
                    #print("diff:",diff)
                    if diff <= hash_th:
                        if not os.path.exists(hash_dir):
                            os.makedirs(hash_dir)
                        shutil.move(str(file_i), hash_dir)
                        print("%s is same %s" % (file_i.name,hashs))
                        same_hash_num.value += 1
                        add_dhas = 0
                        break
                if add_dhas:
                    dhash_list.append(dhas)
def get_size_func(files):
    w_list,h_list = [] ,[]
    for file_i in tqdm(files):
        try:
            img = Image.open(str(file_i))
        except:
            continue
        w, h = img.size[:2]
        w_list.append(w)
        h_list.append(h)
    return np.mean(w_list),np.mean(h_list)
def png_fix_func(files):
    for img in tqdm(files):
        if img.suffix in [".png",".PNG"]:
            image = io.imread(img)
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
            cv2.imencode('.png', image)[1].tofile(img)

def bad_img_mv_func(files,num_dict):
    for file_i in tqdm(files):

        #error img
        try:
            img = Image.open(str(file_i))
            form = img.format
        except:
            if not os.path.exists(error_dir):
                os.makedirs(error_dir)
            shutil.move(str(file_i), error_dir)
            print("%s is error file" % file_i.name)
            num_dict["error_num"] += 1
            continue
        #error img

        if str(file_i)[0]==".":
            if not os.path.exists(error_dir):
                os.makedirs(error_dir)
            shutil.move(str(file_i), error_dir)
            print("%s is error file" % file_i.name)
            num_dict["error_num"] += 1

        #too small size img

        if min(img.size) <= min_size:
            if not os.path.exists(small_dir):
                os.makedirs(small_dir)
            shutil.move(str(file_i), small_dir)
            print("%s is size <%d pixels" % (file_i.name, min_size))
            num_dict["small_num"] += 1
            continue

        #webp img
        if form=="WEBP":
            if not os.path.exists(webp_dir):
                os.makedirs(webp_dir)
            print(f"{str(file_i)} is WEBP file, has trans")
            shutil.move(str(file_i), webp_dir)
            img.save(str(file_i))
            num_dict["webp_num"] += 1

        # gif img
        if form=="GIF" or file_i.suffix=="gif":
            if not os.path.exists(gif_dir):
                os.makedirs(gif_dir)
            shutil.move(str(file_i), gif_dir)
            print("%s is gif" % file_i.name)
            num_dict["gif_num"].value += 1
            continue

        #other wraning img
        try:
            img.load()
        except:
            if not os.path.exists(warning_dir):
                os.makedirs(warning_dir)
            shutil.move(str(file_i), warning_dir)
            num_dict["wraning_num"] += 1
            print("%s is warning" % file_i.name)
            continue

        #exif img
        try:
            img._getexif()
        except:
            if not os.path.exists(exif_dir):
                os.makedirs(exif_dir)
            shutil.move(str(file_i), exif_dir)
            img.save(str(file_i))
            num_dict["exif_num"] += 1
            print("%s is EXIF file, has trans" % file_i.name)
            continue

        #other invalid img
        try:
            img = Image.open(str(file_i))
            img.verify()
        except Exception as e:
            print('Invalid image',e)
            if not os.path.exists(invalid_dir):
                os.makedirs(invalid_dir)
            shutil.move(str(file_i), invalid_dir)
            num_dict["invalid_num"] += 1
            print("%s is invalid" % file_i.name)
            continue

def bad_img_mv(files):

    num_dict = Manager().dict()
    num_dict["gif_num"] = 0
    num_dict["error_num"] = 0
    num_dict["wraning_num"] = 0
    num_dict["invalid_num"] = 0
    num_dict["small_num"] = 0
    num_dict["exif_num"] = 0
    num_dict["webp_num"] = 0
    #files = [p for p in src_dir.glob("*.*") if is_img(p)]
    pool = Pool(processes=WORKERS_bad_img_mv)
    for i in range(0, WORKERS_bad_img_mv):
        files_ = files[i:len(files):WORKERS_bad_img_mv]
        pool.apply_async(bad_img_mv_func, (files_,num_dict,))
    pool.close()
    pool.join()
    print("bad images:")
    print(num_dict)

def same_img_mv(files):
    md5_list = Manager().list()
    dhash_list = Manager().list()
    same_md5_num = Manager().Value("same_md5_num",0)
    same_hash_num = Manager().Value("same_hash_num", 0)

    pool = Pool(processes=WORKERS_md5_mv)
    for i in range(0, WORKERS_md5_mv):
        files_ = files[i:len(files):WORKERS_md5_mv]
        pool.apply_async(same_mv_func, (files_,md5_list,dhash_list,same_md5_num,same_hash_num,))
    pool.close()
    pool.join()
    print("total same_md5_num: ", same_md5_num.value)
    print("total same_hash_num: ", same_hash_num.value)

if __name__ == "__main__":
    src_dir = Path("/data01/xu.fx/dataset/LOGO_DATASET/white_data/万维误检数据0705")
    min_size = 10
    hashs = None#"totalhash"  # ahash,dhash,phash,totalhash
    hash_th = None#1
    hash_size = (8, 8)
    WORKERS = 10
    split = 10

    same_dir = os.path.join(src_dir.parent, src_dir.name + "_bad_images",
                            "same_md5")  # src_dir + "_bad_images/same_md5"
    hash_dir = os.path.join(src_dir.parent, src_dir.name + "_bad_images",
                            "same_hash")  # src_dir + "_bad_images/same_dhash"
    gif_dir = os.path.join(src_dir.parent, src_dir.name + "_bad_images", "gif")  # src_dir + "_bad_images/gif"
    error_dir = os.path.join(src_dir.parent, src_dir.name + "_bad_images", "error")  # src_dir + "_bad_images/error"
    warning_dir = os.path.join(src_dir.parent, src_dir.name + "_bad_images",
                               "warning")  # src_dir + "_bad_images/warning"
    invalid_dir = os.path.join(src_dir.parent, src_dir.name + "_bad_images",
                               "invalid")  # src_dir + "_bad_images/invalid"
    small_dir = os.path.join(src_dir.parent, src_dir.name + "_bad_images", "small")  # src_dir + "_bad_images/small"
    webp_dir = os.path.join(src_dir.parent, src_dir.name + "_bad_images", "webp")  # src_dir + "_bad_images/webp"
    exif_dir = os.path.join(src_dir.parent, src_dir.name + "_bad_images", "exif")  # src_dir + "_bad_images/exif"

    WORKERS_bad_img_mv = WORKERS
    WORKERS_md5_mv = WORKERS
    files = sorted([p for p in src_dir.rglob("*.*") if is_img(p)])
    print(len(files))
    #png_fix_func(files)
    bad_img_mv(files)
    same_img_mv(files)
    # random.shuffle(files)
    # w,h = get_size_func(files)
    # print(w,h)

    # if split:
    #     for i in range(split):
    #         block = int(len(files)/split)
    #         files_ = files[i*block:(1+i)*block]
    #         bad_img_mv(files_)
    #         same_img_mv(files_)
    # else:
    #     bad_img_mv(files)
    #     same_img_mv(files)

