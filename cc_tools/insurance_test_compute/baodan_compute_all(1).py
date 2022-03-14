import numpy as np
import os
import io

label_path = 'insurance_test_gt_3rd'
predict_path = 'insurance_test_pred_3rd_0.8'


list_path_real = os.listdir(label_path)
list_path_our = os.listdir(predict_path)

total_num = len(list_path_real)

detect_num = 0
Name_count_our = 0
Idnum_count_our = 0
Date_count_our = 0
Date_start_count_our = 0
Date_end_count_our = 0
total_count_our = 0

for i in range(0, len(list_path_real)):
    path_our = os.path.join(predict_path, list_path_real[i])
    path_real = os.path.join(label_path, list_path_real[i])
    #print(path_our)

    with open(path_real,'r',encoding='utf-8') as f_r:
        lines_r = f_r.readlines()
        tmp = []
        for r in lines_r:
            r = r.strip().split(":")[-1]
            if r != '':
                tmp.append(r)
        lines_r = tmp
        
    with open(path_our, 'r', encoding='UTF-8-sig') as f_p:
        lines_p = f_p.read()
        lines_p = lines_p.strip()
        lines_p = lines_p.split("\n")
        tmp = []
        for p in lines_p:
            if p != '':
                tmp.append(p)
        lines_p = tmp
    
    if len(lines_p) < 2:
        continue

    if len(lines_r) == 2:
        detect_num += 1
        if lines_r[0] == lines_p[0] and lines_r[1][-16:] == lines_p[1][-16:]:
            total_count_our += 1
            Idnum_count_our += 1
            Name_count_our += 1
            Date_start_count_our += 1
            Date_end_count_our += 1
        continue

    if len(lines_r) != len(lines_p):
        continue


    detect_num += 1

    if lines_r[0] == lines_p[0]:
        Name_count_our += 1
    #else:
        #print('保单号不匹配:', path_our)
        #print(lines_r)
        #print(lines_p)

    if lines_r[1][-16:] == lines_p[1][-16:]:
        Idnum_count_our += 1
    #else:
        #print('车架号不匹配:', path_our)
        #print(lines_r)
        #print(lines_p)
    if lines_r[2] == lines_p[2]:
        Date_start_count_our+=1
    #else:
        #print('日期1不匹配:', path_our)
        #print(lines_r)
        #print(lines_p)

    if lines_r[3] == lines_p[3]:
        Date_end_count_our+=1
    #else:
        #print('日期2不匹配:', path_our)
        #print(lines_r)
        #print(lines_p)

    if lines_r == lines_p:
        total_count_our+=1
    #else:
        #print("not match:", path_our)
        #print(lines_r)
        #print(lines_p)
        
        

Name_count_our_rate = Name_count_our / detect_num
Idnum_count_our_rate = Idnum_count_our / detect_num
Date_start_count_our_rate = Date_start_count_our / detect_num
Date_end_count_our_rate = Date_end_count_our / detect_num
total_count_our_rate = total_count_our / detect_num
print("total num = ", total_num)
print("detect num = ", detect_num)
print("succ rate = ", detect_num*1.0/total_num)
print('保险单号字段准确率：',Name_count_our_rate)
print('车架号码字段准确率：',Idnum_count_our_rate)
print('日期1字段准确率：',Date_start_count_our_rate)
print('日期2字段准确率：',Date_end_count_our_rate)
print('全部字段准确率：',total_count_our_rate)
