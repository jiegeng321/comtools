import numpy as np
import os
import json
import io
import PIL.Image
from tqdm import tqdm
import shutil
#import Levenshtein
import pandas as pd
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

label_path = './baodan_test_gt'
predict_path = './test_result'

#list_path_real = os.listdir(label_path)
#list_path_real = sorted(list_path_real)
list_path_our = os.listdir(predict_path)
list_path_our = sorted(list_path_our)

total_num = len(list_path_our)
Name_count_our = 0
Idnum_count_our = 0
Date_count_our = 0
Date_start_count_our = 0
total_count_our = 0

def char_rate(str_in,str_true):
    len_ = len(str_true)
    count = 0
    for char in str_in:
        if char in str_true:
            count+=1
    if count>=len_:
        count=len_
    return count/len_

for i in range(0, len(list_path_our)):
    #path_real = os.path.join(label_path, list_path_real[i])
    path_our = os.path.join(predict_path, list_path_our[i])
    path_real = os.path.join(label_path, list_path_our[i])
    #path_real = path_real.replace(".jpg.txt", ".txt")

    with open(path_real,'r',encoding='utf-8') as f_r:
        lines_r = f_r.readlines()
        tmp = []
        for r in lines_r:
            r = r.strip().split(": ")[-1]
            tmp.append(r)

        lines_r = tmp

        with open(path_our,'r',encoding='utf-8') as f_p:
            lines_p = f_p.read()
            lines_p = lines_p.strip()
            lines_p = lines_p.split("\n")
            tmp = []
            for p in lines_p:
                p = p.split(": ")[-1]
                tmp.append(p)
            lines_p = tmp

    lines_p[1] = lines_p[1][-16:]
    lines_r[1] = lines_r[1][-16:]
    #print(lines_r[1][-16:])
    if lines_r==lines_p:
        total_count_our+=1

    if lines_r[0] == lines_p[0]:
        Name_count_our+=1
    else:
        print('保单号不匹配:',path_our)

    if lines_r[1][-16:] == lines_p[1][-16:]:
        Idnum_count_our+=1
    else:
        print('车架号不匹配:',path_our)

    if lines_r[2] == lines_p[2]:
        Date_count_our+=1
    else:
        print('开始日期不匹配:',path_our)

    if lines_r[3] == lines_p[3]:
        Date_start_count_our+=1
    else:
        print('结束日期不匹配:', path_our)

Name_count_our_rate = Name_count_our / total_num
Idnum_count_our_rate = Idnum_count_our / total_num
Date_count_our_rate = Date_count_our / total_num
Date_start_count_our_rate = Date_start_count_our / total_num
total_count_our_rate = total_count_our / total_num
print("total num = ", total_num)
print('保险单号字段准确率：',Name_count_our_rate)
print('车架号码字段准确率：',Idnum_count_our_rate)
print('开始日期字段准确率：',Date_count_our_rate)
print('结束日期字段准确率：',Date_start_count_our_rate)
print('全部字段准确率：',total_count_our_rate)
