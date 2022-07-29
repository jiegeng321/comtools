#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import ast
import os
import requests
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import classification_report
import argparse
import pickle
txt_dir = ["/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/7月1日_7月8日.txt",
            ]
save_name = "./logo_brand_info/fordeal_logo_info_0701_0708.pkl"

def readtxt(txt_file):
    print("reading txt file")
    if type(txt_file) is list:
        lines = []
        try:
            for txt in txt_file:
                with open(txt, 'r') as fr:
                    lines += fr.readlines()
            print("reading done")
            return lines
        except Exception as e:
            print(e)
            return None
    else:
        try:
            with open(txt_file, 'r') as fr:
                lines = fr.readlines()
            print("reading done")
            return lines
        except Exception as e:
            print(e)
            return None
lines = readtxt(txt_dir)
BRAND = []
brand_data = {}
for line in tqdm(lines):
    try:
        dict_brand = ast.literal_eval(line)
    except:
        print("bad line:", line)
        continue
    if "finalCheckResult" in dict_brand and dict_brand["finalCheckResult"] == "Reject":
        #print(dict_brand["finalTagHit"])
        for i in dict_brand["finalTagHit"].split(","):
            if "[图像]侵权/品牌" in i:
                brand = i.split("/")[-1]
                if brand in brand_data:
                    brand_data[brand] += 1
                else:
                    brand_data[brand] = 1
    else:
        print("no human result")
print(brand_data)
for k,v in brand_data.items():
    BRAND.append({"name":k,"value":v})
print(BRAND)
print(len(BRAND))

pickle.dump(BRAND, open(save_name, "wb"))
data = pickle.load(open(save_name, "rb"))
print(data)
print(len(data))
        # .split("/")[-1]


