#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from pathlib import Path

import requests

from func.funcxml import readxml
import cv2
import random
from func.print_color import bcolors
import os
import shutil
from func.check import check_dir
import ast
txt_path = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/1229-1231.txt"
dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_data_for_logo_test"
#need_num = 50000
# need_brand = {"miu_miu":10000,"converse":10000,"loewe":10000,"seiko":10000,"mcm":10000,"guess":10000,"citizen":10000,"chloe":10000,
#               "fossil":10000,"jeep":10000,"tory_burch":10000,"playboy":10000,"casio":10000,"chaumet":10000,"zara":10000,
#               "lamborghini":10000,"bmw":10000,"philipp_plein":10000,"valentino_garavani":10000,"estee_lauder":10000,
#               "timberland":10000,"vacheron_constantin":10000,"pandora":10000,"piaget":10000,"blancpain":10000,
#               "girard_perregaux":10000,"coca_cola":10000,"dkny":10000,"comme_des_garcons":10000,"paul_shark":10000,
#               "lyle_scott":10000,"ellesse":10000,"moschino":10000,"jabra":10000,"zegna":10000,"gant":10000,"panerai":10000,
#               "tudor":10000,"franck_muller":10000,"zenith":10000,"movado":10000,"bally":10000,"diesel":10000,"caterpillar":10000,
#               "reebok":10000,"bosch":10000,"escada":10000,"davidoff":10000,"dr_martens":10000,"dunhill":10000,"evisu":10000,
#               "clinique":10000,"juicy_couture":10000,"audi":10000,"mlb":10000,"glashutte_original":10000}
#{'autoCheckResult': 'Reject', 'autoCheckTime': 1640829053049, 'commodityUrlId': '1640814835440828705', 'crawlTaskId': '0', 'finalCheckResult': 'Accept', 'finalTagHit': '', 'gmtCreate': 1640814835519, 'id': '1640814835519418071', 'imageId': 'p-comp/1640827048145000Y0A9D59580030001', 'imageSize': '106252', 'isScreenshot': 0, 'lastChecker': '刘丹', 'ruleHit': '图像识别品牌【侵权/品牌/louis_vuitton】', 'seqId': '1640829052949000Y0A9D729C0036001', 'status': 3, 'tagHit': '[图像]侵权/品牌/louis_vuitton', 'taskId': '113402', 'taskUrlId': '0', 'textData': 'https://s3.forcloudcdn.com/item/images/dmc/8bcbfa32-b64d-4db4-b889-237572b24611-728x728.jpg', 'type': 1}
need_brand = {'gucci':10000, 'michael_kors':10000, 'coach':10000, 'adidas':10000, 'louis_vuitton':10000, 'fendi':10000, 'nike':10000, 'versace':10000, 'goyard':10000, 'burberry':10000, 'issey_miyake':10000, 'christian_dior':10000, 'celine':10000}
get_brand = {}

# if not os.path.exists(dst_dir):
#     os.makedirs(dst_dir)
with open(txt_path,"r") as f:
    data = f.readlines()
print("total lines :",len(data))
print("need brand :",need_brand)
downloaded_images = 0
for index,line in enumerate(data):
    downloaded_per_list = 0
    dict_brand = ast.literal_eval(line)
    #if dict_brand["finalCheckResult"]=="Reject":#Reject
    img_list = dict_brand["imageCommodityData"]
    #print(index,":",img_list)

    for img in img_list:
        try:
            auto_result = img["autoCheckResult"]
            final_result = img["finalCheckResult"]
            if auto_result == "Reject" and final_result == "Accept" and "图像识别品牌【侵权/品牌" in img["ruleHit"]:
                print(img)
                url = img["textData"]
                final_brand_raw = list(set(img["ruleHit"].split(",")))
                if final_brand_raw==[]:
                    continue
                #print(final_brand_raw)
                final_brand = []
                for brand in final_brand_raw:
                    if "图像识别品牌【侵权/品牌" in brand:
                        final_brand.append(brand)
                #print(final_brand)
                if final_brand==[]:
                    continue
                print_name = final_brand[0].split("/")[-1].split("】")[0]
                if len(final_brand)>=2:
                    for final in final_brand[1:]:
                        print_name += "_"+final.split("/")[-1].split("】")[0]
                final_brand = max(final_brand,key=final_brand.count)
                final_brand = final_brand.split("/")[-1].split("】")[0]

                #print(final_brand)
                if final_brand in need_brand:
                    if final_brand in get_brand and get_brand[final_brand]>=need_brand[final_brand]:
                        print(f"brand {final_brand} is enough,get {get_brand[final_brand]} images")
                        continue
                    else:
                        if final_brand in get_brand:
                            get_brand[final_brand] += 1
                        else:
                            get_brand[final_brand] = 1
                else:
                    continue

                img_name = url.split("/")[-1]
                resq = requests.get(url)
                if len(resq.content) > 250:
                    img_out = os.path.join(dst_dir,final_brand)
                    if not os.path.exists(img_out):
                        os.makedirs(img_out)
                    open(os.path.join(img_out,print_name+"_"+img_name), 'wb').write(resq.content)
                    downloaded_images += 1
                    downloaded_per_list += 1
                    # if downloaded_images>=need_num:
                    #     print("images is enough %d"%downloaded_images)
                    #     exit()
                else:
                    continue
        except Exception as e:
            print(e)
            continue
    print(index,"this list has %d images,have downloaded %d/%d,total downloaded %d" %(len(img_list),downloaded_per_list,len(img_list),downloaded_images))
    if index%10==0:
        find_all=1
        if len(get_brand)==len(need_brand):
            for k,v in get_brand.items():
                if v<need_brand[k]:
                    find_all=0
        else:
            find_all = 0
        if find_all==1:
            print("final index:",index)
            print(f"get images: {get_brand}")
            exit()
        print(f"get images: {get_brand}")




