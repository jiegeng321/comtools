#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""

import argparse
from pathlib import Path
import requests
import json
import cv2
import os
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from func.funcxml import readxml
from func.check import check_dir
from multiprocessing import Pool
from pascal_voc_writer import Writer

parser = argparse.ArgumentParser(description='test for logo service')
parser.add_argument("--url", type=str, default='.')
parser.add_argument('--yolo_dir', type=str, default=None)
parser.add_argument('--txt', type=str, default=None)
parser.add_argument('--dst_dir', type=str, default='./', help="")
parser.add_argument('--conf_thresh', type=float, default=0.1)
args = parser.parse_args()

suffix = ['.jpg', '.png', '.jpeg']


def readtxt(txt_file):
    jsonstrs = []
    with open(txt_file, 'r') as fr:
        lines = fr.readlines()
        jsonstrs = [line for line in lines]
    return jsonstrs

def get_label(label_str):
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
    return list(set(first_label)), list(set(second_label)), list(set(third_label))

def autoVSfinal(autolabel, finallabel):
    for a_l in autolabel:
        if a_l in finallabel:
           return True
    return False

# def get_data_fromyolo(yolo_dir):
#     img_dir = yolo_dir / "JPEGImages/eval/images"
#     anno_dir = yolo_dir / "Annotations"
#     imgs = [i for i in img_dir.rglob("*.*") if i.suffix.lower() in suffix]
#     annos = [str(i).replace("JPEGImages/eval/images", 'Annotations').replace(i.suffix, ".xml") for i in imgs]
#     return imgs, annos

def get_data_fromchecked(yolo_dir):
    img_dir = yolo_dir
    imgs = [i for i in img_dir.rglob("*.*") if i.suffix.lower() in suffix]
    print(imgs)
    annos = [str(i).replace(i.suffix, ".xml") for i in imgs]
    return imgs, annos


def get_data_fromtxt(txt_path):
    jsondata = readtxt(txt_path)
    return jsondata


def get_img(url, imgurl, dst_dir, finalthirdlabel, brand_names):
    if len(finalthirdlabel)==0:
        return
    gt_name = None
    for f in finalthirdlabel:
        if f in brand_names:
            gt_name = f
            break
    print(f"gt_name--->{gt_name}")
    file_name = imgurl.split('/')[-1]
    xml_name = file_name.split('.')[0]+'.xml'
    h, w = file_name.split('-')[-1].split('.')[0].split('x')
    resq = requests.get(imgurl)
    imgdata=None
    img_out = os.path.join(dst_dir, gt_name, file_name)
    open(img_out, 'wb').write(resq.content)
    if len(resq.content) > 100:
        imgdata = resq.content
    if imgdata is None:
        return
    open(img_out, 'wb').write(resq.content)
    res = url_res(imgdata, file_name, url)
    writer = Writer(file_name, w, h)
    for item in res:
        class_name = item["logo_name"]
        score = item["score"]
        box = item['box']
        writer.addObject(class_name, int(box['x1']), int(box['y1']), int(box['x2']), int(box['y2']))
    writer.save(os.path.join(dst_dir, gt_name, xml_name))



def url_res(imgdata, file_name, url):
    payload = {'imageId': file_name}
    file_temp = [('img', (file_name, imgdata, 'image/jpeg'))]
    try:
        response = requests.post(url, data=payload, files=file_temp)
        result = response.json()
        return result["res"]
    except:
        return []


def res_filter(res, conf=0.1, brand_filter=[], mode="yolo", extra={}):
    if mode == "yolo":
        anno_path = extra['anno']
        try:
            #print(anno_path)
            labels = readxml(str(anno_path))
            #print(labels)
            gt_names = list(set([i[0].split('-')[0] for i in labels]))
            #print(gt_names)
        except Exception as e:
            print(e)
            gt_names = []
            gt_res = []
    not_find_class = []
    not_find_box = []
    not_find_score = []
    for item in res:
        class_name = item["logo_name"]
        if class_name=="ac/dc":
            class_name="ac dc"
        if class_name=="A-COLD-WALL":
            class_name="A COLD WALL"
        if class_name=="Bell  Ross":
            class_name="Bell Ross"
        if class_name=="dooney  bourke":
            class_name="dooney bourke"
        score = item["score"]
        box = item['box']
        if class_name in brand_filter:
            if mode=="yolo":
                if class_name not in gt_names:
                    not_find_class.append(class_name)
                    not_find_box.append(box)
                    not_find_score.append(score)
                #     return class_name
                # else:
                #     return None
            else:
                return class_name
    return not_find_class,not_find_box,not_find_score


