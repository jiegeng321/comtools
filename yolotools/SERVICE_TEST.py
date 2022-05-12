#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
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
#from model.config import logo_id_to_name
#from multiprocessing import Pool, Manager
warnings.filterwarnings('ignore')
#import time
from multiprocessing import Pool, Manager
WORKERS = 30
save_empty = True
score_th = None#0.5
#logo white test
# image_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/white_test_labeled/"
# out_pred_img_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/white_test_0401"
# save_label_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/white_test_0401.json"
#pattern white test
# image_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/white_test_labeled/"
# out_pred_img_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/white_test_0401"
# save_label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/white_test_0401.json"
#logo test
# image_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/brand_labeled/"
# out_pred_img_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/online_0420"
# save_label_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/online_0420.json"
#pattern test
image_dir = "/data02/xu.fx/dataset/PATTERN_DATASET/comb_data/clsdataset_pattern_v3/val/lv_h/"
out_pred_img_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/tmp3"
save_label_json = None#"/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/tmp2.json"

ai_brand_logo_url = "http://10.57.31.15:5032/v2/logo_brand_rec"
#ai_brand_logo_tm_url = "http://10.58.14.38:55902/v2/logo_brand_rec"
ai_brand_logo_tm_url = "http://10.57.31.15:1000/v2/logo_brand_rec"
#ai_brand_logo_tm_url_t4 = "http://192.168.6.150:1001/v2/logo_brand_rec"
ai_brand_logo_tm_url_t4 = "http://192.168.6.148:1002/v2/logo_brand_rec"
ai_brand_logo_tm_url_p40 = "http://10.57.31.15:1003/v2/logo_brand_rec"
ai_brand_pattern_url_p40 = "http://10.57.31.15:1003/v2/pattern_brand_rec"
brand_pattern_url = "http://10.57.31.15:1004/v2/logo_brand_rec"
#url_dict = {"pattern":brand_pattern_url}
url_dict = {"logo-tm":ai_brand_pattern_url_p40}
if out_pred_img_dir:
    if not os.path.exists(out_pred_img_dir):
        os.makedirs(out_pred_img_dir)

#BINARY_API_ENDPOINT = "{}/v2/logo_brand_rec".format(base_url)
image_list = [p for p in Path(image_dir).rglob('*.*')]
print("test img num:",len(image_list))
print("result save to:",save_label_json)
with open('/data01/xu.fx/comtools/human_label_to_model_label/l2l_dict.json', 'r') as f:
    l2l_data = json.load(f)

find_num = 0
different_num = 0
total_num = len(image_list)
#random.shuffle(image_list)

def det_server_func(image_list,save_json_dict):
    for index, image_path in tqdm(enumerate(image_list)):
        if not is_img(image_path.name) or image_path.name[0]==".":
            continue
        try:
            image_path = str(image_path)
            img = cv2.imread(image_path)
            h, w, _ = img.shape
            file_name = image_path.split('/')[-1]
            logo_list_human = []
            logo_list = []
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
                    if pred==[]:
                        brand_name = "empty"
                        logo_list_human.append({brand_name:1.0})
                        logo_list.append(brand_name)
                    else:
                        for logo_instance in pred:
                            logo = logo_instance['logo_name']#.split("-")[0]
                            score = logo_instance['score']
                            if score_th:
                                if score < score_th:
                                    continue
                            logo_list.append(logo)

                            if logo not in l2l_data:
                                logo = logo.lower().replace(" ", "_")
                            else:
                                logo = l2l_data[logo].split("/")[-1]
                            # if logo == "new_york_yankees":
                            #     logo = "mlb"
                            #print(logo)
                            #logo = logo.replace("'","")
                            logo_list_human.append({logo:score})
                            box = logo_instance['box']
                            score = logo_instance['score']
                            x1,y1,x2,y2 = box['x1'],box['y1'],box['x2'],box['y2']
                            # try:
                            #     cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                            #     cv2.putText(img, logo, (x1, y1-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                            #     cv2.putText(img, str(round(score, 3)), (x1, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1,
                            #                 cv2.LINE_AA)
                            # except Exception as e:
                            #     print(e)
                            #     continue
                else:
                    print("error", result, file_name)
                    continue
            if logo_list==[]:
                logo_list.append("empty")

            if logo_list_human == []:
                logo_list_human.append({"empty":1.0})
            # result_ = {}
            # result_["logo"] = list(set(logo_list_human))
            # result_["logo"] =
            save_json_dict[file_name] = logo_list_human
            logo_list.sort()
            brand_max_prd = max(logo_list, key=logo_list.count)
            brand_name = brand_max_prd#.split("-")[0]
            if out_pred_img_dir:
                if brand_name=="empty" and not save_empty:
                    continue
                save_dir = os.path.join(out_pred_img_dir,brand_name)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                try:
                    cv2.imwrite(os.path.join(save_dir, file_name), img)
                except:
                    print("problem file: ",os.path.join(save_dir, file_name))
        except Exception as e:
            print(e)
            print(image_path)
            continue
        if index%100==0:
            print(str(os.getpid()),"have processed:",index,"/",len(image_list))
        #     with open(save_label_json, 'w') as f:
        #         json.dump(dict(save_json_dict), f)
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
if save_label_json:
    with open(save_label_json, 'w') as f:
        json.dump(dict(save_json_dict), f)
    #print(save_json_dict)
    print("write len：",len(save_json_dict))
    with open(save_label_json, 'r') as f:
        model_result = json.load(f)
    print("read len:",len(model_result))
    print(save_json_dict.popitem())
