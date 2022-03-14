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
#diff_path = 'compare_with_ten_files_compute/total_for_compute'
label_path = './paper_label_new'
predict_path = 'paper_crnn_result'
list_path_real = os.listdir(label_path)
list_path_our = os.listdir(predict_path)
#list_path_ten = os.listdir(diff_path+'/ten')
# print(list_path)
#useful_file = 0
#if not os.path.exists(savaFileName):
#    os.makedirs(savaFileName)
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
        #print(path_real)
        lines_r = f_r.read()
        lines_r = lines_r.strip('\n').strip('{').strip('}')
        lines_r = lines_r.split(' ')
        a = '姓名：' + lines_r[3][6:] + '\n'
        b = '身份证号：' + lines_r[4][3:] + '\n'
        c = '有效期至：' + lines_r[5][5:].strip('"') + '\n'
        lines_r = [a, b, c]
        with open(path_our,'r',encoding='utf-8') as f_p:
            lines_p = f_p.read()
            #print(lines_p)
            lines_p = lines_p.strip('\n').strip('{').strip('}')
            lines_p = lines_p.split(' ')

            a = '姓名：'+lines_p[3][6:]+'\n'
            b = '身份证号：' + lines_p[4][3:]+'\n'
            c = '有效期至：' + lines_p[5][5:].strip('"')+'\n'
            lines_p = [a,b,c]
            #print(lines_p)
    if lines_r==lines_p:
        total_count_our+=1
    #else:
    #    print('all_diff:',path_our)
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

print(Name_count_our,Idnum_count_our,total_count_our)
Name_count_our_rate = Name_count_our / total_num
Idnum_count_our_rate = Idnum_count_our / total_num
Date_count_our_rate = Date_count_our / total_num
total_count_our_rate = total_count_our / total_num

print('姓名字段准确率：',Name_count_our_rate)
print('身份号码字段准确率：',Idnum_count_our_rate)
print('有效期字段准确率：',Date_count_our_rate)
print('全部字段准确率：',total_count_our_rate)