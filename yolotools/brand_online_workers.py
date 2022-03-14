#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import argparse
from pathlib import Path
import requests
import json
import cv2
import os
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool

parser = argparse.ArgumentParser(description='test for logo service')
parser.add_argument("--csv", type=str, default='.')
parser.add_argument('--output', type=str, default='result0.3.csv')
parser.add_argument('--conf_thresh', type=float, default=0.1)
args = parser.parse_args()

# url
ai_brand_logo_url = "http://10.58.10.51:28088/v2/logo_brand_rec"
ai_brand_logo_tm_url = "http://10.58.14.38:55902/v2/logo_brand_rec"
brand_pattern_url = "http://10.58.14.38:55903/v2/brand_pattern_rec"

brand_filter = {}

# brand_filter = {"nike": 0.7, "Adidas": 0.6, "Abercrombie Fitch": 0.75, "Apple": 0.6,
#                 "armani": 0.7, "Asics": 0.75, "burberry": 0.75, "captain america": 0.6,
#                 "chanel": 0.75, "ck": 0.75, "dior": 0.75, "fendi": 0.8, "Ferrari": 0.75,
#                 "FILA": 0.55, "Givenchy": 0.75, "Chicago Bulls": 0.75, "Disney": 0.75,
#                 "golden goose": 0.75, "Golden State Warriors": 0.65, "gucci": 0.75,
#                 "Hermes": 0.75, "Kenzo": 0.7, "kobe": 0.7, "lacoste": 0.7, "Los Angeles lakers": 0.7,
#                 "lv": 0.6, "marc Jacobs": 0.6, "Marlboro": 0.75, "Michael Kors": 0.75,
#                 "NEW BALANCE": 0.7, "new orleans saints": 0.75, "nike": 0.7, "off-white": 0.7,
#                 "palace": 0.65, "puma": 0.75, "ralph lauren": 0.75, "SK-II": 0.75, "Stussy": 0.75,
#                 "supreme": 0.6, "Under Armour": 0.7, "Vans": 0.6, "ysl": 0.75, "the north face": 0.6,
#                 "NBA": 0.7, "alexander mcqueen": 0.75, "alexander wang": 0.6,
#
#                 "BMW": 0.75, "Cocacola": 0.75, "converse": 0.75, "fjallraven": 0.75, "hello kitty": 0.6,
#                 "jeep": 0.75, "longchamp": 0.75, "mac": 0.75, "mcm": 0.75, "miu miu": 0.75, "mlb": 0.75,
#                 "palyboy": 0.75, "Valentino Garavani": 0.75, "zara": 0.75,
#
#                 "adidas": 0.85
#                 }


def read_csv(csv_path):
    if csv_path.endswith('.xlsx'):
        csv = pd.read_excel(csv_path, keep_default_na=False)
    elif csv_path.endswith('.csv'):
        csv = pd.read_csv(csv_path, keep_default_na=False)
    else:
        print("the format is Error!")
        exit()
    return csv


def byte2cv(content):
    image = cv2.imdecode(np.asarray(bytearray(content), dtype='uint8'), cv2.IMREAD_COLOR)
    return image


def get_native_img(url_image, native_dir="./"):
    file_name = url_image.split("/")[-1]
    img_path = os.path.join(native_dir, file_name)
    imgdata = open(img_path, 'rb')
    return imgdata, file_name


def get_img(url_image):
    s = requests.session()
    file_name = url_image.split("/")[-1]
    s.keep_alive = False  # ??????
    imgdata = None
    try:
        resq = s.get(url_image)
        if len(resq.content) > 100:
            imgdata = resq.content
        return imgdata, file_name
    except requests.exceptions.ProxyError:
        return None, file_name


def url_res(imgdata, file_name, url):
    payload = {'imageId': '00003'}
    requests.adapters.DEFAULT_RETRIES = 5
    file_temp = [('img', (file_name, imgdata, 'image/jpeg'))]
    try:
        response = requests.post(url, data=payload, files=file_temp)
        result = response.json()
        return result["res"]
    except:
        return []


def conf_filter(res, conf=0.5, brand_filter={}):
    img_res = []
    for item in res:
        class_name = item["logo_name"]
        score = item["score"]
        if class_name in brand_filter:
            if score > brand_filter[class_name]:
                img_res.append(class_name)
        else:
            if score > conf:
                img_res.append(class_name)
    return img_res


