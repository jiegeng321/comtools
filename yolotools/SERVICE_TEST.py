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
import random
import shutil as sh
# import numpy as np
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
# import matplotlib.pyplot as plt
# import random
import warnings
import shutil
import numpy as np
import torch
import clip
from PIL import Image
from comfunc.tools import is_img
#from my_clip.my_clip import clip_func
#from model.config import logo_id_to_name
#from multiprocessing import Pool, Manager
warnings.filterwarnings('ignore')
#import time
from multiprocessing import Pool, Manager

WORKERS = 10
save_empty = True
score_th = 0.5
#logo white test
# image_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/white_test_labeled/"
# out_pred_img_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/white_test_0401"
# save_label_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/white_test_0401.json"
#pattern white test
# image_dir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/white_test_labeled/"
# out_pred_img_dir = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/white_test_0401"
# save_label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/white_test_0401.json"
#logo test
image_dir = "/data02/xu.fx/dataset/LOGO_DATASET/comb_data/yolodataset_logo_784bs_1394ks_0715/JPEGImages/train/images"
out_pred_img_dir = None#"/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/online_l_0718_t4_newplugin"
save_label_json = "/data01/xu.fx/comtools/forgeting_test/epoch185_3.json"
back_save_label_json = save_label_json.replace(".json","_back.json")
#pattern test
# image_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_white_data_for_pattern_0621/empty"
# out_pred_img_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_white_data_for_pattern_0621/empty_pre"
# save_label_json = None#"/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online_v1.2_0623.json"

ai_cartoon_url = "http://192.168.6.148:5032/v2/cartoon_rec"
ai_brand_logo_url = "http://10.57.31.15:5032/v2/logo_brand_rec"
#ai_brand_logo_tm_url = "http://10.58.14.38:55902/v2/logo_brand_rec"
ai_brand_logo_tm_url = "http://10.57.31.15:1000/v2/logo_brand_rec"
#ai_brand_logo_tm_url_t4 = "http://192.168.6.150:1001/v2/logo_brand_rec"
ai_brand_logo_tm_url_t4 = "http://192.168.6.148:1001/v2/logo_brand_rec"
ai_brand_logo_tm_url_p40 = "http://10.57.31.15:1001/v2/logo_brand_rec"
ai_brand_logo_online_url = "https://ai-brand-logostg.tongdun.cn/v2/logo_brand_rec"
ai_brand_pattern_url_p40 = "http://10.57.31.15:1002/v2/pattern_brand_rec"
brand_pattern_url = "http://10.57.31.15:1004/v2/logo_brand_rec"
#url_dict = {"pattern":brand_pattern_url}
url_dict = {"logo":ai_brand_logo_tm_url_t4}
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

def det_server_func(image_list,save_json_dict,pids):
    if str(os.getpid()) not in pids:
        pids.append(str(os.getpid()))
    for index, image_path in tqdm(enumerate(image_list[9700+9000:])):
        if not is_img(image_path.name) or image_path.name[0]==".":
            continue
        try:
            image_path = str(image_path)
            img = cv2.imread(image_path)
            h, w, _ = img.shape
            file_name = image_path.split('/')[-1]
            logo_list_human = []
            for model_name, url in url_dict.items():
                if model_name == "logo":
                    color = [255,0,0]
                elif model_name == "logo-tm":
                    color = [0,255,0]
                else:
                    color = [0,0,255]
                try:
                    resq1 = requests.request
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
                        logo_list_human.append({"logo":"empty","score":0.0,"box":[]})
                    else:
                        for logo_instance in pred:
                            logo = logo_instance['logo_name']#.split("-")[0]
                            score = logo_instance['score']
                            if score_th:
                                if score < score_th:
                                    continue
                            if "border" in logo:
                                logo = logo.replace("_border", "")
                            if "small" in logo:
                                logo = logo.replace("_small", "")
                            if logo not in l2l_data:
                                logo = logo.lower().replace(" ", "_").replace(".", "")
                            else:
                                logo = l2l_data[logo].split("/")[-1]
                            box = logo_instance['box']
                            x1,y1,x2,y2 = box['x1'],box['y1'],box['x2'],box['y2']
                            logo_list_human.append({"logo":logo,"score":score,"box":[x1,y1,x2,y2]})
                            try:
                                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                                cv2.putText(img, logo, (x1, y1-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                                cv2.putText(img, str(round(score, 3)), (x1, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1,
                                            cv2.LINE_AA)
                            except Exception as e:
                                print(e)
                                continue
                else:
                    print("error", result, file_name)
                    continue
            if logo_list_human == []:
                logo_list_human.append({"logo":"empty","score":0.0,"box":[]})
            logo_list_human = sorted(logo_list_human, key=lambda x: x.get("score"),reverse=True)
            save_json_dict[file_name] = logo_list_human
            brand_name = logo_list_human[0]["logo"]
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
        save_pid = pids[-1]
        if (index+1)%500==0 and save_label_json and str(os.getpid())==save_pid:
            if len(pids)<WORKERS:
                pids.append(pids[-1])
                pids[-1] = random.choice(pids[:-1])
            else:
                pids[-1] = random.choice(pids[:-1])

            with open(save_label_json, 'w') as f:
                json.dump(dict(save_json_dict), f)

            if save_label_json != None or len(save_json_dict)>10:
                sh.copy(save_label_json, back_save_label_json)
            print(save_pid,"saved num:",len(save_json_dict))
save_json_dict = Manager().dict()
pids = Manager().list()
pool = Pool(processes=WORKERS)
for i in range(0, WORKERS):
    imgs = image_list[i:len(image_list):WORKERS]
    pool.apply_async(det_server_func, (imgs,save_json_dict,pids,))
pool.close()
pool.join()

if save_label_json:
    with open(save_label_json, 'w') as f:
        json.dump(dict(save_json_dict), f)
    print("write len：",len(save_json_dict))
    with open(save_label_json, 'r') as f:
        model_result = json.load(f)
    print("read len:",len(model_result))
    print("sample:",save_json_dict.popitem())
    print("result save to",save_label_json)
    sh.rmtree(back_save_label_json)
