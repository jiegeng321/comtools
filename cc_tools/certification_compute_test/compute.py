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

label_path = './label'
predict_path = './predict'
list_path_real = os.listdir(label_path)
list_path_our = os.listdir(predict_path)

total_num = len(list_path_real)
Name_count_our = 0
Idnum_count_our = 0
Date_count_our = 0
total_count_our = 0
#char_list = ['Name','Idnum','Date']
def char_rate(str_in,str_true):
    len_ = len(str_true)
    count = 0
    for char in str_in:
        if char in str_true:
            count+=1
    if count>=len_:
        count=len_
    return count/len_
for i in tqdm(range(0, len(list_path_real))):
    path_real = os.path.join(label_path, list_path_real[i])
    path_our = os.path.join(predict_path, list_path_our[i])
    with open(path_real,'r',encoding='utf-8') as f_r:
        lines_r = f_r.readlines()
        with open(path_our,'r',encoding='utf-8') as f_p:
            lines_p = f_p.readlines()
    if lines_r==lines_p:
        total_count_our+=1
    r = lines_r
    p = lines_p
    if r[0] == p[0]:
        Name_count_our+=1
    else:
        print('name_diff:',list_path_our[i])
    if r[1] == p[1]:
        Idnum_count_our+=1
    else:
        print('idnum_diff:',list_path_our[i])
    if r[2] == p[2]:
        Date_count_our+=1
    else:
        print('date_diff:',list_path_our[i])

Name_count_our_rate = Name_count_our / total_num
Idnum_count_our_rate = Idnum_count_our / total_num
Date_count_our_rate = Date_count_our / total_num
total_count_our_rate = total_count_our / total_num

print('姓名字段准确率：',Name_count_our_rate)
print('身份号码字段准确率：',Idnum_count_our_rate)
print('有效期字段准确率：',Date_count_our_rate)
print('全部字段准确率：',total_count_our_rate)