def image_merge_res(imgdata, file_name):
    # brand model
    if "logo" in models:
        ai_brand_logo_res = url_res(imgdata, file_name, ai_brand_logo_url)
    else:
        ai_brand_logo_res = []
    if "logo-tm" in models:
        ai_brand_logo_tm_res = url_res(imgdata, file_name, ai_brand_logo_tm_url)
    else:
        ai_brand_logo_tm_res = []

    # parttern model
    if "pattern" in models:
        brand_pattern_res = url_res(imgdata, file_name, brand_pattern_url)
    else:
        brand_pattern_res = []
    img_res = ai_brand_logo_res + ai_brand_logo_tm_res + brand_pattern_res
    res = conf_filter(img_res, brand_filter=brand_filter)
    return res


def product_merge_res(img_list_res):
    #print(img_list_res)
    return list(set(img_list_res))


def detect_for_one_img(image_url):
    img_data, file_name = get_native_img(image_url, "/data01/erwei.wang/fordeal0913-0/images_all")
    # img_data, file_name = get_img(image_url)
    res = image_merge_res(img_data, file_name)
    print(res)


def main(csv_path):
    csv = read_csv(csv_path)
    csv_file_new = "./output.xlsx"
    colums = csv.columns.tolist()
    data_csv = []
    for index, item in enumerate(csv.itertuples()):
        temp_res = []
        for data in item:
            if not isinstance(data, str) or not data.startswith("https://"):
                continue
            # img_data, file_name = get_native_img(data, "/data01/erwei.wang/fordeal0913-0/images_all")
            img_data, file_name = get_img(data)
            if img_data is None:
                res = []
            else:
                res = image_merge_res(img_data, file_name)
            temp_res += res
        item_res = product_merge_res(temp_res)
        print(f"{index}:{item_res}")
        data_csv.append(item_res)
    insert_id = colums.index("_col1")
    colums.insert(insert_id, "jishenlabel")
    csv["jishenlabel"] = data_csv
    df = csv.reindex(columns=colums)
    df.to_excel(csv_file_new)


def product_list_res(item,index):
    temp_res = []
    img_index = 0
    human_result = item[3]
    for data in item:
        if not isinstance(data, str) or not data.startswith("https://"):
            continue
        img_index += 1
        img_data, file_name = get_img(data)
        res = image_merge_res(img_data, file_name)
        if human_result==0 and res != []:
            for re in res:
                save_path = os.path.join(save_diff_dir,re)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                with open(save_path+"/"+file_name, "wb") as f:
                    f.write(img_data)
                print(f"diff img is saved: {os.path.join(save_path,file_name)}")
        res_ = []
        if res != []:
            for r in res:
                re = str(img_index) + ":" + r
                res_.append(re)
        temp_res += res_
    item_res = product_merge_res(temp_res)
    print(f"{index}:{human_result}")
    print(f"{index }:{item_res}")
    return item_res


def main(csv_path,csv_file):
    csv = read_csv(csv_path)[100:2000]

    csv_file_new = csv_file
    colums = csv.columns.tolist()
    data_csv = []
    num_process = 3
    pool = Pool(num_process)
    for index, item in enumerate(csv.itertuples()):
        list_item = [i for i in item]
        data_csv.append(pool.apply_async(product_list_res, args=(list_item,index)))
    pool.close()
    pool.join()
    print(len(data_csv))
    data_csv = [i.get() for i in data_csv]
    insert_id = colums.index("_col1")
    colums.insert(insert_id, "jishenlabel")
    csv["jishenlabel"] = data_csv
    df = csv.reindex(columns=colums)
    df.to_excel(csv_file_new)



if __name__ == "__main__":
    # per image
    # img_url = "https://s3.forcloudcdn.com/item/images/dmc/d3811a5f-e47b-42f7-9a98-048f7fb017f1-960x960.jpeg"
    # detect_for_one_img(img_url)

    #models = ["logo","logo-tm","pattern"]
    models = ["pattern"]
    save_diff_dir = None#"/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_0923_0_addwhite_diff"
    csv_file = "./output_gucci_addwhite.xlsx"
    csv_path = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/漏审gucci.xlsx"
    main(csv_path,csv_file)
