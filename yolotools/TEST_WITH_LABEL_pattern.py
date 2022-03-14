#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import os
import json


import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import shutil
from func.tools import check_dir
fordeal_important = pd.read_excel("fordeal重点品牌分析详情1028.xlsx")
fordeal_important = fordeal_important.iloc[:,0].tolist()
model_dir = None#"/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/online_comlogo_0118_wts"
diff_dir = None#"/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/test_diff"
model_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online_02103.json"
support_th = 50
fordeal_care = False
label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/label.json"
save_result_csv = None#"/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online_with_label_result.csv"
if diff_dir and model_dir:
    check_dir(diff_dir,delete=True)
with open(model_json, 'r') as f:
    model_result = json.load(f)
with open(label_json, 'r') as f:
    label_result = json.load(f)
model_list = []
label_list = []
total_num = 0
diff_num = 0

for key,value in label_result.items():
    # if value!="empty":
    #     value = value+"_h"
    if key in model_result:
        total_num += 1
        # if "lv" in model_result[key]:
        #     model_result[key].remove("lv")
        #     model_result[key].append("louis_vuitton")

        if value=="empty" and len(model_result[key])>=2 and "empty" in model_result[key]:
            label_list.append(value)
            model_result[key].remove("empty")
            #print(model_result[key])
            model_list.append(max(model_result[key], key=model_result[key].count))
        else:
            #if value.split("-")[0] in model_result[key]:
                #print(value)
            if value in model_result[key]:
                label_list.append(value)
                model_list.append(value)
            else:
                if model_result[key]==[]:#img has problem
                    continue
                if len(model_result[key])>=2 and "empty" in model_result[key]:
                    model_result[key].remove("empty")
                label_list.append(value)
                model_list.append(max(model_result[key], key=model_result[key].count))

        if label_list[-1] != model_list[-1]:
            diff_num += 1
            print(f"diff:{diff_num},{label_list[-1]}:{model_list[-1]}")
            if diff_dir and model_dir:
                for brand in os.listdir(model_dir):
                    if key in os.listdir(os.path.join(model_dir,brand)):
                        shutil.copy(os.path.join(model_dir,brand,key),os.path.join(diff_dir,label_list[-1]+"_"+model_list[-1]+"_"+key))

#print(label_list)
#print(model_list)
label_out_num = len(label_list) - label_list.count("empty")
model_out_num = len(model_list) - model_list.count("empty")
print(label_out_num/total_num)
print(model_out_num/total_num)
print(total_num)
print(diff_num)
print(diff_num/total_num)

#print(label_list)
#print(model_list)
class_result = classification_report(label_list, model_list,zero_division=False,output_dict=True)
#print(class_result)
#print(class_result["mcm"])

new_class_result = {}
for key,ite in class_result.items():
    if key=="accuracy" or key=="weighted avg" or key == "macro avg" or key == "empty":
        continue
    if ite["support"]==0:
        continue
    ite["precision"] = round(ite["precision"],2)
    ite["recall"] = round(ite["recall"], 2)
    ite["f1-score"] = round(ite["f1-score"], 2)
    new_class_result[key] = [ite["support"],ite["recall"],ite["precision"],ite["f1-score"]]
pd_data = pd.DataFrame(new_class_result,index=["support","recall","precision","f1-score"])
    #print(key,item["support"])
pd_data = pd.DataFrame(pd_data.values.T,index=pd_data.columns,columns=pd_data.index)
#pd.set_option('max_colwidth',50)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd_data = pd_data.sort_values(by="support",ascending=False)
print(pd_data)
# tmp = pd_data[pd_data["support"]>=10]
# print(tmp[tmp["recall"]<=0.93].index.tolist())
# print(len(tmp[tmp["recall"]<=0.93].index.tolist()))

pd_data.to_csv(save_result_csv)
#print(new_class_result)
# new_class_result = sorted(new_class_result.items(), key = lambda kv:(kv[1]["support"], kv[0]),reverse=True)
# for i in new_class_result:
#     print(i)
#print(type(new_class_result))
print("total test brand fordeal have: ",len(pd_data[pd_data["support"]>=support_th]))
print("recall mean: ", pd_data[pd_data["support"]>=support_th]["recall"].mean())
print("precision mean: ", pd_data[pd_data["support"]>=support_th]["precision"].mean())
if fordeal_care:
    for i in fordeal_important:
        if i not in pd_data.index.tolist():
            fordeal_important.remove(i)
    fordeal_important.remove('seiko')
    fordeal_care = pd_data.loc[fordeal_important,:]
    #print(fordeal_care)
    print("fordeal care brand:",len(fordeal_care[fordeal_care["support"]>20]))
    #print("recall mean: ", pd_data.loc[fordeal_important,"support"].min())
    print("recall mean: ", fordeal_care[fordeal_care["support"]>20]["recall"].mean())
    print("precision mean: ", fordeal_care[fordeal_care["support"]>20]["precision"].mean())
#print("precision mean: ", pd_data[pd_data.index in fordeal_important]["precision"])

#print("total test brand fordeal have: ",len(pd_data[pd_data["recall"]!=0].iloc[:,0]))
#print(pd_data[pd_data["recall"]!=0].index)

# logo_list = sorted(pd_data[pd_data["recall"]!=0].index.tolist())
# for i in logo_list:
#     print(i)

# print("recall mean: ", len(pd_data[pd_data["recall"]>0]))
# print("recall mean: ", pd_data["recall"].mean())
# print("precision mean: ", pd_data["precision"].mean())
# print("recall mean: ", pd_data[pd_data["recall"]>0]["recall"].mean())
# print("precision mean: ", pd_data[pd_data["recall"]>0]["precision"].mean())
#print(len(pd_data[pd_data["f1-score"]==0]))
#print(len(pd_data[pd_data["f1-score"]==0])/1418)