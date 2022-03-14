# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:27:06 2020

@author: Administrator
"""

import numpy as np
import os
import json
import io
from PIL import Image , ImageDraw , ImageFont
from tqdm import tqdm
import cv2
#设置图片和txt标注路径，转成的json格式存在图片路径下的outputs，可直接用标注精灵打开
img_path = 'traffic_light_test_img'
result_json_file = 'traffic_light_result.json'
draw_save_path = 'yolo_draw_img'
txt_save_path = 'yolo_txt_result'
json_save_path = 'yolo_split_json_result'
SAVE_JSON = False
SAVE_DRAW = False
SAVE_TXT = True
CONFIDENCE = 0.3


list_im = os.listdir(img_path)
if SAVE_JSON:
    if not os.path.exists('./'+json_save_path):
        os.makedirs('./'+json_save_path)
if SAVE_DRAW:
    if not os.path.exists('./'+draw_save_path):
        os.makedirs('./'+draw_save_path)
if SAVE_TXT:
    if not os.path.exists('./' + txt_save_path):
        os.makedirs('./' + txt_save_path)

yolo_result = json.load(open(result_json_file))
data = json.load(open('./template.json'))
for result in tqdm(yolo_result):
    save_name = result['filename'].split('/')[-1]
    image = Image.open(os.path.join(img_path, save_name))
    img_width,img_height = image.size
    boxs = result['objects']
    obj = []
    data['path'] = "C:\\Users\\Administrator\\Desktop\\txt_to_json_traffic_light\\%s\\"%img_path+save_name
    if SAVE_TXT:
        file_handle = open(txt_save_path + '/' + save_name.replace('.jpg', '.txt'), mode='w')
    for box in boxs:
        confidence = box['confidence']
        box = box['relative_coordinates']

        center_x = box['center_x']*img_width
        center_y = box['center_y'] * img_height
        width = box['width'] * img_width
        height = box['height'] * img_height

        xmin = center_x - width / 2
        xmax = center_x + width / 2
        ymin = center_y - height / 2
        ymax = center_y + height / 2
        if SAVE_JSON:
            if confidence>CONFIDENCE:
                obj.append({"name": "traffic_light",
                            "bndbox": {"xmin": int(xmin), "ymin": int(ymin), "xmax": int(xmax),
                                       "ymax": int(ymax)}})
        if SAVE_TXT:
            if confidence > CONFIDENCE:

                    file_handle.write("traffic_light")
                    file_handle.write(",")
                    file_handle.write(str(round(confidence,2)))
                    file_handle.write(",")
                    file_handle.write(str(int(xmin)))
                    file_handle.write(",")
                    file_handle.write(str(int(ymin)))
                    file_handle.write(",")
                    file_handle.write(str(int(xmax)))
                    file_handle.write(",")
                    file_handle.write(str(int(ymax)))
                    file_handle.write("\n")
        if SAVE_DRAW:
            draw = ImageDraw.Draw(image)
            if confidence > CONFIDENCE:
                draw.text((int(xmin),int(ymin)-19), "%s"%str(round(confidence,2)), fill='yellow',font=ImageFont.truetype('./WeiRuanYaHei-1.ttf',size=15))
                draw.rectangle((int(xmin),int(ymin),int(xmax),int(ymax)), fill=None, outline='red', width=2)
    file_handle.close()
    data['outputs']['object'] = obj
    if SAVE_DRAW:
        image.save(os.path.join(draw_save_path,save_name), quality=100)
    if SAVE_JSON:
        with open('./'+json_save_path+'/'+save_name.replace('.jpg','.json'),'w',encoding='utf-8') as f:
          json.dump(data,f,ensure_ascii=False)
































































