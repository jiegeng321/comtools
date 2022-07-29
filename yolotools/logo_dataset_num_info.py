#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import pickle
import pandas as pd
csv_path = "/data01/xu.fx/comtools/yolotools/data_info/yolodataset_logo_784bs_1394ks_0715_brand_info.csv"
save_name = "logo_brand_info.pkl"
brand_csv_data = pd.read_csv(csv_path)
BRAND = []
brand_data = {}
for i in brand_csv_data.iterrows():
    #print(i[1])
    #print(i[1]["Unnamed: 0"],i[1]["total_brand_num"],i[1]["dataset_brand_num"])
    if not pd.isna(i[1]["dataset_brand_num"]):
        BRAND.append({"name":i[1]["Unnamed: 0"],"value":i[1]["dataset_brand_num"]})
    #break

print(BRAND)
print(len(BRAND))

pickle.dump(BRAND,open(save_name,"wb"))
data=pickle.load(open(save_name,"rb"))
print(data)
print(len(data))
