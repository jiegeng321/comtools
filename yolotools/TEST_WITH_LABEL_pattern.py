#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import os
import json

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import shutil
from comfunc.tools import check_dir
#pattern white test
# model_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/white_test_0401.json"
# label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/white_label.json"
#pattern test
# model_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online_0616_2.json"
# label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/label.json"
model_dir = None#"/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_test"
diff_dir = None#"/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/test_diff"
#pattern test
model_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online_0818_2.json"
label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/label.json"

score_th = {"adidas_h": 0.7, "coach_h": 0.5, "fendi_h": 0.65, "gucci_h": 0.6, "lv_h": 0.6, "michaelkors_h": 0.4, "nike_h": 0.7,
                'versace_h':0.7, 'christian_dior_h':0.75, 'goyard_h':0.6, 'burberry_h':0.6, 'issey_miyake_h':0.65, 'celine_h':0.6,
            "reebok_h":0.6,"mcm_h":0.75,"hermes_h":0.85,"van_cleef_arpels_h":0.8,"thom_browne_h":0.7}
# score_th = {"adidas_h": 0.45, "coach_h": 0.5, "fendi_h": 0.5, "gucci_h": 0.4, "lv_h": 0.4, "michaelkors_h": 0.4, "nike_h": 0.5,
#                 'versace_h':0.5, 'christian_dior_h':0.5, 'goyard_h':0.4, 'burberry_h':0.4, 'issey_miyake_h':0.45, 'celine_h':0.5,
#             "reebok_h":0.6,"mcm_h":0.65,"hermes_h":0.75,"van_cleef_arpels_h":0.65,"bottega_veneta_h":0.7}

score_th_other = 0.5

save_result_csv = None#"/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online_with_label_result.csv"
support_th = 10
show_pic = False
show_detail = True
if diff_dir and model_dir:
    check_dir(diff_dir,delete=True)
with open(model_json, 'r') as f:
    model_result = json.load(f)
#print(model_result)
model_result_th = {}
if score_th:
    for k,pre_list in model_result.items():
        pre_list_th = []
        for pre in pre_list:
            for key,value in pre.items():
                if key=="logo":
                    brand = value
                elif key=="score":
                    score = value
            if "border" in brand:
                brand = brand.replace("_border", "")
            if "small" in brand:
                brand = brand.replace("_small", "")
            if brand in score_th:
                if score >= score_th[brand]:
                    brand = brand.split("-")[0]
                    pre_list_th.append(brand)
            else:
                if score >= score_th_other:
                    brand = brand.split("-")[0]
                    pre_list_th.append(brand)
        if pre_list_th==[]:
            pre_list_th.append("empty")
        model_result_th[k]=list(set(pre_list_th))

    
with open(label_json, 'r') as f:
    label_result = json.load(f)
print(len(label_result))
print(len(model_result_th))
model_list = []
label_list = []
total_num = 0
diff_num = 0

for key,value in label_result.items():
    if key in model_result_th:
        total_num += 1

        if value=="empty" and len(model_result_th[key])>=2 and "empty" in model_result_th[key]:
            label_list.append(value)
            model_result_th[key].remove("empty")
            #print(model_result_th[key])
            model_list.append(max(sorted(model_result_th[key]), key=model_result_th[key].count))
        else:
            #if value.split("-")[0] in model_result_th[key]:
                #print(value)
            if value in model_result_th[key]:

                label_list.append(value)
                model_list.append(value)
            else:
                if model_result_th[key]==[]:#img has problem
                    continue
                if len(model_result_th[key])>=2 and "empty" in model_result_th[key]:
                    model_result_th[key].remove("empty")
                label_list.append(value)
                model_list.append(max(sorted(model_result_th[key]), key=model_result_th[key].count))

        if label_list[-1] != model_list[-1]:
            diff_num += 1
            print(f"diff:{diff_num},{label_list[-1]}:{model_list[-1]},{key},{model_result[key]}")
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
    if key=="accuracy" or key=="weighted avg" or key == "macro avg":# or key == "empty":
        continue
    if ite["support"]==0:
        continue
    ite["precision"] = round(ite["precision"],4)
    ite["recall"] = round(ite["recall"], 4)
    ite["f1-score"] = round(ite["f1-score"], 4)
    new_class_result[key] = [ite["support"],ite["recall"],ite["precision"],ite["f1-score"]]
