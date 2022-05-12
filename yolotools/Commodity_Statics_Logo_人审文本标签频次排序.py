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

def readtxt(txt_file):
    print("reading txt file")
    try:
        with open(txt_file, 'r') as fr:
            lines = fr.readlines()
        print("reading done")
        return lines
    except Exception as e:
        print(e)
        return None

def analyze_data(lines):
    text_brand = []
    print("analyzing...")
    for line in tqdm(lines):
        try:
            dict_brand = ast.literal_eval(line)
        except:
            print("bad line:",line)
            continue
        if "finalCheckResult" in dict_brand and "finalTagHit" in dict_brand:
            if "[文本]侵权/品牌" in dict_brand["finalTagHit"]:
                for per_brand in dict_brand["finalTagHit"].split(","):
                    if "[文本]侵权/品牌" in per_brand:
                        brand = per_brand.split("/")[-1]  # nike
                        text_brand.append(brand)
    print("done")
    return text_brand

if __name__=="__main__":
    from collections import Counter
    txt_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0415.txt"
    lines = readtxt(txt_dir)
    text_brand = analyze_data(lines)
    count_text_brand = Counter(text_brand)
    print(count_text_brand)
