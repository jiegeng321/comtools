#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import argparse
from pathlib import Path
import requests
import json
import cv2
import os
from tqdm import tqdm
# import numpy as np
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
# import matplotlib.pyplot as plt
# import random
import warnings
import shutil
from comfunc.tools import is_img
from pascal_voc_writer import Writer
#from model.config import logo_id_to_name
#from multiprocessing import Pool, Manager
warnings.filterwarnings('ignore')
#import time
from multiprocessing import Pool, Manager
WORKERS = 30
save_empty = False
score_th = None#0.5

image_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/check_wew_by_fx_raw"
xml_dir = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/checked"
dst_xml_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/check_wew_by_fx_raw"
#save_label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online3.json"

ai_brand_logo_url = "http://10.58.10.51:5031/v2/logo_brand_rec"
ai_brand_logo_tm_url = "http://10.58.14.38:55902/v2/logo_brand_rec"
brand_pattern_url = "http://10.58.14.38:55903/v2/pattern_brand_rec"
#url_dict = {"logo":ai_brand_logo_url,"logo-tm":ai_brand_logo_tm_url,"pattern":brand_pattern_url}
#url_dict = {"logo":ai_brand_logo_url}
url_dict = {"logo-tm":ai_brand_logo_tm_url}

# if out_pred_img_dir:
#     if not os.path.exists(out_pred_img_dir):
#         os.makedirs(out_pred_img_dir)

#BINARY_API_ENDPOINT = "{}/v2/logo_brand_rec".format(base_url)
image_list = [p for p in Path(image_dir).rglob('*.*')][:]
print(len(image_list))
# with open('/data01/xu.fx/comtools/human_label_to_model_label/l2l_dict.json', 'r') as f:
#     l2l_data = json.load(f)

find_num = 0
different_num = 0
total_num = len(image_list)
#random.shuffle(image_list)
def readxml(annotion_path):
    # print(annotion_path)
    res = []
    from xml.etree import ElementTree as ET
    try:
        root = ET.parse(annotion_path).getroot()
    except :
        assert "the file is not found."
    else:
        w = root.find("size").find("width").text
        h = root.find("size").find("height").text
        for index, subtree in enumerate(root.iter('object')):
            label = subtree.find("name").text
            bbox = subtree.find('bndbox')
            x1 = float(bbox.find('xmin').text)
            y1 = float(bbox.find('ymin').text)
            x2 = float(bbox.find('xmax').text)
            y2 = float(bbox.find('ymax').text)
            res.append((label, x1, y1, x2, y2))
    return res,w,h
def det_server_func(image_list,save_json_dict):
    for image_path in tqdm(image_list):
        if not is_img(image_path.name):
            continue
        # if "WewData" in image_path.name:
        #     continue
        try:
            image_path = str(image_path)
            img = cv2.imread(image_path)
            h, w, _ = img.shape
            file_name = image_path.split('/')[-1]
            # logo_list_human = []
            #logo_list = []

            for model_name, url in url_dict.items():
                if model_name == "logo":
                    color = [255,0,0]
                elif model_name == "logo-tm":
                    color = [0,255,0]
                else:
                    color = [0,0,255]
                resq1 = requests.request
                try:
                    payload = {'imageId': '00003'}
                    file_temp = [('img', (file_name, open(image_path, 'rb'), 'image/jpeg'))]
                    response = resq1("POST", url, data=payload, files=file_temp)
                    result = json.loads(response.text)
                except Exception as e:
                    print(e)
                    print(file_name)
                    continue

                if 'res' in result:
                    pred = result['res']
                    #print(pred)
                    if pred==[]:
                        brand_name = "empty"
                        # logo_list_human.append(brand_name)
                        # logo_list.append(brand_name)
                    else:
                        src_xml = os.path.join(xml_dir,file_name.replace(Path(image_path).suffix, ".xml"))
                        dst_xml = os.path.join(dst_xml_dir,file_name.replace(Path(image_path).suffix, ".xml"))
                        if not os.path.exists(src_xml):
                            continue
                        res, w, h = readxml(src_xml)
                        writer = Writer(file_name.replace("&", ''), w, h)
                        logo_exist_list = []
                        for re in res:
                            writer.addObject(re[0], re[1], re[2], re[3],re[4])
                            logo_exist_list.append(re[0].lower())
                        for logo_instance in pred:
                            logo = logo_instance['logo_name']
                            score = logo_instance['score']
                            box = logo_instance['box']
                            if score_th:
                                if score < score_th:
                                    continue
                            if logo.lower() in logo_exist_list:
                                print(logo," exits")
                            else:
                                print(logo, " added")
                                writer.addObject(logo, box["x1"], box["y1"], box["x2"], box["y2"])
                        writer.save(dst_xml)

                else:
                    print("error", result, file_name)
                    continue

        except Exception as e:
            print(e)
            print(image_path)
            continue

save_json_dict = Manager().dict()
pool = Pool(processes=WORKERS)
for i in range(0, WORKERS):
    imgs = image_list[i:len(image_list):WORKERS]
    pool.apply_async(det_server_func, (imgs,save_json_dict,))
pool.close()
pool.join()

# save_json_dict = {}
# det_server_func(image_list,save_json_dict)
# print(len(save_json_dict))
# if save_label_json:
#     with open(save_label_json, 'w') as f:
#         json.dump(dict(save_json_dict), f)
#     #print(save_json_dict)
#     print("write len：",len(save_json_dict))
#     with open(save_label_json, 'r') as f:
#         model_result = json.load(f)
#     print("read len:",len(model_result))
#     print(save_json_dict.popitem())
