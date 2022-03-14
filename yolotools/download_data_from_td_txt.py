#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""

import json
import os
import time

import cv2
import random
import requests
import argparse
import numpy as np
from pathlib import Path
#from func.check import check_dir
#from func.path import os.path.join
from pascal_voc_writer import Writer
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

#os.environ.setdefault("ftp_proxy","http://10.57.240.219:7890")
#os.environ.setdefault("http_proxy","http://10.57.240.219:7890")
#os.environ.setdefault("https_proxy","http://10.57.240.219:7890")
parser = argparse.ArgumentParser(description="accept annotion txt from jinglang, to make yolodata")
parser.add_argument('--show', action='store_true', help="show picture")
args = parser.parse_args()


def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 255), textSize=16):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def makedataset():
    lines = []
    with open(src_json, 'r', encoding= 'utf-8') as fjson:
        data = fjson.readlines()
        for data_i in data:
            if data_i.strip().find('version":"4.3.0"}{"backgroundImage"') == -1:
                lines.append(data_i.strip())
            else:
                temp = data_i.strip().split('version":"4.3.0"}{"backgroundImage"')
                lines.append(temp[0] + 'version":"4.3.0"}')
                lines.append('{"backgroundImage"'+ temp[1])

        random.shuffle(lines)
        #val_num = int(len(lines)*0.2)
        print('total_num: ',len(lines))
        #print('val_num: ',val_num)
        for index, line in tqdm(enumerate(lines)):
            try:
                json_str = json.loads(line.strip())
            except:
                print(line.strip())
                exit()
            img_name = json_str['backgroundImage']['originFileName']
            img_name = fix_name + img_name.replace('-', '').replace('_', '').replace(',', '').replace(' ', '').replace('&', '').replace('~', '').replace("'", "").replace("’", "")
            img_name = img_name
            fix_str = os.path.splitext(img_name)[1]
            if fix_str == ".gif":
                continue
            xml_name = img_name[:-1*len(fix_str)] + ".xml"
            w = json_str['backgroundImage']['width']
            h = json_str['backgroundImage']['height']
            writer = Writer(img_name, w, h)
            url = json_str['backgroundImage']['src']
            img_id = url[40:40+32]
            #img_id = url.split("fileId=")[-1].split("&type")[0]
            #print(img_id)
            url = "https://lbstg.tongdun.me/api/file/downloadFromCeph?fileId="+img_id
            #url = "https://lbstg.tongdun.me/api/file/download?fileId=" + img_id
            #url = url.replace("dubhe.tongdun.cn","lbstg.tongdun.me").replace("load","download")
            print(url)
            #start = time.time()
            #try:
            resq = requests.get(url)
            #except:
                #print("net error")
            #print(time.time()-start)
            if len(resq.content) > 100:
                img_out = os.path.join(dst_dir , img_name)
                open(img_out, 'wb').write(resq.content)
            else:
                continue
            objects = json_str["objects"]
            bg_scaleX = json_str['backgroundImage']['scaleX']
            bg_scaleY = json_str['backgroundImage']['scaleY']
            if args.show:
                cv2_img = cv2.imread(img_out)
            for object in objects:
                type = object['type']
                ob_scaleX = object['scaleX']
                ob_scaleY = object['scaleY']
                if type == "rect":
                    try:
                        name = object["label"]['name'].replace('&', '')
                    except:
                        print(json_str)
                        continue
                    left = round(object['left'] / bg_scaleX, 3)
                    top = round(object['top'] / bg_scaleY, 3)
                    width = (object['width'] * ob_scaleX) / bg_scaleX
                    height = (object['height'] * ob_scaleY) / bg_scaleY
                    new_left = min(left, left + width)
                    new_top = min(top, top + height)
                    new_right = max(left, left + width)
                    new_down = max(top, top + height)
                    writer.addObject(name, new_left, new_top, new_right, new_down)
                elif type == "polygon":
                    pass
                else:
                    pass
                if args.show:
                    cv2.rectangle(cv2_img, (int(left), int(top)), (int(left+width), int(top+height)), [255, 0, 0], 1)
                    #cv2.putText(cv2_img, name, (int(left) - 6, int(top)), cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255], 1, cv2.LINE_AA)
                    cv2_img = cv2ImgAddText(cv2_img, name, int(left), int(top) - 16)
            writer.save(os.path.join(dst_dir, xml_name))
            if args.show:
                # cv2.imwrite('./example.jpg', cv2_img)
                print(img_name)
                cv2_img = cv2.resize(cv2_img, (960, 960))
                cv2.imshow("img", cv2_img)
                cv2.waitKey(-1)


if __name__=="__main__":
    args.show = False

    src_json = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal标注20类1105/project_comme_des_garcons-fordeal标注-20211102.txt"
    fix_name = "commedesgarconsgf_"
    dst_dir = Path("/data01/xu.fx/dataset/LOGO_DATASET/D12/checked")

    print(src_json)
    makedataset()
