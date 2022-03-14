# -*- coding: utf-8 -*-
import os
import json
from tqdm import tqdm
txt_path = './label/'
save_txt = './label.txt'
txt_list = os.listdir(txt_path)
with open(save_txt,'w',encoding='utf-8') as lab:
    for txt in tqdm(txt_list):
        point_list = []
        with open(txt_path+txt,'r',encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.split(',')
                p = {}
                p["transcription"] = "FUCK"
                p["points"] = [[round(float(line[0])),round(float(line[1]))],[round(float(line[2])),round(float(line[3]))],[round(float(line[4])),round(float(line[5]))],[round(float(line[6])),round(float(line[7]))]]
                point_list.append(p)
        text = json.dumps(point_list, ensure_ascii=False)
        lab.write(txt.split('.')[0] +'.jpg' + '\t' + text + '\n')
