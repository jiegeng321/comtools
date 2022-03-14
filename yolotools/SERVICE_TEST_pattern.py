#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import argparse
from pathlib import Path
import requests
import json
import cv2
import os
from tqdm import tqdm
import warnings
import shutil
from comfunc.tools import is_img,check_dir
warnings.filterwarnings('ignore')
from multiprocessing import Pool, Manager
WORKERS = 30
save_empty = True
score_th = None#0.5

image_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/burberry"
out_pred_img_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/burberry_pred"
save_label_json = None#"/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online_02103.json"

brand_pattern_url = "http://10.58.14.38:55903/v2/pattern_brand_rec"
url_dict = {"pattern":brand_pattern_url}
if out_pred_img_dir:
    check_dir(out_pred_img_dir,delete=True)

image_list = [p for p in Path(image_dir).rglob('*.*')]
print("test img num:",len(image_list))
print("result save to:",save_label_json)

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
                        logo_list_human.append(brand_name)
                        logo_list.append(brand_name)
                    else:
                        for logo_instance in pred:
                            logo = logo_instance['logo_name'].split("-")[0]
                            score = logo_instance['score']
                            if score_th:
                                if score < score_th:
                                    continue
                            logo_list.append(logo)
                            logo_list_human.append(logo)
                            box = logo_instance['box']
                            score = logo_instance['score']
                            x1,y1,x2,y2 = box['x1'],box['y1'],box['x2'],box['y2']
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
            if logo_list==[]:
                logo_list.append("empty")

            if logo_list_human == []:
                logo_list_human.append("empty")
            # result_ = {}
            # result_["logo"] = list(set(logo_list_human))
            # result_["logo"] =
            save_json_dict[file_name] = list(set(logo_list_human))
            logo_list.sort()
            brand_max_prd = max(logo_list, key=logo_list.count)
            brand_name = brand_max_prd.split("-")[0]
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
        # if index%1000==0:
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
