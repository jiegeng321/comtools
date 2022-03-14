#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""
import argparse
import copy
import pandas as pd

def read_csv(csv_path):
    if csv_path.endswith('.xlsx'):
        csv = pd.read_excel(csv_path, keep_default_na=False)
    elif csv_path.endswith('.csv'):
        csv = pd.read_csv(csv_path, keep_default_na=False)
    else:
        print("the format is not support!")
        exit()
    return csv

def get_label(label_str, all_labels={}, statics={}):
    label_str = label_str.split(",")
    first_label = []
    second_label = []
    third_label = []

    for i in label_str:
        i = i.strip("[图像]")
        sd = i.split('/')
        if len(sd)==1:
            first_label.append(sd[0].lower())
        elif len(sd) == 2:
            first_label.append(sd[0].lower())
            second_label.append(sd[1].lower())
        else:
            first_label.append(sd[0].lower())
            second_label.append(sd[1].lower())
            if sd[2].lower()=="new_york_yankees":
                sd[2] = "mlb"
            elif sd[2].lower()=="dolce_gabbana":
                sd[2] = "dolce"
            elif sd[2].lower()=="dior":
                sd[2] = "christian_dior"
            elif sd[2].lower()=="offwhite":
                sd[2] = "off_white"
            elif sd[2] == "kenzo_takada":
                sd[2] = "kenzo"
            elif sd[2] == "black_panther":
                sd[2] = "marvel"
            elif sd[2] == "ray_ban":
                sd[2] = "rayban"
            else:
                pass
            third_label.append(sd[2].lower())
            if sd[2].lower() not in all_labels:
                all_labels[sd[2].lower()]={"召回率":0, "查准率":0}
                statics[sd[2].lower()] = {"tp":0, "fp":0, 'taget':0}
    return list(set(first_label)), list(set(second_label)), list(set(third_label))

def autoVSfinal(autolabel, finallabel, isUpdate, static_res={}):
    flag = False
    if not isUpdate:
        for a_l in autolabel:
            if a_l in finallabel:
                flag = True
        return flag

    for f_l in finallabel:
        if f_l!="":
            if f_l in static_res:
                static_res[f_l]['taget'] += 1

    for a_l in autolabel:
        if a_l in finallabel:
            if a_l in static_res:
                static_res[a_l]['tp'] +=1
                flag = True
        else:
            static_res[a_l]["fp"] += 1

    return flag

def get_data(csv, filename, atten_list=[]):
    print(csv.keys())
    product_id = "商品ID"
    person_label = "人审标签"
    person_res = "人审结果"
    auto_label = "机审标签"
    auto_res = "机审结果"

    total_products = len(csv[product_id])
    p_r_a_r = 0
    p_r_a_a = 0
    a_r_p_a = 0
    a_r_p_r = 0

    total_labels = dict()
    statics_num = dict()
    for p_labels, p_res, auto_labels, auto_res in zip(csv[person_label], csv[person_res], csv[auto_label], csv[auto_res]):
        if p_res == "Accept" and auto_res == "Accept":
            continue

        finalfirstlabel, finalsecondlabel, finalthirdlabel = get_label(p_labels, total_labels, statics_num)
        autofirstlabel, autosecondlabel, autothirdlabel = get_label(auto_labels, total_labels, statics_num)
        if p_res == "Reject":
            fres = autoVSfinal(autothirdlabel, finalthirdlabel, True, static_res=statics_num)
            if fres:
                p_r_a_r += 1
            else:
                p_r_a_a += 1
        if auto_res== "Reject":
            fres = autoVSfinal(finalthirdlabel, autothirdlabel, False)
            if not fres:
                a_r_p_a += 1
            else:
                a_r_p_r += 1


    for brand_name, quota in total_labels.items():
        taget = statics_num[brand_name]['taget']
        tp = statics_num[brand_name]['tp']
        fp = statics_num[brand_name]['fp']
        total_labels[brand_name]["品牌出现次数"] = taget
        if tp==0:
            total_labels[brand_name][list(quota.keys())[0]]=0
            total_labels[brand_name][list(quota.keys())[1]]=0
        else:
            total_labels[brand_name][list(quota.keys())[0]] = round(tp / taget, 3)
            total_labels[brand_name][list(quota.keys())[1]] = round(tp / (fp + tp), 3)

    xlsx_str = f"{filename}_out.xlsx"
    temp = sorted(total_labels.items(), key=lambda kv: kv[1]['品牌出现次数'], reverse=True)
    print(temp)
    print(f"所有商品数量: {total_products}")
    print(f"当人审标签包含某品牌，但机身标签也包含该品牌的商品数量: {p_r_a_r}")
    print(f"当人审标签包含某品牌，但机身标签不包含该品牌的商品数量: {p_r_a_a}")
    print(f"当机审标签包含某品牌，但人审标签不包含该品牌的商品数量: {a_r_p_a}")
    print(f"以人审标签为准情况下，机审召回率: {round(p_r_a_r / (p_r_a_r + p_r_a_a), 2)}")
    print(f"以人审标签为准情况下，机审查准率: {round(p_r_a_r / (a_r_p_a + a_r_p_r), 2)}")
    column_item = ['品牌','fordeal关注', '品牌出现次数', '召回', '查准', '所有商品数量', '人审正，机审负', "人审正，机审正", "机审正，人审负",'人审标签为准,机审召回率', '人审标签为准,机审查准率']
    brand_name = [i[0] for i in temp]
    values = [i[1] for i in temp]
    data = []
    if brand_name[0] in atten_list:
        oo1 = [brand_name[0],'是' ,values[0]['品牌出现次数'], values[0]['召回率'], values[0]['查准率'],  total_products, p_r_a_r, p_r_a_a, a_r_p_a, round(p_r_a_r / (p_r_a_r + p_r_a_a), 2), round(p_r_a_r / (a_r_p_a + a_r_p_r), 2)]
    else:
        oo1 = [brand_name[0], '否', values[0]['品牌出现次数'], values[0]['召回率'], values[0]['查准率'], total_products, p_r_a_r, p_r_a_a, a_r_p_a, round(p_r_a_r / (p_r_a_r + p_r_a_a), 2), round(p_r_a_r / (a_r_p_a + a_r_p_r), 2)]
    data.append(oo1)
    for index, (brand, value) in enumerate(zip(brand_name, values)):
        if index==0:
            continue
        if brand in atten_list:
            data.append([brand, '是', value['品牌出现次数'], value['召回率'], value['查准率']])
        else:
            data.append([brand, '否', value['品牌出现次数'], value['召回率'], value['查准率']])
    tmp_xls = pd.DataFrame(data, columns=column_item)
    tmp_xls.to_excel(xlsx_str)



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=str, required=True, help="the input table path.")
    parser.add_argument("-a", type=str, default="", help="the input table path.")
    args = parser.parse_args()
    #args.t = "/data01/xu.fx/comtools/yolotools/1.18~2.17审核数据.xlsx"
    xlsx_file = args.t
    attention_file = args.a
    if attention_file=="":
        atten_List = []
    else:
        atten_csv = read_csv(attention_file)
        atten_List = [i.lower().replace(' ', '_') for i in atten_csv['英文名'] if i!= ""]
    file_name = xlsx_file.split('/')[-1].split('.')[0]
    csv = read_csv(xlsx_file)
    get_data(csv, file_name, atten_List)