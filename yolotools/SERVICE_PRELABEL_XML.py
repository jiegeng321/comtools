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
from pascal_voc_writer import Writer
import warnings
warnings.filterwarnings('ignore')
from multiprocessing import Pool
import ast
parser = argparse.ArgumentParser()
parser.add_argument("-server", type=str, default="{'logo':'http://192.168.6.148:1001/get_logodet_det_annotations'}",help="the server urls.")
parser.add_argument("-score_th", type=float, default=0.5, help="the score threshold,0 means donot use score threshold.")
parser.add_argument("-workers", type=int, default=10, help="the workers num.")
parser.add_argument("-source_dir", type=str, required=True, help="the source img dir.")
parser.add_argument("-draw_pic", type=str, default=False, help="draw box in image")

args = parser.parse_args()
url_dict = ast.literal_eval(args.server)
WORKERS = args.workers
score_th = args.score_th
draw_pic = args.draw_pic
image_dir = args.source_dir
# ai_brand_logo_url_t4 = "http://192.168.6.148:1001/get_logodet_det_annotations"
# url_dict = {"logo":ai_brand_logo_url_t4}
image_list = [p for p in Path(image_dir).rglob('*.*')]
print("prelabel img num:",len(image_list))
total_num = len(image_list)
def is_img(img_name):
    return True if str(img_name).split(".")[-1].lower() in ["jpg","png","jpeg","gif"] \
                   and str(img_name)[0] != "." else False

def det_server_func(image_list):

    for index, image_path in tqdm(enumerate(image_list)):
        if not is_img(image_path.name):
            continue

        try:
            img = cv2.imread(str(image_path))
            h, w, _ = img.shape
            writer = Writer(image_path.name.replace("&", ''), w, h)
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
                    file_temp = [('img', (image_path.name, open(str(image_path), 'rb'), 'image/jpeg'))]
                    response = resq1("POST", url, data=payload, files=file_temp)
                    result = json.loads(response.text)
                except Exception as e:
                    print(e)
                    print(image_path.name)
                    continue

                if 'model_res' in result:
                    pred = result['model_res']

                    if pred!=[]:
                        for logo_instance in pred:
                            logo = logo_instance['type']#.split("-")[0]
                            score = logo_instance['score']
                            if score_th:
                                if score < score_th:
                                    continue

                            box = logo_instance['bbox']
                            x1,y1,x2,y2 = box['x_min'],box['y_min'],box['x_max'],box['y_max']
                            writer.addObject(logo, x1,y1,x2,y2)

                            if draw_pic:
                                try:
                                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                                    cv2.putText(img, logo, (x1, y1-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                                    cv2.putText(img, str(round(score, 3)), (x1, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1,
                                                cv2.LINE_AA)
                                except Exception as e:
                                    print(e)
                                    continue
                else:
                    print("error", result, image_path.name)
                    continue
            xml_path = image_path.with_suffix('.xml')
            writer.save(xml_path)
            if draw_pic:
                cv2.imwrite(str(image_path), img)
        except Exception as e:
            print(e)
            print(image_path)
            continue
        if index%100==0:
            print(str(os.getpid()),"have processed:",index,"/",len(image_list))

pool = Pool(processes=WORKERS)
for i in range(0, WORKERS):
    imgs = image_list[i:len(image_list):WORKERS]
    pool.apply_async(det_server_func, (imgs,))
pool.close()
pool.join()


