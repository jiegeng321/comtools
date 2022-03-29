#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import ast
import os
import requests
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import classification_report
#线上数据的txt文件
txt_paths = ["/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0301-0309.txt",
             "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0310-0319.txt"]
#csv输出目录
save_result_csv_dir = "./"
name = "txt_to_csv.csv"
num = None


lines = []
for txt_path in txt_paths:
    with open(txt_path, "r") as f:
        lines += f.readlines()

#{"autoCheckResult":"Reject","category":"Modelless suit;无模特套装","checkStatus":1,"commodityId":"34436835","commodityPend":0,"crawlTaskId":"0","finalCheckResult":"Reject","finalTagHit":"[图像]侵权/品牌/nike,[文本]侵权/品牌/nike","gmtCreate":1647896413239,"id":"1647896413239724233","imageAutoCheckResult":"Reject","imageCommodityData":[{"autoCheckResult":"Reject","autoCheckTime":1647909792434,"commodityUrlId":"1647896413239724233","crawlTaskId":"0","finalCheckResult":"Reject","finalTagHit":"[图像]侵权/品牌/nike","gmtCreate":1647896413284,"id":"1647896413284396118","imageId":"p-comp/1647909201385000Y8C9F6D2D0030001","imageSize":"224269","isScreenshot":0,"lastChecker":"胡国玉","ruleHit":"图像识别品牌【侵权/品牌/nike】","seqId":"1647909792379000Y8C8F62600030001","status":3,"tagHit":"[图像]侵权/品牌/nike","taskId":"212182","taskUrlId":"0","textData":"https://s3.forcloudcdn.com/item/images/dmc/18c17623-1dc2-4f21-9a6f-ee50151ea537-750x750.jpeg","type":1}
#{"autoCheckResult":"Accept","autoCheckTime":1647909775974,"commodityUrlId":"1647896413239563947","crawlTaskId":"0","finalCheckResult":"Accept","finalTagHit":"","gmtCreate":1647896413284,"id":"1647896413284783127","imageId":"p-comp/1647909229496000Y8C9F52200030001","imageSize":"380863","isScreenshot":0,"lastChecker":"胡国玉","seqId":"1647909775960000Y8C8F30C90030001","status":3,"taskId":"212182","taskUrlId":"0","textData":"https://s3.forcloudcdn.com/item/images/dmc/1b51bbf6-0d47-4bcc-9e31-df4fc5ab119c-1080x1080.jpeg","type":1}
if num:
    lines = lines[:num]

print("total lines :",len(lines))
max_line = 50
with open(os.path.join(save_result_csv_dir,"txt_to_csv.csv"),"w") as f:
    f.write("商品ID,人审标签,图片URL"+", "*(max_line-1)+"\n")
    for line in tqdm(lines):
        dict_brand = ast.literal_eval(line)
        if "commodityId" in dict_brand and "imageCommodityData" in dict_brand and "finalTagHit" in dict_brand:
            list_per_pic = dict_brand["imageCommodityData"]
            id = dict_brand["commodityId"]
            final_result = dict_brand["finalTagHit"].replace(",",".")
            urls = []
            for per_pic in list_per_pic:
                if "textData" in per_pic:
                    urls.append(per_pic["textData"])
            str = id+","+final_result+","
            if len(urls) > max_line:
                urls = urls[:max_line]
            for u in urls:
                str += u+","
            for nu in range(max_line-len(urls)):
                str += " ,"
            f.write(str+"\n")