def yolo_data_check(yolo_dir, url, dst_dir="./", brandname=[]):
    imgs, annos = get_data_fromchecked(yolo_dir)
    # for name in brandname:
    #     check_dir(os.path.join(dst_dir, name))
    lenth = len(imgs)
    get_num = 0
    for index, item in enumerate(zip(imgs, annos)):
        img, anno = item
        if "WewData" in str(img):
            continue
        if index%20==0:
            print(f"Processing {index}/{lenth},get {get_num}")
        #pbar.set_description(f"Processing {img.name}")
        file_name = img.name
        suffix = img.suffix
        metadata = open(str(img), 'rb')
        res = url_res(metadata, file_name, url)
        metadata.close()
        if len(res)==0:
            continue
        anno_dict = {"anno":anno}
        not_find_class,not_find_box,not_find_score = res_filter(res, brand_filter=brandname, extra=anno_dict)
        if not_find_class !=[]:
            img_cv = cv2.imread(str(img))
            check_dir(os.path.join(dst_dir, max(not_find_class, key=not_find_class.count)))
            color = [255, 0, 0]
            for comp_name,box,score in zip(not_find_class,not_find_box,not_find_score):
                try:
                    x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']
                    cv2.rectangle(img_cv, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(img_cv, comp_name, (x1, y1 - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                    cv2.putText(img_cv, str(round(score, 3)), (x1, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1,
                                cv2.LINE_AA)
                except Exception as e:
                    print(e)
                    continue
            try:
                cv2.imwrite(os.path.join(dst_dir, max(not_find_class, key=not_find_class.count), file_name), img_cv)
                with open(str(anno), 'rb') as fr:
                    data = fr.read()
                    fw = open(os.path.join(dst_dir, max(not_find_class, key=not_find_class.count), str(file_name.replace(suffix, '.xml'))), 'wb')
                    fw.write(data)
                    fw.close()
            except Exception as e:
                print(e)
                continue
            get_num += 1
            print(f"get one {max(not_find_class, key=not_find_class.count)} +1")


def online_data_check(txt_dir, url, dst_dir="./", brandname=[]):
    for name in brandname:
        check_dir(os.path.join(dst_dir, name))
    jsondata = get_data_fromtxt(txt_dir)
    for jsonstr in tqdm(jsondata):
        data = json.loads(jsonstr)
        if data['autoCheckResult']=="Accept" and data["finalCheckResult"] == "Accept":
            continue
        if data['autoCheckResult'] == "Reject":
            imgdata = data["imageCommodityData"]
            for imginfo in imgdata:
                if imginfo["finalCheckResult"] == "Accept":
                    continue
                if "tagHit" in imginfo:
                    auto_label = imginfo["tagHit"]
                else:
                    auto_label = ""
                person_label = imginfo["finalTagHit"]
                finalfirstlabel, finalsecondlabel, finalthirdlabel = get_label(person_label)
                autofirstlabel, autosecondlabel, autothirdlabel = get_label(auto_label)
                if not autoVSfinal(finalthirdlabel, brand_names):
                    continue
                if not autoVSfinal(autothirdlabel, finalthirdlabel):
                    imgurl = imginfo['textData']
                    get_img(url, imgurl, dst_dir, finalthirdlabel, brand_names)


if __name__=="__main__":
    yolo_dir = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/checked"
    # serverurl = args.url
    # dst_dir = args.dst_dir
    txt_dir = None#"/data01/xu.fx/dataset/LOGO_DATASET/comb_data/checked"
    serverurl = "http://10.58.14.38:55902/v2/logo_brand_rec"
    #serverurl_ = "http://10.58.10.51:5031/v2/logo_brand_rec"
    #serverurl = "http://10.58.14.38:55909/v2/logo_brand_rec"
    dst_dir = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/check_fx_by_fx"
    style = ['3M-1', '3T-1', '5.11 Tactical-2', 'A. Lange Sohne-w-1', 'ac dc-w-1', 'Acer-w-1', 'Addicted-w-1', 'Ado Den Haag-1', 'Agnes B-w-1', 'Always-w-1', 'American Eagle-1', 'American Eagle-w-2', 'Amiri-1', 'Anaheim Angels-1', 'Anaheim Angels-2', 'Anaheim Ducks-1', 'Anaheim Ducks-2', 'Anaheim Ducks-3', 'Anna Sui-w-1', 'Anne Klein-2', 'Anne Klein-w-1', 'AQUABEADS-w-1', 'Aquascutum-2', 'Aquascutum-w-1', 'Arcteryx-1', 'Arcteryx-w-2', 'Ariat-2', 'Ariat-w-1', 'Ariel-2', 'Ariel-w-1', 'Arizona Diamondbacks-1', 'Arizona Diamondbacks-4', 'Arizona Diamondbacks-w-2', 'Audi-2', 'Audio Technica-1', 'Audio Technica-w-2', 'AussieBum-w-1', 'AussieBum-w-2', 'Babolat-1', 'Babolat-w-2', 'Babyliss-1', 'Bally-w-1', 'Barbie-1', 'Barbie-2', 'Barbour-w-1', 'Batman-2', 'Batman-w-1', 'BeautyBlender-2', 'BeautyBlender-w-1', 'Bebe-w-1', 'Bed Head-w-1', 'belkin-2', 'belkin-w-1', 'Bell Ross-w-1', 'Bell Ross-w-2', 'Belstaff-2', 'Belstaff-w-1', 'BEN JERRYS-w-1', 'Bill Blass-2', 'Bill Blass-w-1', 'Billabong-2', 'Billabong-w-1', 'Bioderma-w-1', 'Biotherm-w-1', 'BitDefender-2', 'BitDefender-w-1', 'Bjorn Borg-w-1', 'Bjorn Borg-w-3', 'black panther-w-1', 'black panther-w-2', 'black widow-w-1', 'black widow-w-2', 'Blackberry-2', 'Blackberry-w-1', 'Blackhawk-2', 'Blackhawk-w-1', 'Blancpain-w-1', 'Blaze and the Monster Machines-1', 'Blaze and the Monster Machines-2', 'BMC Racing-1', 'BMW-1', 'Bobbi Brown-2', 'Bobbi Brown-w-1', 'Bobbi Brown-w-3', 'Bontrager-2', 'Bontrager-w-1', 'BOSCH-2', 'BOSCH-w-1', 'Boston Bruins-2', 'Boston Bruins-3', 'BRABUS-w-1', 'Braun-w-1', 'Brazil-1', 'Breeze Smoke-w-1', 'Brioni-1', 'BRUT-w-1', 'Bubble Guppies-1', 'Buffalo Sabres-2', 'Buffalo Sabres-3', 'Buffalo Sabres-w-1', 'Bugatti Veyron-1', 'Bugatti Veyron-2', 'Bugslock-w-1', 'Bulova-2', 'Bulova-w-1', 'bunch o balloons-w-1', 'Cacharel-w-1', 'Calgary Flames-3', 'Cannondale-2', 'Cannondale-w-1', 'Care Bears-1', 'Carmex-w-1', 'Carolina Herrera-2', 'Carolina Herrera-w-1', 'Carolina Hurricanes-2', "Carter's-w-1", 'Casio-w-1', 'Casio-w-2', 'Caterpillar-2', 'Caterpillar-w-1', 'Cath Kidston-1', 'CHAUMET-w-1', 'Cheap Monday-2', 'Cheap Monday-w-1', 'Chevrolet-2', 'Chevrolet-w-1', 'Chevron-1', 'Chevron-w-2', 'Chicago Blackhawks-2', 'Chicago Blackhawks-3', 'Chicago Cubs-1', 'Chicago Cubs-2', 'Chloe-w-1', 'Chopard-w-1', 'Chopard-w-2', 'christian audigier-3', 'Chrome Hearts-2', 'Chrome Hearts-w-1', 'Chrome Hearts-w-3', 'Cisco-2', 'Cisco-w-1', 'Citizen-w-1', 'CLARINS-w-1', 'Clarisonic-w-1', 'Clarisonic-w-2', 'Cleveland golf-2', 'Cleveland golf-w-1', 'Cleveland Indians-1', 'Cleveland Indians-2', 'Clinique-1', 'Clinique-w-2', 'CLUSE-w-1', 'CND-1', 'Coca-Cola-1', 'cole haan-w-1', 'Colgate-w-1', 'Colorado Avalanche-2', 'Colorado Avalanche-3', 'Colorado Avalanche-w-1', 'Comme Des Garcons-2', 'Comme Des Garcons-w-1', 'Compaq-1', 'Compaq-w-2', 'Conair-w-1', 'Concord-2', 'Concord-w-1', 'Converse-1', 'Converse-3', 'Converse-w-2', 'Coogi-w-1', 'Copper Fit-1', 'Corum-2', 'Corum-w-1', 'Coty-2', 'Coty-w-1', 'Crabs Adjust Humidity-1', 'Crabs Adjust Humidity-w-3', 'Creative-1', 'Crocs-2', 'Crocs-w-1', 'Crumpler-1', 'Crumpler-2', 'CWC-1', "D'Addario-w-1", 'Daiwa-1', 'Daiwa-2', 'Dallas Stars-1', 'Dallas Stars-2', 'Daniel Roth-w-1', 'Daniel Roth-w-2', 'Davidoff-2', 'Davidoff-3', 'Davidoff-w-1', 'DC shoes-1', 'DC shoes-w-1', 'Deadpool-w-1', 'Dean Guitar-1', 'Death Wish Coffee Co.-1', 'Def Leppard-1', 'Def Leppard-w-2', 'Dell-1', 'Desigual-w-1', 'Detroit Red Wings-1', 'Dettol-w-1', 'DeWALT-w-1', 'DFB-1', 'DHC-w-1', 'Diadora-2', 'Diadora-3', 'Diesel-w-1', 'DKNY-w-2', 'Doctor Strange-w-1', 'Doctor Strange-w-2', 'dooney bourke-2', 'dooney bourke-w-1', 'Dr. Martens-w-1', 'DRAGON BALL-1', 'DRAGON BALL-w-2', 'DUCATI-1', 'DUCATI-w-2', 'Dumbo-1', 'Dunhill-1', 'Dunhill-w-2', 'Durex-w-1', 'dyson-1', 'Ecco-w-1', 'ECKO-2', 'ECKO-w-1', 'ED Hardy-2', 'ED Hardy-w-1', 'Edmonton Oilers-1', 'ElementCase-2', 'ElementCase-w-1', 'Ellesse-1', 'Ellesse-w-2', 'Elvis Presley-2', 'England-1', 'ENVE-1', 'EOS-w-1', 'Eotech-1', 'Eotech-3', 'Eotech-w-2', 'Epson-w-1', 'Ergobaby-2', 'Ergobaby-w-1', 'Escada-w-1', 'ESP-1', 'ESS-w-1', 'estee lauder-2', 'estee lauder-w-1', 'Everlast-2', 'Everlast-w-1', 'Evisu-1', 'Evisu-w-2', 'Facebook-1', 'Facebook-w-2', 'FC Barcelona(FCB)-1', 'Fear Of God Essentials-w-1', 'Fear Of God Essentials-w-2', 'Fear Of God Essentials-w-3', 'Fender-1', 'Feyenoord-1', 'Fingerlings-1', 'Fischer-1', 'Fischer-w-2', 'Fitbit-2', 'Fitbit-w-1', 'FJALLRAVEN-1', 'FJALLRAVEN-w-2', 'FLEXFIT-2', 'FLEXFIT-w-1', 'Florida Panthers-1', 'Florida Panthers-3', 'Foreo-w-1', 'Forever 21-w-1', 'Fossil-w-1', 'Fox Head-2', 'Franck Muller-2', 'Franck Muller-w-1', 'Franco Moschino-w-1', 'Frida Kahlo-1', 'Fuji film-w-1', 'Furla-w-1', 'FURminator-w-1', 'g_star raw-2', 'g_star raw-w-1', 'Game of Thrones-1', 'Game of Thrones-2', 'Games Workshop-2', 'Gant-w-1', 'GAP-w-1', 'Garmin-w-1', 'gazelle-w-1', 'Ghd-1', 'Gildan-w-1', 'Girard Perregaux-2', 'Girard Perregaux-w-1', 'Giro-2', 'Giro-w-1', 'Glashutte Original-1', 'Glashutte Original-2', 'Goo Jit Zu-1', 'Google-w-1', 'GoPro-w-1', 'Grado-w-1', 'Graham-w-1', 'Grand Seiko-1', 'Grand Seiko-2', 'Grenco Science-2', 'Grenco Science-3', 'Grenco Science-w-1', 'Griffin-3', 'Griffin-w-1', 'Griffin-w-2', 'GRUMPY CAT-w-1', 'Guardians of the Galaxy-w-1', 'Guerlain-w-1', 'Guess-1', 'Guess-w-2', 'Hamilton-w-1', 'Harley Davidson-1', 'Harley Davidson-2', 'Harry Potter-1', 'harry winston-1', 'harry winston-w-2', 'harry winston-w-3', 'harry winston-w-4', 'Hatchimals-1', 'Havaianas-w-1', 'HEAD-2', 'HEAD-w-1', 'helena rubinstein-w-1', 'helena rubinstein-w-2', 'Hello Kitty-2', 'Hello Kitty-w-1', 'Heron Preston-1', 'Heron Preston-2', 'Heron Preston-3', 'Hexbug-w-1', 'Hey Dude-w-1', 'HM-1', 'Hogan-1', 'Honeywell-w-1', 'Houston Astros-1', 'Houston Astros-2', 'HP-1', 'HTC-1', 'HUF-2', 'HUF-w-1', 'Hunter-w-1', 'Hyundai-2', 'Hyundai-w-1', 'Ibanez-w-1', 'ICE Watch-w-1', 'ICE Watch-w-2', 'Iced Earth-1', 'IMREN-2', 'IMREN-w-1', 'Incase-1', 'Incipio-2', 'Incipio-w-1', 'INFUSIUM-w-1', 'INSTANTLY AGELESS-1', 'Iron Maiden-1', 'iron man-w-1', 'Issey Miyake-w-1', 'Jabra-w-1', "Jack Daniel's-w-1", 'Jack Jones-w-1', 'Jack Jones-w-3', 'jack wills-w-1', 'jack wills-w-2', 'JACOB CO-3', 'JACOB CO-w-1', 'Jacquemus-w-1', 'Jeep-w-1', 'John Deere-2', 'John Deere-w-1', 'John Deere-w-3', 'Juicy Couture-1', 'Juicy Couture-2', 'Juicy Couture-4', 'Juventus-2', 'Juventus-3', 'JW Anderson-2', 'JW Anderson-w-1', 'Kansas Royals-1', 'Kansas Royals-2', 'Kansas Royals-3', 'Kaporal-2', 'Kaporal-w-1', 'KEEN-1', "Kiehl's-1", 'Kingston-2', 'Kipling-1', 'KNVB-2', 'KNVB-3', 'KOSS-2', 'KTM-1', 'L.O.L. SURPRISE!-1', 'La Martina-2', 'La Martina-w-1', 'Lamborghini-1', 'Leicester City F.C-1', 'Lesmills-w-1', 'LG-2', 'LG-w-1', 'Lilo Stitch-1', 'Links of London-2', 'Links of London-w-1', 'Loewe-1', 'Loewe-w-2', 'Logitech-3', 'Logitech-4', 'Logitech-w-1', 'Logitech-w-2', 'Longchamp-1', 'Longchamp-2', 'Los Angeles Dodgers-1', 'Los Angeles Dodgers-2', 'Los Angeles Kings-1', 'Los Angeles Kings-2', 'Luke Combs-1', 'Luke Combs-2', 'Lululemon-2', 'Lyle Scott-2', 'Lyle Scott-w-1', 'M.A.C-1', 'Mammut-2', 'Marcelo Burlon-2', 'Marshall-1', 'Marshall-2', 'Marvel-w-1', 'Max factor-w-1', 'Max factor-w-2', 'MBT-1', 'MCM-1', 'MCM-w-2', 'Metallica-1', 'MIFFY-1', 'MIFFY-2', 'Milwaukee Brewers-1', 'Milwaukee Brewers-2', 'Milwaukee Brewers-3', 'Milwaukee Brewers-4', 'Minesota Twins-1', 'Minesota Twins-2', 'Minesota Twins-3', 'Minnesota wild-1', 'Minnesota wild-2', 'miu miu-1', 'Mizuno-1', 'Mizuno-2', 'MLB-1', 'MLB-2', 'MMS-1', 'Monster Energy-1', 'Monster Energy-2', 'Montreal Canadiens-1', 'Montreal Expos-1', 'Montreal Expos-2', 'Montreal Expos-3', 'moose knuckles-1', 'moose knuckles-2', 'Mophie-2', 'MOTORHEAD-1', 'Motorola-2', 'Movado-1', 'Muhammad Ali-w-1', 'Mulberry-2', 'Nashville Predators-1', 'New Jersey Devils-1', 'New York Islanders-1', 'New York Islanders-2', 'New York Mets-1', 'New York Mets-2', 'New York Rangers-2', 'New York Rangers-3', 'New York Yankees-1', 'New York Yankees-2', 'New York Yankees-3', 'Nirvana-2', 'Nirvana-3', 'Nokia-w-1', 'Nutribullet-w-1', 'Nutribullet-w-2', 'Oakland Athletics-1', 'Oakland Athletics-2', 'Olympique de Marseille-2', 'Olympus-w-1', 'OPI-w-1', 'Ottawa Senators-1', 'Ottawa Senators-2', 'Otter box-2', 'Otter box-w-1', 'Otter box-w-3', 'OXO-2', 'Ozark-2', 'Ozark-w-1', 'Paco Rabanne-2', 'Paco Rabanne-w-1', 'Pandora-1', 'Pandora-2', 'Pandora-w-3', 'PANERAI-1', 'PANERAI-2', 'Paris Saint Germain-1', 'Patagonia-2', 'Paul frank-2', 'Paul Shark-1', 'Paul Shark-2', 'Paul Smith-1', 'Paul Smith-2', 'Pearl Izumi-2', 'Pearl Izumi-w-1', 'Philadelphia Phillies-2', 'Philadelphia Phillies-3', 'Philadelphia Phillies-w-1', 'Philipp Plein-1', 'Philipp Plein-2', 'Philipp Plein-4', 'Phoenix Coyotes-1', 'Phoenix Coyotes-4', 'Piaget-w-1', 'Pinarello-2', 'Pinarello-w-1', 'PING-w-1', 'PINK FLOYD-2', 'PINK FLOYD-3', 'Pittsburgh Penguins-1', 'Pixar-1', 'Pixar-2', 'PJ MASKS-1', 'Plantronics-2', 'Plantronics-w-1', 'Playboy-2', 'Playstation-2', 'Playstation-w-1', 'POCOYO-w-1', 'Pony-2', 'Pony-3', 'PopSockets-1', 'PopSockets-3', 'Portugal-1', 'Power Rangers-2', 'Power Rangers-4', 'Premier League-3', 'Premier League-w-1', 'Premier League-w-2', 'Prince-2', 'Prince-w-1', 'Pro Kennex-2', 'Pro Kennex-w-1', 'PSV Eindhoven-1', 'PSV Eindhoven-w-2', 'Pxg-1', 'RAW-1', 'RB Leipzig-2', 'RCMA-w-1', 'Reebok-2', 'Reebok-3', 'Reebok-w-1', 'Rip Curl-2', 'Rip Curl-4', 'Ritchey-2', 'Ritchey-3', 'Ritchey-w-1', 'ROBO FISH-w-1', 'Roger Vivier-1', 'Roger Vivier-2', 'rosetta stone-1', 'Roxy-1', 'S.H.I.E.L.D.-1', 'S.H.I.E.L.D.-3', 'Salomon-2', 'Salomon-w-1', 'Samantha Thavasa-2', 'Samantha Thavasa-w-3', 'Samsonite-1', 'Samsonite-3', 'San Jose Sharks-1', 'Sanrio-1', 'scooby doo-1', 'scooby doo-w-2', 'Seagate-1', 'Seagate-2', 'Shaun the sheep-w-3', 'Shaun the sheep-w-4', 'Shiseido-1', 'Shure-w-1', 'Skoda-2', 'SLAP CHOP-w-1', 'Slazenger-2', 'Slazenger-w-1', 'Smith Wesson-2', 'Smith Wesson-w-1', 'SONS OF ARTHRITIS-w-1', 'Sony Ericsson-1', 'Sony Ericsson-w-2', 'Speck-2', 'Speck-3', 'Speck-w-1', 'Srixon-1', 'Srixon-2', 'St. Louis Cardinals-1', 'St. Louis Cardinals-2', 'St. Louis Cardinals-4', 'St. Louis Cardinals-w-3', 'stan smith-w-1', 'Stefano Ricci-1', 'Stefano Ricci-3', 'Streamlight-1', 'Streamlight-2', 'Supra-2', 'Supra-w-1', 'Swatch-w-1', 'Swig-2', 'SwitchEasy-1', 'SwitchEasy-w-2', 'Tampa Bay Lightning-1', 'Tampa Bay Lightning-w-2', 'Tampa Bay Rays-2', 'Tampa Bay Rays-w-1', 'Tapout-1', 'TECHNOMARINE-1', 'TECHNOMARINE-w-1', 'THE ALLMAN BROTHERS BAND-2', 'THE ALLMAN BROTHERS BAND-3', 'The Black Crowes-2', 'The Black Crowes-w-1', 'The Horus Heresy-w-1', 'the punisher-1', 'the punisher-2', 'Thomas Sabo-w-1', 'Thomas Sabo-w-2', 'Timberland-2', 'Timberland-w-1', 'Titleist-1', 'Titoni-3', 'Titoni-w-2', 'Toms-w-1', 'Tonino Lamborghini-1', 'Tonino Lamborghini-2', 'Too Faced-w-1', 'Toronto Maple Leafs-1', 'Toronto Maple Leafs-2', 'tory burch-1', 'tory burch-w-2', 'tous-1', 'tous-2', 'tous-3', 'Toy Watch-1', 'Travis Scott-2', 'True Religion-2', 'True Religion-w-1', 'TRXTraining-w-1', 'Tudor-1', 'Tudor-w-2', 'U_boat-w-1', 'UAG-1', 'UEFA-2', 'UEFA-3', 'UEFA-w-1', 'Umbro-2', 'Umbro-w-1', 'USA soccer-1', 'USA soccer-2', 'VACHERON CONSTANTIN-1', 'VACHERON CONSTANTIN-w-2', 'Valentino Garavani-1', 'Valentino Garavani-2', 'Valentino Garavani-3', 'Victorias secret-2', 'Victorias secret-w-1', 'Visa-w-1', 'VLONE-2', 'VLONE-w-1', 'VOLBEAT-3', 'VOLBEAT-w-1', 'Volcom-2', 'Volcom-w-1', 'Volkl-2', 'Volkl-w-1', 'West Ham United-1', 'West Ham United-2', 'Whirlpool-w-1', 'Wilson-2', 'Wilson-w-1', 'Wrangler-w-1', 'WWE-2', 'Xmen-2', 'Xmen-w-1', 'Xxio-1', 'Yonex-1', 'Yonex-2', 'Zara-2', 'Zara-w-1', 'Zegna-1', 'Zegna-2', 'Zenith-w-1', 'Zimmermann-w-1', 'Zumba Fitness-2', 'Zumba Fitness-w-1', 'Pokemon-1', 'Audi-w-1', 'BMW-2', 'BMW-w-3', 'Lamborghini-2', 'MCM-h-1', 'Reebok-h-4']
    style2 = ['dior-w-1', 'golden goose-1', 'coach-w-1', 'fendi-1', 'balenciaga-w-1', 'prada-w-1', 'ck-2', 'ysl-w-1', 'ysl-1', 'lv-2', 'lv-1', 'versace-w-1', 'versace-1', 'fendi-w-1', 'dolce-1', 'Givenchy-w-1', 'the north face-1', 'dior-w-2', 'golden goose-2', 'chanel-2', 'chanel-1', 'dolce-w-3', 'dolce-w-2', 'nike-1', 'nike-w-1', 'off-white-w-1', 'burberry-w-1', 'supreme-1', 'gucci-3', 'dsquared2-w-1', 'burberry-1', 'gucci-2', 'ck-1', 'armani-1', 'Michael Kors-1', 'burberry-2', 'Kenzo-1', 'Givenchy-1', 'Hermes-w-1', 'fendi-2', 'Hermes-2', 'Hermes-1', 'Michael Kors-w-1', 'nike-6', 'dior-1', 'Moncler-1', 'Moncler-2', 'off-white-1', 'balenciaga-1', 'Moncler-w-1', 'supreme-2', 'armani-w-1', 'armani-w-2', 'dior-2', 'gucci-1', 'dolce-3', 'nike-2', 'palace-w-1', 'palace-1', 'Hublot-2', 'Hublot-w-1', 'canada goose-1', 'tommy Hilfiger-6', 'tag heuer-1', 'alexander mcqueen-w-2', 'alexander mcqueen-w-1', 'Abercrombie Fitch-w-3', 'Iwc-w-1', 'marc Jacobs-1', 'balmain-w-1', 'ralph lauren-1', 'tommy Hilfiger-w-1', 'audemars piguet-w-1', 'Jaeger-LeCoultre-w-1', 'salvatore Ferragamo-1', 'Van Cleef Arpels-w-1', 'Van Cleef Arpels-2', 'Cartier-1', 'Cartier-w-1', 'Montblanc-2', 'New Era-1', 'New Era-w-2', 'NEW BALANCE-1', 'lacoste-w-1', 'lacoste-1', 'palm angels-1', 'Under Armour-1', 'Abercrombie Fitch-2', 'Abercrombie Fitch-w-2', 'NEW BALANCE-w-1', 'Rolex-1', 'Rolex-w-1', 'ralph lauren-w-1', 'Abercrombie Fitch-1', 'Omega-1', 'Omega-w-1', 'NEW BALANCE-2', 'CHRISTIAN LOUBOUTIN-1', 'Bvlgari-w-1', 'audemars piguet-2', 'hugo boss-w-1', 'hugo boss-w-2', 'tag heuer-w-1', 'Adidas-2', 'Adidas-w-1', 'Abercrombie Fitch-w-1', 'Iwc-w-2', 'bape-1', 'New Era-2', 'Adidas-1', 'New Era-w-1', 'marc Jacobs-w-1', 'Montblanc-w-1', 'salvatore Ferragamo-2', 'salvatore Ferragamo-4', 'tommy Hilfiger-w-2', 'canada goose-w-1', 'salvatore Ferragamo-3', 'balmain-1', 'palm angels-2', 'bape-w-1', 'bape-w-2', 'Under Armour-w-1', 'Cartier-w-2', 'alexander mcqueen-1', 'rayban-1', 'FILA-1', 'New Orleans Pelicans-w-2', 'Washington Redskins-1', 'Washington Redskins-w-1', 'Houston Rockets-1', 'Houston Rockets-w-2', 'Houston Rockets-w-3', 'FIFA-w-1', 'Boston Celtics-w-1', 'Pittsburgh Steelers-1', 'Pittsburgh Steelers-w-1', 'Dallas Cowboys-w-1', 'Toronto Raptors-w-1', 'Toronto Raptors-2', 'New Orleans Pelicans-1', 'New Orleans Pelicans-3', 'Brooklyn Nets-w-2', 'Boston Celtics-3', 'Boston Celtics-w-2', 'Los Angeles lakers-w-1', 'Denver Nuggets-w-2', 'Sacramento Kings-1', 'Indiana Pacers-w-2', 'Brooklyn Nets-1', 'Portland Trail Blazers-1', 'nba-w-1', 'nba-1', 'Buffalo Bills-1', 'Buffalo Bills-w-1', 'Sacramento Kings-w-1', 'Indiana Pacers-2', 'Hollister Co-1', 'Tampa Bay Buccaneers-w-1', 'Phoenix Suns-w-3', 'Phoenix Suns-w-2', 'Phoenix Suns-2', 'Houston Texans-1', 'Utah Jazz-1', 'Utah Jazz-w-1', 'david yurman-1', 'david yurman-w-1', 'Miami Heat-w-1', 'Miami Heat-w-2', 'kate spade-w-1', 'Carolina Panthers-1', 'kate spade-1', 'Milwaukee Bucks-1', 'Milwaukee Bucks-w-1', 'Detroit Lions-3', 'Utah Jazz-4', 'Sacramento Kings-3', 'Oklahoma City Thunder-1', 'Oklahoma City Thunder-w-3', 'Jacksonville Jaguars-1', 'Jacksonville Jaguars-w-1', 'San Antonio Spurs-2', 'New Orleans Pelicans-w-1', 'Orlando Magic-2', 'New York Knicks-2', 'Adobe-1', 'Adobe-w-1', 'Philadelphia Eagles-1', 'Memphis Grizzlies-w-1', 'Washington Wizards-w-1', 'Tennessee Titans-w-1', 'HID Global-1', 'CALL OF DUTY GHOSTS-w-2', 'Denver Broncos-w-1', 'Los Angeles Chargers-w-1', 'Chicago Bulls-1', 'Minnesota Timberwolves-w-1', 'Minnesota Timberwolves-w-2', 'Dallas Mavericks-w-1', 'Dallas Mavericks-1', 'Green Bay Packers-w-1', 'Dallas Mavericks-w-3', 'A COLD WALL-w-1', 'Indianapolis Colts-1', 'Indianapolis Colts-w-1', 'Atlanta Hawks-1', 'Detroit Lions-1', 'Oklahoma City Thunder-w-2', 'Cleveland Browns-1', 'FILA-2', 'Baltimore Ravens-w-1', 'Cleveland Browns-w-1', 'San Antonio Spurs-1', 'Miami Dolphins-w-1', 'Los Angeles Chargers-1', 'Portland Trail Blazers-w-1', 'Philadelphia 76ers-1', 'Chicago Bears-w-1', 'Orlando Magic-w-1', 'Portland Trail Blazers-w-2', 'Chicago Bears-1', 'Memphis Grizzlies-w-2', 'Hollister Co-w-1', 'New York Knicks-1', 'Washington Wizards-2', 'Tennessee Titans-1', 'Houston Texans-w-1', 'Guitar Hero-1', 'New York Giants-1', 'Washington Wizards-3', 'Alcon-w-1', 'Los Angeles lakers-3', 'Denver Nuggets-1', 'Denver Nuggets-2', 'Toronto Raptors-3', 'Brooklyn Nets-2', 'Denver Nuggets-w-1', 'Oakland Raiders-1', 'Oakland Raiders-w-1', 'San Francisco 49ers-1', 'San Francisco 49ers-2', 'Utah Jazz-2', 'Philadelphia 76ers-3', 'Kansas City Chiefs-1', 'Kansas City Chiefs-w-1', 'Miami Heat-1', 'Cleveland Cavaliers-w-1', 'Philadelphia 76ers-2', 'Chicago Bulls-w-1', 'Philadelphia Eagles-w-1', 'Golden State Warriors-1', 'New England Patriots-w-1', 'Chicago Bulls-w-2', 'Memphis Grizzlies-2', 'Memphis Grizzlies-1', 'Golden State Warriors-w-1', 'New England Patriots-1', 'Carolina Panthers-w-1', 'Indiana Pacers-1', 'Dallas Cowboys-w-2', 'Minnesota Vikings-1', 'Atlanta Falcons-1', 'Minnesota Vikings-w-1', 'Boston Celtics-1', 'nfl-w-1', 'nfl-2', 'Los Angeles Clippers-1', 'Miami Dolphins-1', 'Washington Wizards-1', 'Indiana Pacers-w-1', 'Baltimore Ravens-1', 'Sacramento Kings-2', 'Los Angeles lakers-2', 'New York Jets-w-1', 'Cleveland Cavaliers-1', 'Atlanta Hawks-w-1', 'Detroit Pistons-w-1', 'A COLD WALL-w-2', 'Orlando Magic-w-2', 'New Orleans Saints-1', 'Oklahoma City Thunder-w-1', 'Denver Broncos-1', 'Cleveland Cavaliers-3', 'Arizona Cardinals-1', 'Arizona Cardinals-w-1', 'Sacramento Kings-4', 'Minnesota Timberwolves-1', 'New York Giants-w-1', 'Los Angeles Clippers-w-1', 'Minnesota Timberwolves-2', 'blu电子烟-1', 'Philadelphia Eagles-w-2', 'Atlanta Hawks-2', 'Toronto Raptors-1', 'Chicago Bulls-w-3', 'Detroit Pistons-1', 'Orlando Magic-1', 'Cleveland Cavaliers-w-2', 'Miami Heat-2', 'Toronto Raptors-w-2', 'Denver Nuggets-4', 'Denver Nuggets-5', 'Los Angeles Rams-2', 'Los Angeles Rams-1', 'Seattle Seahawks-w-1', 'Phoenix Suns-1', 'Dallas Cowboys-w-3', 'Tampa Bay Buccaneers-1', 'Seattle Seahawks-1', 'Phoenix Suns-w-1', 'Houston Rockets-2', 'FIFA-1', 'Detroit Lions-w-1', 'Charlotte Hornets-2', 'Charlotte Hornets-w-1', 'Dallas Mavericks-2', 'Buffalo Bills-w-2', 'Cleveland Cavaliers-2', 'Atlanta Falcons-w-1', 'Charlotte Hornets-w-2', 'Alcon-w-2', 'Charlotte Hornets-1', 'Cincinnati Bengals-2', 'Cincinnati Bengals-w-1', 'Cincinnati Bengals-1', 'Breguet-2', 'Red Bull-1', 'USA Basketball-1', 'Nike-just do it', 'Fred Perry-2', 'Overwatch-2', 'Fred Perry-1', 'tiffany co-1', 'Marlboro-1', 'Ugg-1', 'World of Warcraft-1', 'World of Warcraft-4', 'World of Warcraft-3', 'Disney-2', 'Liverpool FC-2', 'Pantene-2', 'Pantene-1', 'Gibson-1', 'kobe-2', 'Pampers-1', 'Honda-1', 'Breguet-1', 'Red Bull-2', 'Oakley-1', 'Benefit-1', 'Honda-2', 'Benefit-3', 'Butterfly-2', 'Gillette-w-1', 'Gillette-w-2', 'Butterfly-1', 'breitling-1', 'breitling-2', 'Liverpool FC-1', 'Lancome-1', 'Liverpool FC-w-1', 'Daniel wellington-2', 'Daniel wellington-1', 'Longines-1', "Blue's Clues-1", 'Jack wolfskin-1', 'Spyderco-1', 'Spyderco-2', 'Sisley-1', 'game boy-1', 'Starcraft-w-1', "Levi's-w-1", 'Manchester United-1', 'Sisley-2', 'Specialized-w-1', 'Specialized-1', 'Manchester City-1', 'Giuseppe Zanotti-1', 'YETI-1', 'CAZAL-1', 'Tide-1', 'Lancome-2', 'roor-1', 'Columbia-1', 'Columbia-2', 'The Rolling Stones-1', 'The Rolling Stones-w-1', 'Zelda-w-1', 'switch-2', 'switch-1', 'Beats by Dr.Dre-1', 'Overwatch-1', 'Bottega Veneta-1', 'YETI-2', 'Superdry-w-3', 'Superdry-w-2', 'Arsenal-1', 'JBL-1', 'Maui Jim-1', "Levi's-1", 'Nickelodeon-1', 'Shimmer And Shine-1', 'HearthStone-3', 'HearthStone-1', 'Asics-2', 'Lego-1', 'Celine-2', 'SK-II-1', 'Ulysse Nardin-w-1', 'Oral-B-1', 'Duracell-w-2', 'Heroes of the Storm-1', 'Honda-3', 'Heroes of the Storm-3', 'R4-1', 'LINDBERG-1', 'Tottenham Hotspur-2', 'Chelsea-1', 'Chelsea-2', 'Bose-1', 'Elizabeth Arden-1', 'Beats by Dr.Dre-w-2', 'Beats by Dr.Dre-w-1', 'breitling-3', 'Zelda-3', 'Duracell-w-1', 'Diablo-1', 'Overwatch-w-1', 'L’Oreal-1', 'Ferrari-2', 'Ferrari-1', 'Tottenham Hotspur-1', 'puma-2', 'Amiibo-1', 'JUUL-1', 'Honda-5', 'Herbal Essences-w-3', 'Herbal Essences-1', 'Herbal Essences-w-1', 'World of Warcraft-w-1', 'Martin Co-1', 'Wallykazam-1', 'DESTINY-w-1', 'DESTINY-1', 'Asics-1', 'Headshoulders-1', 'Headshoulders-w-1', 'Headshoulders-w-2', 'Birkenstock-1', 'Kenan and Kel-1', 'Celine-1', 'alexander wang-w-1', 'Cummins-1', 'Asics-3', 'Honda-4', 'The Fairly Oddparents-1', 'Zelda-2', 'Amiibo-2', 'SKYLANDERS-1', 'Starcraft-2', 'goyard-1', 'Superdry-w-1', 'Apple-1', 'Benefit-2', 'fullips-2', 'kobe-1', 'Starcraft-1', 'Chi-1', 'fullips-1', 'Blizzard-1', 'World of Warcraft-2', 'Ferrari-3', 'Rimowa-1', 'The Killers-1', 'goyard-2', 'USA Basketball-2', 'The Loud House-1', 'Starcraft-3', 'iRobot-1', 'Herbal Essences-2', 'Manchester City-2', 'Sisley-3', 'puma-1', 'Disney-1', 'HearthStone-2', 'Apple-w-3', 'hydro flask-1', 'hydro flask-w-1', 'Gibson-2', '7up-2', '7up-1', 'Efest-2', 'Efest-1', 'Tissot-1', 'Stussy-2', 'Stussy-1', 'Blackberry Smoke-1', 'Tods-1', 'Tods-2', 'swarovski-1', 'swarovski-2', 'Skullcandy-1', 'Skullcandy-2', 'Jimmy Choo-1', 'Taylormade-2', 'Taylormade-1', 'Jurlique-1', 'Maybelline-1', 'Vans-1', 'Vans-2', 'Baby Shark-2', 'Scotty Cameron-2', 'Scotty Cameron-3', 'Scotty Cameron-1', 'Scotty Cameron-4', 'Shimano-1', 'manolo blahnik-1', 'vivienne westwood-1', 'vivienne westwood-2', 'Monchhichi-1', 'Sennheiser-2', 'Baby Shark-1', 'Vans-3', 'Shimano-2', 'Maybelline-2', 'Jimmy Choo-2', 'Bright Bugz-2', 'Sennheiser-1', 'Alberta Ferretti-w-1', 'Bright Bugz-1', 'footjoy-2', 'footjoy-w-1', 'BENQ-w-1', 'AWT-1', 'BVB-1', 'AFC Ajax-2', 'AFC Ajax-w-1', 'Asos-w-1', 'Patek Philippe-1', 'Big Green Egg-w-2', 'Big Green Egg-w-1', 'CAMELBAK-w-1', 'Azzaro-w-1', 'Patek Philippe-2', 'AKG by Harmon-2', 'AKG by Harmon-w-1', 'Bestway-w-1', 'Allsaints-w-1', 'Bakugan-1', 'Beretta-2', 'Beretta-w-1', 'Cadillac-2', 'Led Zeppelin-w-2', 'Alpinestars-w-1', 'Alpinestars-2', 'Carhartt-w-1', 'Bentley-w-1', 'Bentley-2', 'Carhartt-2', 'Callaway-w-1', 'Callaway-2', 'Bushnell-w-1', 'Berluti-w-1', 'Cadillac-w-1', 'Led Zeppelin-1', 'Azzaro-2', 'c1rca-w-2', 'Cards Against Humanity-w-1', 'Avengers-w-1', 'Burts Bees-w-1', 'Canon-1', 'captain america-w-2', 'AS Roma-1', 'Benetton-w-1', 'Benetton-2', 'Atletico de Madrid-1', 'Led Zeppelin-w-3', 'Alfar Romeo-1', 'c1rca-1', 'captain america-w-3', 'Aspinal of London-w-2', 'captain america-w-1', 'Betty Boop-w-2', 'Aspinal of London-w-1', 'Betty Boop-w-1', 'Audioquest-w-1', 'Bunchems-1', 'Betty Boop-w-3', 'Alpinestars-w-3', 'AS Roma-w-2', 'Hennessy-w-1', 'Porsche-2', 'puma-w-1', 'Bang Olufsen-2', 'Bang Olufsen-w-1', 'Nike-1', 'St Dupont-w-2', 'Merrell-w-1', 'ZigZag-1', 'Nixon-2', 'Urban Decay-3', 'Urban Decay-w-1', 'Urban Decay-w-2', 'captain america-3', 'Phiten-2', 'Texas Rangers-3', 'Texas Rangers-2', 'Texas Rangers-1', 'San Diego Padres-w-1', 'San Diego Padres-2', 'San Francisco Giants-w-1', 'San Francisco Giants-2', 'San Francisco Giants-3', 'San Francisco Giants-w-4', 'Toronto Blue Jays-1', 'Chicago White Sox-1', 'Chicago White Sox-3', 'Chicago White Sox-2', 'Cincinnati Reds-2', 'Cincinnati Reds-1', 'Detroit Tigers-1', 'Boston Red Sox-2', 'Boston Red Sox-4', 'Boston Red Sox-1', 'Boston Red Sox-3', 'Atlanta Bravs-1', 'Atlanta Bravs-3', 'Atlanta Bravs-4', 'Atlanta Bravs-2', 'Baltimore Orioles-4', 'Baltimore Orioles-5', 'Baltimore Orioles-2', 'Baltimore Orioles-3', 'Pinko-1', 'Florida Marlins-2', 'Florida Marlins-6', 'Florida Marlins-4', 'Florida Marlins-3', 'Florida Marlins-1', 'Florida Marlins-5', 'western digital-w-1', 'western digital-2', 'Hennessy-2', 'Mercedes Benz-2', 'Mercedes Benz-w-1', 'Merrell-2', 'Zippo-w-1', 'Zippo-2', 'Sephora-w-2', 'Sephora-1', 'Shu Uemura-w-1', 'Schwarzkopf-w-2', 'Skin79-2', 'Philadelphia Flyers-1', 'St. Louis Blues-1', 'Jim Beam-w-1', 'Vegas Golden Knights-1', 'Washington Capitals-2', 'Vancouver Canucks-2', 'Vancouver Canucks-w-3', 'Vancouver Canucks-1', 'Hurley-2', 'Hurley-w-1', 'Winnipeg Jets-1', 'Winnipeg Jets-2', 'Washington Capitals-1', 'Maserati-2', 'Maserati-3', 'Hurley-6', 'Magpul-2', 'RADO-2', 'Roger Dubuis-2', 'Roger Dubuis-w-1', 'Romain Jerome-1', 'Kappa-2', 'Baby phat-w-1', 'Baby phat-2', 'Toppik-w-1', 'Land Rover-w-1', 'Land Rover-2', 'LED LENSER-2', 'Robo Alive-w-1', 'Tech Deck-w-1', 'SHOPKINS-w-1', 'Porsche-w-1', 'Columbus Blue Jackets-3', 'Columbus Blue Jackets-2', 'FC bayern munchen-1', 'HAMANN-w-2', 'HAMANN-1', 'Nasa-1']

    brand_names = []
    for i in style:
        brand_names.append(i.split("-")[0])
    brand_names = list(set(brand_names))

    # brand_names = ["CHAUMET", "Casio", "Playboy", "tory burch", "Jeep", "Fossil", "Chloe", "Citizen", "Guess", "Converse", "MCM", "Grand Seiko",
    #                "Loewe", "miu miu", "Zara", "Lamborghini", "BMW"]
    print(len(brand_names),brand_names)
    if yolo_dir is not None:
        yolo_data_check(Path(yolo_dir), serverurl, dst_dir= dst_dir, brandname=brand_names)
    if txt_dir is not None:
        online_data_check(Path(txt_dir), serverurl, dst_dir=dst_dir, brandname=brand_names)







