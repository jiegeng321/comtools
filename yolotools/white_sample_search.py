#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

# 检查品牌是否中1000logo中
# 将不在logo1000中的数据复制到另一目录

import os
import random
import glob
import shutil
from pathlib import Path
from func.path import ospathjoin
from func.check import check_dir
from tqdm import tqdm
import pandas as pd

weblogo2m_list1=['3m','adidas','aldi','alfaromeo','allianz','amazon','android']
weblogo2m_list2=['apple','armani','asus','bacardi','bankofamerica','barbie','barclays',
'basf','batman','bayer','bbc','bbva','becks','bershka','blizzardentertainment',
'bmw','boeing','bottegaveneta','bulgari','calvinklein','canon','carlsberg',
'carters','cartier','caterpillar','chanel','chevrolet','chevron','chickfila',
'chimay','chiquita','cisco','citi']
weblogo2m_list3=['coach','cocacola','colgate','comedycentral','converse','corona','costco','cvs',
'danone','dhl','disney','drpepper','dunkindonuts','ebay','erdinger','espn'
'esso','evernote',]
weblogo2m_list4=['facebook','fedex','ferrari','firefox','ford','fosters','fritolay','gap',
'generalelectric','gildan','gillette','goodyear','google','gucci','guiness',
'hanes','heineken','hermes','hershey','hh','homedepot'
]
weblogo2m_list5=['honda','hp','hsbc','hyundai','ikea','intel','internetexplorer','jackinthebox',
'jagermeister','jcrew','johnnywalker','kelloggs','kfc','kodak','kraft','lacoste',
'lamborghini','lego','levis','lexus','lg','londonunderground','loreal',
'louisvuitton','luxottica','marlboro','maserati','mastercard','mcdonald',
'michelin','microsoft','milka','millerhighlife','mitsubishi','mk','mobil']
weblogo2m_list6=['motorola','mtv','nasa','nbc','nescafe','nestle','netflix','nike','nintendo',
'nissan','northface','nvidia','obey','olympics','oracle','pampers','panasonic',
'paulaner','pepsi','philips','playstation','poloralphlauren','porsche']
weblogo2m_list7=['prada','puma','rbc','recycling','redbull','reebok','renault','republican',
'rittersport','rolex','samsung','santander','sap','schwinn','sega','shell',
'siemens','singha','skechers','soundcloud','soundrop','spiderman','starbucks',
'stellaartois','subaru','subway','superman','supreme','suzuki','tacobell',
'teslamotors','texaco','thomsonreuters','timberland','tissot','tommyhilfiger',
'toyota','tsingtao','underarmour','uniqlo','unitednations','ups','vaio','visa',
'volkswagen','volvo','walmart','warnerbros','wellsfargo','wii']
weblogo2m_list8=['windows','wordpress','xbox','yamaha','youtube','zara'
]

#open_logo_list=weblogo2m_list8

dst_dir = "/data01/xu.fx/dataset/white_sample_factory/raw_white_images_from_open_dataset/WebLogo-2M/"
open_dataset_dir = "/data01/xu.fx/dataset/open_dataset/WebLogo-2M/3/"
check_dir(dst_dir)
open_logo_list = os.listdir(open_dataset_dir) #weblogo2m_list2

logo1000 = pd.read_csv("/data01/xu.fx/dataset/open_dataset/LOGO1000.csv")
logo1000_list = logo1000["品牌"].tolist()
logo1000_list_low = []
for i in logo1000_list:
    logo1000_list_low.append(i.replace(" ","").replace("'","").replace("-","").replace("&","").replace("\n","").replace(".","").lower())
print(logo1000_list_low)
need_logo = []
for logo in tqdm(open_logo_list):
    if logo.replace(" ","").replace("'","").replace("-","").replace("&","").replace("\n","").replace(".","").lower() in logo1000_list_low:
        pass
    else:
        print(logo)
        need_logo.append(logo)
        files = os.listdir(os.path.join(open_dataset_dir,logo))
        for f in files:
            if f.split(".")[-1] != "xml":
                shutil.copy(os.path.join(open_dataset_dir,logo,f),os.path.join(dst_dir,logo+"_"+f))
print(len(need_logo))
print(need_logo)


'''
empty_dir = "/data01/xu.fx/dataset/white_sample_factory/comb_model_process_raw_images/empty"
test_dir = "/data01/xu.fx/dataset/comb_data/yolo_dataset_comb_209bs_345ks/JPEGImages/test"
white_black_test_dir = test_dir.replace("test","white_black_test")

black_samples_num = 10000
white_black_ratio = [0.7, 0.3]
random_seed = 1

check_dir(white_black_test_dir)
check_dir(os.path.join(white_black_test_dir, "images"))
check_dir(os.path.join(white_black_test_dir, "labels"))

test_files = os.listdir(os.path.join(test_dir,"images"))
if black_samples_num:
    test_num = black_samples_num
else:
    test_num = len(test_files)

empty_files = os.listdir(empty_dir)
empty_num = len(empty_files)

need_empty_num = int(test_num*(white_black_ratio[0]/white_black_ratio[1]))
if empty_num<need_empty_num:
    need_empty_num=empty_num

random.seed(random_seed)
random.shuffle(test_files)
random.seed(random_seed)
random.shuffle(empty_files)
print("white samples num:", need_empty_num)
print("black samples num:", test_num)
print("coping white samples")
for i in tqdm(range(need_empty_num)):
    shutil.copy(os.path.join(empty_dir,empty_files[i]),os.path.join(white_black_test_dir,"images"))
    with open(os.path.join(white_black_test_dir,"labels",empty_files[i].replace(empty_files[i].split(".")[-1],"txt")),'w') as f:
        pass
print("coping black samples")
for j in tqdm(range(test_num)):
    shutil.copy(os.path.join(test_dir,"images", test_files[j]), os.path.join(white_black_test_dir, "images"))
    shutil.copy(os.path.join(test_dir,"labels", test_files[j].replace(test_files[j].split(".")[-1],"txt")), os.path.join(white_black_test_dir, "labels"))
'''