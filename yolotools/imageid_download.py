 #!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import hashlib
import json
import argparse
import base64
import os
import re
from multiprocessing import Pool
import requests
from tqdm import tqdm
from comfunc.tools import read_xlsx,check_dir

def base64_encode(img_path):
    with open (img_path,'rb') as f:
        base64_encode = base64.b64encode(f.read())
    return base64_encode.decode()

def getallfiles(path):
    allfile = []
    for dirpath, dirnames, filenames in os.walk(path):
        for dir in dirnames:
            allfile.append(os.path.join(dirpath, dir))
        for name in filenames:
            allfile.append(os.path.join(dirpath, name))

    vaild_path = []
    for item in allfile:
        if item.endswith('jpg') or item.endswith('jpeg') or item.endswith('png') or item.endswith('webp'):
            vaild_path.append(item)
    return vaild_path

def download_url(image_path,save_name):
    try:
        resp = requests.get(image_path)
    except:
        return
    md = hashlib.md5(resp.content).hexdigest()
    # image_path = os.path.join(save_name, '{}.jpg'.format(md))
    image_path = os.path.join(save_name, '{}'.format(image_path.replace('/', '_')))
    with open(image_path, 'wb') as f:
        f.write(resp.content)

def read_csv(csv_path):
    all_img_list = []
    with open(csv_path,'r') as f:
        for line in f.readlines():
            all_img_list.extend(line.split(','))
    return all_img_list

def read_csv_file(csv_path):
    all_img_list = []
    data_list = os.listdir(csv_path)
    if os.path.exists('{}/{}'.format(csv_path, '.DS_Store')):
        os.remove('{}/{}'.format(csv_path, '.DS_Store'))
    for item in data_list:
        with open('{}/{}'.format(csv_path,item), 'r') as f:
            lines = f.readlines()
            for line in lines:
                    imageId = line.strip().split(',')[0]
                    compileX = re.compile(r"[a-zA-Z0-9]")
                    imageId = compileX.findall(imageId)
                    imageId = ''.join(imageId)
                    all_img_list.append((imageId))
    return all_img_list
def read_excel_file(xlsx_file):
    return read_xlsx(xlsx_file)["imageId"].apply(lambda x:x.split("\"")[1]).to_list()
def download_imageid(image_path,save_name):
    url = "https://gleaner.tongdun.cn/resource/image?type=image_id&image_id={}&timestamp={}&token={}"
    salt = "7c8c01906b3faeaafebb0d6fc9296f08"
    timestamp = int(round(time.time() * 1000))
    m2 = hashlib.md5()
    str_salt = str(timestamp) + "_" + str(salt)
    m2 = hashlib.md5(str_salt.encode(encoding='utf-8'))
    token = m2.hexdigest()
    imageUrl = url.format(image_path, str(timestamp), token)
    try:
        resp = requests.get(imageUrl)
        image_path = '{}/{}.jpg'.format(save_name, image_path)
        open(image_path, 'wb').write(resp.content)
    except:
        print('error: ',imageUrl)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--img_file', type=str, default='/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/品牌模型优化数据/图像识别品牌【侵权品牌vlone】.xlsx', help='image file')
    parser.add_argument('-s','--save_name', type=str, default='/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/品牌模型优化数据/vlone', help='save json name')
    opt = parser.parse_args()

    image_file = opt.img_file
    save_name = opt.save_name
    check_dir(save_name)

    all_img_list = read_excel_file(image_file)
    #print(all_img_list[:100])
    num_process = 16
    pool = Pool(num_process)
    results = []
    pbar = tqdm(total=len(all_img_list))
    def update(*a):
        pbar.update()

    for image_path in all_img_list:
        results.append(pool.apply_async(download_imageid,args=(image_path,save_name),callback=update))

    pool.close()
    pool.join()

