#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""
import argparse
from pathlib import Path
import requests
import json
import cv2
import os
import random
from tqdm import tqdm
import numpy as np
from evaluator.test_eval import YOLOTest

parser = argparse.ArgumentParser(description='test for logo service')

parser.add_argument("--image_dir", type=str, default='.')
parser.add_argument('--output', type=str, default='result0.3.csv')
parser.add_argument('--base_url', type=str, default='http://10.58.14.38:55902')
parser.add_argument('--conf_thresh', type=float, default=0.1)

args = parser.parse_args()
bg = [".jpg", ".png", ".jpeg"]
out_dir = "./out"

BINARY_API_ENDPOINT = "{}/v2/logo_brand_rec".format(args.base_url)

image_list = [p for p in Path(args.image_dir).rglob('*.*') if p.suffix.lower() in bg]

found_num = 0
total_num = len(image_list)


det_boxes = {}
nums = 0
for image_path in tqdm(image_list):
    if image_path.name == ".DS_Store":
        continue
    image_path = str(image_path)
    img = cv2.imread(image_path)
    file_name = image_path.split('/')[-1]
    payload = {'imageId': '00003'}
    file_temp = [('img', (file_name, open(image_path, 'rb'), 'image/jpeg'))]
    resq1 = requests.request
    resq2 = requests.request
    response = resq1("POST", BINARY_API_ENDPOINT, data=payload, files=file_temp)

    result = json.loads(response.text)

    ds = np.empty([0, 6])
    if 'res' in result:
        pred = result['res']
        if len(pred)!=0:
            nums+=1
        for logo_instance in pred:
            box = logo_instance['box']
            logo_name = logo_instance['logo_name']
            x1 = box['x1']
            y1 = box['y1']
            x2 = box['x2']
            y2 = box['y2']
            color1 = 0
            color2 = 0
            color3 = 255
            ds = np.vstack([ds, np.array([x1, y1, x2, y2, logo_instance['score'], 0])])
            # cv2.rectangle(img, (x1, y1), (x2, y2), [color1, color2, color3], 2)
            # cv2.putText(img, logo_name, (x1 - 6, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 0, 0], 1, cv2.LINE_AA)

    det_boxes[file_name] = ds

yolo_test = YOLOTest(["LOGO"], det_boxes, "/data01/erwei.wang/dataset/data/test_twins")
yolo_test.evaluate_detections()
print("pic rito：", round(nums/total_num, 4))

    # cv2.imwrite(os.path.join(out_dir, file_name), img)

    # conf0.1
    # enter_try = BINARY_API_ENDPOINT.replace("38088", "38089")
    # # print(file_temp)
    # payload_2 = {'imageId': '00004'}

    # file_temp2 = [('img', (file_name, open(image_path, 'rb'), 'image/jpeg'))]
    # response_2 = resq2("POST", enter_try , data=payload_2, files=file_temp2)
    # results2 = json.loads(response_2.text)
    # if 'res' in results2:
    #     pred2 = results2['res']
    #     print("in res2")
    #     for logo_instance in pred2:
    #         box = logo_instance['box']
    #         x1 = box['x1']
    #         y1 = box['y1']
    #         x2 = box['x2']
    #         y2 = box['y2']
    #         color1 = 0
    #         color2 = 0
    #         color3 = 255
    #         cv2.rectangle(img, (x1, y1), (x2, y2), [color1, color2, color3], 1)
    # print(file_name)
    # cv2.imwrite(os.path.join(out_dir, file_name), img)


