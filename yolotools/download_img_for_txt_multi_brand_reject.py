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
txt_paths = ["/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/1207-1210.txt",
             "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/1201-1206.txt",
             "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/1130.txt",
             "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/1127-1129.txt"]
dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_data_pattern_reebok_mcm"
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
#need_brand = {'gucci':10000, 'michael_kors':10000, 'coach':10000, 'adidas':10000, 'louis_vuitton':10000, 'fendi':10000, 'nike':10000, 'versace':10000, 'goyard':10000, 'burberry':10000, 'issey_miyake':10000, 'christian_dior':10000, 'celine':10000}

need_brand = {"reebok":5000,"mcm":3000}
donot_need_brand = ["all"]#['hello_kitty', 'jeep', 'salvatore_ferragamo', 'longines', 'van_cleef_arpels', 'casio', 'playboy', 'prada', 'tory_burch', 'fila', 'mlb', 'versace', 'new_balance', 'nike', 'rolex', 'converse', 'armani', 'franco_moschino', 'miu_miu', 'valentino_garavani', 'under_armour', 'calvin_klein', 'puma', 'vans', 'balenciaga', 'chanel', 'tommy_hilfiger', 'asics', 'supreme', 'patek_philippe', 'omega', 'lacoste', 'hugo_boss', 'louis_vuitton', 'swarovski', 'levis', 'chloe', 'mcm', 'hermes', 'michael_kors', 'moncler', 'loewe', 'the_north_face', 'cartier', 'ralph_lauren', 'alexander_mcqueen', 'bottega_veneta', 'coach', 'mercedes_benz', 'philipp_plein', 'juventus', 'canada_goose', 'celine', 'fendi', 'gucci', 'guess', 'adidas', 'vacheron_constantin', 'zara', 'givenchy', 'christian_louboutin', 'jimmy_choo', 'burberry', 'tiffany_co', 'bape', 'balmain', 'bvlgari', 'reebok', 'fc_barcelona_fcb', 'hublot', 'ellesse', 'panerai', 'lego', 'iwc', 'nba', 'timberland', 'porsche', 'fossil', 'citizen', 'ugg', 'nasa', 'stussy', 'tissot', 'bally', 'pandora', 'audemars_piguet']
donot_need_num = 0
auto_result_filter = None#"Reject"
final_result_filter = "Reject"


get_brand = {}
data = []
for txt_path in txt_paths:
    with open(txt_path, "r") as f:
        data += f.readlines()
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
            if (auto_result == auto_result_filter or auto_result_filter == None) \
                    and (final_result == final_result_filter or final_result_filter==None) \
                    and "侵权/品牌" in img["ruleHit"]:
                #print(img)
                url = img["textData"]
                final_brand_raw = list(set(img["ruleHit"].split(",")))
                if final_brand_raw==[]:
                    continue
                #print(final_brand_raw)
                final_brand = []
                for brand in final_brand_raw:
                    if "侵权/品牌" in brand:
                        final_brand.append(brand)
                #print(final_brand)
                if final_brand==[]:
                    continue
                print_name = final_brand[0].split("/")[-1].split("】")[0]
                if len(final_brand)>=2:
                    for final in final_brand[1:]:
                        print_name += "_"+final.split("/")[-1]
                final_brand = max(final_brand,key=final_brand.count)
                #final_brand = final_brand.split("/")[-1]
                final_brand = final_brand.split("/")[-1].split("】")[0]
                # print(final_brand)
                # print(need_brand[final_brand])

                if final_brand in donot_need_brand or (donot_need_brand == ["all"] and final_brand not in need_brand):
                    continue
                if final_brand in get_brand and final_brand in need_brand and get_brand[final_brand]>=need_brand[final_brand]:
                    print(f"brand {final_brand} is enough,get {get_brand[final_brand]} images")
                    continue
                elif final_brand in get_brand and final_brand not in need_brand and final_brand not in donot_need_brand and get_brand[final_brand]>=donot_need_num:
                    print(f"brand {final_brand} is enough,get {get_brand[final_brand]} images")
                    continue
                else:
                    if final_brand in get_brand:
                        get_brand[final_brand] += 1
                    else:
                        get_brand[final_brand] = 1

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
    #     find_all=1
    #     if len(get_brand)==len(need_brand):
    #         for k,v in get_brand.items():
    #             if v<need_brand[k]:
    #                 find_all=0
    #     else:
    #         find_all = 0
    #     if find_all==1:
    #         print("final index:",index)
    #         print(f"get images: {get_brand}")
    #         exit()
        print(f"get images: {get_brand}")




