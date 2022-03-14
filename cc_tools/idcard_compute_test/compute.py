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
diff_path = '.'
list_path_real = os.listdir(diff_path+'/real')
list_path_our = os.listdir(diff_path+'/our_paddle')
list_path_ten = os.listdir(diff_path+'/ten')
# print(list_path)
#useful_file = 0
#if not os.path.exists(savaFileName):
#    os.makedirs(savaFileName)
total_num = len(list_path_real)
Name_count_our = 0
Name_count_ten = 0
Sex_count_our = 0
Sex_count_ten = 0
Nation_count_our = 0
Nation_count_ten = 0
Birth_count_our = 0
Birth_count_ten = 0
Address_count_our = 0
Address_count_ten = 0
IdNum_count_our = 0
IdNum_count_ten = 0
total_char_our = 0
total_char_ten = 0
total_char_rate_our = 0
total_char_rate_ten = 0
char_list = ['Name','Sex','Nation','Birth','Address','IdNum']
def char_rate(str_in,str_true):
    len_ = len(str_true)
    count = 0
    for char in str_in:
        if char in str_true:
            count+=1
    if count>=len_:
        count=len_
    return count/len_
for i in range(0, len(list_path_real)):
    path_real = os.path.join(diff_path+'/real', list_path_real[i])
    path_our = os.path.join(diff_path+'/our_paddle', list_path_real[i])
    path_ten = os.path.join(diff_path+'/ten', list_path_real[i])
    #if os.path.isfile(jpath):
    data_real = json.load(open(path_real,encoding='utf-8-sig'))
    data_our = json.load(open(path_our,encoding='utf-8-sig'))
    data_ten = json.load(open(path_ten,encoding='utf-8-sig'))
    for char_ in char_list:
        total_char_rate_our += char_rate(data_our[char_],data_real[char_])
        total_char_rate_ten += char_rate(data_ten[char_], data_real[char_])
    if data_our['Name'] == data_real['Name'] and data_our['Sex'] == data_real['Sex']and data_our['Nation'] == data_real['Nation']and data_our['Birth'] == data_real['Birth']and data_our['Address'] == data_real['Address']and data_our['IdNum'] == data_real['IdNum']:
        total_char_our+=1
    if data_ten['Name'] == data_real['Name'] and data_ten['Sex'] == data_real['Sex']and data_ten['Nation'] == data_real['Nation']and data_ten['Birth'] == data_real['Birth']and data_ten['Address'] == data_real['Address']and data_ten['IdNum'] == data_real['IdNum']:
        total_char_ten+=1
    if data_our['Name']==data_real['Name']:
        Name_count_our+=1
    else:
        print('our:',data_our['Name'],'\treal:',data_real['Name'],list_path_real[i])
    if data_ten['Name'] == data_real['Name']:
        Name_count_ten += 1
    if data_our['Sex']==data_real['Sex']:
        Sex_count_our+=1
    else:
        print('our:',data_our['Sex'],'\treal:',data_real['Sex'],list_path_real[i])
    if data_ten['Sex'] == data_real['Sex']:
        Sex_count_ten += 1
    if data_our['Nation']==data_real['Nation']:
        Nation_count_our+=1
    else:
        print('our:', data_our['Nation'], '\treal:', data_real['Nation'], list_path_real[i])
    if data_ten['Nation'] == data_real['Nation']:
        Nation_count_ten += 1
    if data_our['Birth']==data_real['Birth']:
        Birth_count_our+=1
    else:
        print('our:', data_our['Birth'], '\treal:', data_real['Birth'], list_path_real[i])
    if data_ten['Birth'] == data_real['Birth']:
        Birth_count_ten += 1
    if data_our['Address']==data_real['Address']:
        Address_count_our+=1
    else:
        print('our:', data_our['Address'], '\treal:', data_real['Address'], list_path_real[i])
    if data_ten['Address'] == data_real['Address']:
        Address_count_ten += 1
    if data_our['IdNum']==data_real['IdNum']:
        IdNum_count_our+=1
    else:
        print('our:', data_our['IdNum'], '\treal:', data_real['IdNum'], list_path_real[i])
    if data_ten['IdNum'] == data_real['IdNum']:
        IdNum_count_ten += 1
Name_count_our_rate = Name_count_our/total_num
Name_count_ten_rate = Name_count_ten/total_num
Sex_count_our_rate = Sex_count_our/total_num
Sex_count_ten_rate = Sex_count_ten/total_num
Nation_count_our_rate = Nation_count_our/total_num
Nation_count_ten_rate = Nation_count_ten/total_num
Birth_count_our_rate = Birth_count_our/total_num
Birth_count_ten_rate = Birth_count_ten/total_num
Address_count_our_rate = Address_count_our/total_num
Address_count_ten_rate = Address_count_ten/total_num
IdNum_count_our_rate = IdNum_count_our/total_num
IdNum_count_ten_rate = IdNum_count_ten/total_num
total_count_our_rate = (Name_count_our+Sex_count_our+Nation_count_our+Birth_count_our+Address_count_our+IdNum_count_our)/(6*total_num)
total_count_ten_rate = (Name_count_ten+Sex_count_ten+Nation_count_ten+Birth_count_ten+Address_count_ten+IdNum_count_ten)/(6*total_num)
total_char_our_rate = total_char_our/total_num
total_char_ten_rate = total_char_ten/total_num
total_char_rate_our_all = total_char_rate_our/(6*total_num)
total_char_rate_ten_all = total_char_rate_ten/(6*total_num)
our = [total_char_rate_our_all,total_char_our_rate,Name_count_our_rate,Sex_count_our_rate,Nation_count_our_rate,Birth_count_our_rate,Address_count_our_rate,IdNum_count_our_rate,total_count_our_rate]
ten = [total_char_rate_ten_all,total_char_ten_rate,Name_count_ten_rate,Sex_count_ten_rate,Nation_count_ten_rate,Birth_count_ten_rate,Address_count_ten_rate,IdNum_count_ten_rate,total_count_ten_rate]
compu_data = np.array([our,ten])
print(total_num)
df = pd.DataFrame(compu_data,index=['自研','Tencent'],columns=['全部字符准确率','全部准确率','姓名字段准确率','性别字段准确率','民族字段准确率','出生字段准确率','住址字段准确率','身份号码字段准确率','综合字段准确率'])
print(df)

