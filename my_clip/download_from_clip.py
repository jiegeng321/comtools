#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import requests,os,json
from tqdm import tqdm
from comfunc.tools import check_dir
clip_json = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/clipsubset (16).json"
dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/usb"
check_dir(dst_dir)
similarity = 0.3
need_num = 1000
def download_from_url(url,id,dst_dir):
    fix = str(url).split(".")[-1]
    try:
        resq = requests.get(url)
        if len(resq.content) > 250:
            open(os.path.join(dst_dir,str(id)+"."+fix), 'wb').write(resq.content)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
downloaded_num = 0
with open(clip_json, 'r') as f:
    clip_imgs = json.load(f)
print("total len:%d"%len(clip_imgs))
for img_dict in tqdm(clip_imgs):
    if float(img_dict["similarity"])>=similarity:
        if download_from_url(img_dict["url"],img_dict["id"],dst_dir):
            downloaded_num+=1
        if downloaded_num>=need_num:
            print("done,downloaded num %d"%downloaded_num)
            break