pd_data = pd.DataFrame(new_class_result,index=["support","recall","precision","f1-score"])
    #print(key,item["support"])
pd_data = pd.DataFrame(pd_data.values.T,index=pd_data.columns,columns=pd_data.index)
#pd.set_option('max_colwidth',50)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd_data = pd_data.sort_values(by="support",ascending=False)
#print(pd_data)
# tmp = pd_data[pd_data["support"]>=10]
# print(tmp[tmp["recall"]<=0.93].index.tolist())
# print(len(tmp[tmp["recall"]<=0.93].index.tolist()))
if save_result_csv:
    pd_data.to_csv(save_result_csv)
#print(new_class_result)
# new_class_result = sorted(new_class_result.items(), key = lambda kv:(kv[1]["support"], kv[0]),reverse=True)
# for i in new_class_result:
#     print(i)
#print(type(new_class_result))
# print(pd_data[pd_data["support"]>=100].index.tolist())
# print(len(pd_data[pd_data["support"]>=100].index.tolist()))
print(total_num)
print(diff_num)
print(diff_num/total_num)
print("total test brand have:",len(pd_data[pd_data["support"]>=support_th]))
print("total test num:",pd_data["support"].sum())
# print("recall mean: ", pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]!=0.0)]["recall"].mean())
# print("recall mean: ", pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]!=0.0)]["precision"].mean())
print("recall mean: ", pd_data[pd_data["support"]>=support_th]["recall"].mean())
print("precision mean: ", pd_data[pd_data["support"]>=support_th]["precision"].mean())
if show_pic:
    pd_data_plt = pd_data["support"].iloc[:20]
    pd_data_plt.plot.bar()
    plt.rcParams['figure.figsize'] = (20.0, 4.0)
    plt.savefig("data_info/total.png",dpi=300)
if show_detail:
    print(pd_data[pd_data["support"]>=support_th])
print("\n")

problem_brand = pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]<=0.5)]
print("problem brands:")
print(problem_brand)


print("total test brand have:",len(pd_data[pd_data["support"]>=support_th]))
print("total test num:",pd_data["support"].sum())
# print("recall mean: ", pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]!=0.0)]["recall"].mean())
# print("recall mean: ", pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]!=0.0)]["precision"].mean())
print("recall mean: ", pd_data[pd_data["support"]>=support_th]["recall"].mean())
print("precision mean: ", pd_data[pd_data["support"]>=support_th]["precision"].mean())
if show_pic:
    pd_data_plt = pd_data["support"].iloc[:20]
    pd_data_plt.plot.bar()
    plt.rcParams['figure.figsize'] = (20.0, 4.0)
    plt.savefig("data_info/total.png",dpi=300)
if show_detail:
    print(pd_data[pd_data["support"]>=support_th])
print("\n")


fordeal_important_ = ["gucci_h","lv_h","adidas_h","michaelkors_h","coach_h","christian_dior_h","fendi_h","celine_h","burberry_h",
                      "goyard_h","versace_h","issey_miyake_h","mcm_h","van_cleef_arpels_h","reebok_h"]
fordeal_care = pd_data.loc[fordeal_important_,:]
print("fordeal care brand:",len(fordeal_care[fordeal_care["support"]>support_th]))
print("fordeal care test num:",fordeal_care["support"].sum())
print("recall mean: ", fordeal_care[fordeal_care["support"]>support_th]["recall"].mean())
print("precision mean: ", fordeal_care[fordeal_care["support"]>support_th]["precision"].mean())
#print(fordeal_care)
print(pd_data.loc["thom_browne_h","recall"],pd_data.loc["thom_browne_h","precision"])