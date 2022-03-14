#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import random
from tqdm import tqdm
import hashlib
from pathlib import Path
from PIL import Image
import shutil
import xml.etree.ElementTree as ET
from func.path import ospathjoin
from func.check import check_dir
from multiprocessing import Pool, Manager
import cv2
import os
import numpy as np
import pandas as pd
from func.print_color import bcolors
import warnings
# warnings.filterwarnings("error", category=UserWarning)
# Image.warnings.simplefilter('error', Image.DecompressionBombWarning)
from func.tools import is_img
#main_data_dir为数据总目录，建议该目录下包含名为checked的目录然后该目录下为xml与图片混合的数据，之后全自动生成yolo数据集和相关数据集统计信息

be_merged_dir = None#"dataset/LOGO_DATASET/D14"
white_sample_dir_list = {}
white_base = "/data01/xu.fx/dataset/PATTERN_DATASET/white_data/pattern_white_total_2nd"
white_sample_dir_list["/data01/xu.fx/dataset/PATTERN_DATASET/white_data/pattern_white_total"] = 5000
white_sample_dir_list[white_base+"/adidas"] = 0
white_sample_dir_list[white_base+"/burberry"] = 1000
white_sample_dir_list[white_base+"/celine"] = 150
white_sample_dir_list[white_base+"/christian_dior"] = 200
white_sample_dir_list[white_base+"/coach"] = 0
white_sample_dir_list[white_base+"/fendi"] = 0
white_sample_dir_list[white_base+"/goyard"] = 200
white_sample_dir_list[white_base+"/issey_miyake"] = 200
white_sample_dir_list[white_base+"/lv"] = 0
white_sample_dir_list[white_base+"/michael_kors"] = 0
white_sample_dir_list[white_base+"/nike"] = 0
white_sample_dir_list[white_base+"/versace"] = 100
white_sample_dir_list[white_base+"/gucci"] = 100

show_data_info = False
use_effective_brand = False
use_class_brand = True

random_seed = 1
train_val_test_ratio = [1.0, 0.0, 0.0]
MAX_NUM_PER_BRAND = None
MAX_OBJ_NUM_PER_BRAND = 10000
#WHITE_SAMPLE_COUNT = 0
detect_num = 2
export_data_info_csv = True
WORKERS = 30

main_data_dir = "dataset/PATTERN_DATASET/comb_data"
yolo_dataset_name = "yolodataset_pattern_15bs_22ks_0301"

######################################################## FX #########################################
CLASS_list_fx = ['gucci-h-1', 'michaelkors-h-1', 'coach-h-1', 'adidas-h-1', 'gucci-4', 'gucci-5', 'lv-h-1', 'fendi-h-1', 'lv-h-2', 'nike-4', 'lv-h-3', 'gucci-h-2',"lv-h-4"]
D7 = ['versace-h-1','christian dior-h-1','goyard-h-1','burberry-h-1','Issey miyake-h-1','christian dior-h-2',"celine-h-1"]
D8 = ['MCM-h-1','Reebok-h-4']
CLASS_list_fx += D7 + D8
brand_names_fx = []
for c in CLASS_list_fx:
    brand = c.split("-")[0]
    if brand not in brand_names_fx:
        brand_names_fx.append(brand)
######################################################## FX #########################################
brand_names = brand_names_fx
CLASS_list = CLASS_list_fx

print(CLASS_list)
print(len(CLASS_list))
#CLASS_list = None
# brand_names_exist = brand_names1+brand_names2+brand_names3+brand_names4+brand_names5+brand_names6+brand_names7+brand_names8
# for i in brand_names:
#     if i.replace(" ","").lower() in [j.replace(" ","").lower() for j in brand_names_exist]:
#         print("%s is exist"%i)
#split img data
# export_dataset_flag = True

WORKERS_get_class = WORKERS
WORKERS_xml = WORKERS
WORKERS_spilt = WORKERS
WORKERS_gif_mv = WORKERS
WORKERS_md5_mv = WORKERS
WORKERS_not_pair_mv = WORKERS
WORKERS_empty_mv = WORKERS
if be_merged_dir:
    be_merged_dir = "/data01/xu.fx/" + be_merged_dir + "/checked"
src_dir = "/data01/xu.fx/"+main_data_dir+"/checked"
yolo_dataset_dir = "/data01/xu.fx/"+main_data_dir+"/"+yolo_dataset_name+"/"
detect_img_dir = "/data01/xu.fx/"+main_data_dir+"/"+yolo_dataset_name+"/test_detect_img"

empty_dir = src_dir + "_empty"
same_dir = src_dir + "_same_md5"
gif_dir = src_dir + "_gif"
error_dir = src_dir + "_error"
not_pair_dir = src_dir + "_not_pair"
wrong_xml_dir = src_dir + "_wrong_xml"
warning_dir = src_dir + "_warning"
effective_brandname = Manager().list(brand_names)

def merge_data(src_dir,dst_dir):
    print("before merged data info:")
    print("merge to dir file num:", int(len(os.listdir(dst_dir))/2))
    print("be merged dir file num:", int(len(os.listdir(src_dir))/2))
    for file in tqdm(os.listdir(src_dir)):
        shutil.copy(os.path.join(src_dir,file),dst_dir)
    print("\nafter merged data info:")
    print("merge to dir file num:", int(len(os.listdir(dst_dir)) / 2))
    print("be merged dir file num:", int(len(os.listdir(src_dir)) / 2))

def not_pair_mv_func(files):
    check_pair = dict()
    not_pair_num = 0
    xml_num = 0
    for file in tqdm(files):
        if file.split('.')[-1]=='xml':
            xml_num+=1
        file_ = ''
        for i in file.split('.')[:-1]:
            file_ += i
        if file_ not in check_pair:
            check_pair[file_] = 1
        else:
            check_pair[file_] += 1
    total_num = len(files)
    print('total num: ',total_num)
    print('xml num: ',xml_num)
    if xml_num!=int(total_num/2):
        print('xml and pic is not pair')
    else:
        print('xml and pic is pair')
    for key,value in tqdm(check_pair.items()):
        if value>=3:
            not_pair_num += 1
            for file_i in files:
                file_ = ''
                for i in file_i.split('.')[:-1]:
                    file_ += i
                if file_ == key:
                    if not os.path.exists(not_pair_dir):
                        os.mkdir(not_pair_dir)
                    shutil.move(ospathjoin([src_dir, file_i]), not_pair_dir)
                    print("%s is not pair" % file_i)
    print('not_pair_num: ',not_pair_num)
def not_pair_mv(src_dir):
    files = os.listdir(src_dir)
    pool = Pool(processes=WORKERS_not_pair_mv)
    for i in range(0, WORKERS_not_pair_mv):
        files_ = files[i:len(files):WORKERS_not_pair_mv]
        pool.apply_async(not_pair_mv_func, (files_,))
    pool.close()
    pool.join()
def empty_mv_func(files):
    empty_num = 0
    for file_i in tqdm(files):
        if file_i.split('.')[-1] in ['jpg','png','jpeg','JPG','PNG','JPEG']:
            xml_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'xml'])
            if not os.path.exists(xml_str):
                print(xml_str)
                if not os.path.exists(empty_dir):
                    os.mkdir(empty_dir)
                shutil.move(ospathjoin([src_dir, file_i]), empty_dir)
                print("%s is empty"%file_i)
                empty_num+=1

        if file_i.endswith('.xml'):
            jpg_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'jpg'])
            png_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'png'])
            jpeg_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'jpeg'])
            JPG_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'JPG'])
            PNG_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'PNG'])
            JPEG_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'JPEG'])
            if not os.path.exists(jpg_str) and not os.path.exists(png_str) and not os.path.exists(jpeg_str) and\
                    not os.path.exists(JPG_str) and not os.path.exists(PNG_str) and not os.path.exists(JPEG_str):
                if not os.path.exists(empty_dir):
                    os.mkdir(empty_dir)
                shutil.move(ospathjoin([src_dir, file_i]), empty_dir)
                print("%s is empty"%file_i)
                empty_num+=1
    print("empty_num: ",empty_num)
def empty_mv(src_dir):
    files = os.listdir(src_dir)
    pool = Pool(processes=WORKERS_empty_mv)
    for i in range(0, WORKERS_empty_mv):
        files_ = files[i:len(files):WORKERS_empty_mv]
        pool.apply_async(empty_mv_func, (files_,))
    pool.close()
    pool.join()

def dataset_check(yolo_dataset_dir):
    train_img = yolo_dataset_dir+'/'+'JPEGImages/train/images'
    eval_img = yolo_dataset_dir+'/'+'JPEGImages/eval/images'
    test_detect_img = yolo_dataset_dir + '/' + 'test_detect_img'
    test_img = yolo_dataset_dir + '/' + 'JPEGImages/test/images'
    label_train = yolo_dataset_dir+'/'+'JPEGImages/train/labels'
    label_eval = yolo_dataset_dir + '/' + 'JPEGImages/eval/labels'
    label_test = yolo_dataset_dir + '/' + 'JPEGImages/test/labels'
    test_detect_img_num = len(os.listdir(test_detect_img))
    train_img_num = len(os.listdir(train_img))
    eval_img_num = len(os.listdir(eval_img))
    test_img_num = len(os.listdir(test_img))
    train_img_white_num = len([i for i in os.listdir(train_img) if "WhiteSample" in i])
    eval_img_white_num = len([i for i in os.listdir(eval_img) if "WhiteSample" in i])
    test_img_white_num = len([i for i in os.listdir(test_img) if "WhiteSample" in i])
    label_train_num = len(os.listdir(label_train))
    label_eval_num = len(os.listdir(label_eval))
    label_test_num = len(os.listdir(label_test))
    print("train img and label num: ", train_img_num,label_train_num,"with white sample: ",train_img_white_num)
    print("eval img and label num: ", eval_img_num,label_eval_num,"with white sample: ",eval_img_white_num)
    print("test img and label num: ", test_img_num,label_test_num,"with white sample: ",test_img_white_num)
    print("detect img num: ", test_detect_img_num)
    if train_img_num==label_train_num and eval_img_num==label_eval_num and test_img_num==label_test_num:
        print(bcolors.OKGREEN+"the dataset is all right"+bcolors.ENDC)
def get_brands_and_labels(src_dir):
    xml_paths = [xml_file for xml_file in walk_xml(src_dir)]
    pool = Pool(processes=WORKERS_get_class)
    class_list = Manager().list()
    file_list = Manager().list()
    not_class_list = Manager().list()
    for i in range(0, WORKERS_get_class):
        xmls = xml_paths[i:len(xml_paths):WORKERS_get_class]
        pool.apply_async(get_brands_and_labels_func, (xmls, class_list,file_list,not_class_list,))
    pool.close()
    pool.join()
    brand_list = []
    class_num = {}
    not_class_num = {}
    file_num = {}
    brand_num = {}
    print('in the class analysis phase')
    for cls in tqdm(class_list):
        if cls in class_num:
            class_num[cls] += 1
        else:
            class_num[cls] = 1
        if cls.split('-')[0] in brand_list:
            brand_num[cls.split('-')[0]] += 1
            pass
        else:
            brand_num[cls.split('-')[0]] = 1
            brand_list.append(cls.split('-')[0])
    print('in the file analysis phase')
    for fil in tqdm(file_list):
        if fil in file_num:
            file_num[fil] += 1
        else:
            file_num[fil] = 1

    print('in the not class analysis phase')
    for cls in tqdm(not_class_list):
        if cls in not_class_num:
            not_class_num[cls] += 1
        else:
            not_class_num[cls] = 1

    print('not classes num list:', end=" ")
    for item in sorted(not_class_num, key=lambda a: not_class_num[a], reverse=True):
        print((item, not_class_num[item]), end=" ")
    print(f"\nnot in class num: {len(not_class_num)}")

    brand_list = list(set(brand_list))
    brand_list.sort(key=str.lower)
    print('classes num list:', end=" ")
    for item in sorted(class_num, key=lambda a: class_num[a], reverse=True):
        print((item, class_num[item]), end=" ")
    print("\nclasses num: ", len(class_num))

    print(bcolors.OKGREEN + 'file num list:' + bcolors.ENDC, end=" ")
    for item in sorted(file_num, key=lambda a: file_num[a], reverse=True):
        print(bcolors.OKGREEN + "(%s" % item + ", " + "%d)" % file_num[item] + bcolors.ENDC, end=" ")
    print(bcolors.OKGREEN + "\nfile num: " + bcolors.ENDC, len(file_num))

    print('brand num list:', end=" ")
    brand_list_sort = []
    for item in sorted(brand_num.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        print(item, end =" ")
        brand_list_sort.append(item[0])
    print("\nbrand num: ", len(brand_list))
    print("\n")
    print('classes list: ', sorted(class_num,key=str.lower))
    print('brand list: ', brand_list_sort)
    return sorted(class_num,key=str.lower),brand_list
def get_brands_and_labels_func(xml_ps,class_list,file_list,not_class_list):
    for anno_file in tqdm(xml_ps):
        try:
            tree = ET.parse(anno_file)
            root = tree.getroot()
        except:
            continue
        file_list.append(anno_file.split("/")[-1].split("_")[0])
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls is None:
                continue
            cls = cls.strip()
            if use_effective_brand:
                if cls.split('-')[0] not in effective_brandname:
                    continue
            if use_class_brand:
                if cls not in CLASS_list:
                    not_class_list.append(cls)
                    print(f"{cls} not in CLASS_list")
                    continue
            class_list.append(cls)

def get_xml_obj_num(anno_file):
    try:
        tree = ET.parse(anno_file)
        root = tree.getroot()
        objs = root.iter('object')
        size = root.find('size')
    except Exception as e:
        print(e)
        objs,size = -1
    return objs,size
def xml2txt(out_file,cls_boxes,size,class_list_sts):
    w = float(size.find('width').text)
    h = float(size.find('height').text)
    box_list = []
    with open(out_file, 'w') as fw:
        for obj in cls_boxes:
            cls = obj[0]
            if cls is None:
                print(out_file,"get None on name")
                continue
            cls = cls.strip()
            if cls not in classes_list:
                continue
            cls_id = classes_list.index(cls)
            xmin, xmax, ymin, ymax = obj[1],obj[2],obj[3],obj[4]
            b = [np.clip(min(xmin, xmax), 0, w), np.clip(max(xmin, xmax), 0, w), np.clip(min(ymin, ymax), 0, h),
                 np.clip(max(ymin, ymax), 0, h)]
            if b not in box_list:
                box_list.append(b)
            else:
                continue
            bb = convert((w, h), b)
            if bb[0] <= 0 or bb[0] >= 1 or bb[1] <= 0 or bb[1] >= 1 or bb[2] <= 0 or bb[3] <= 0:
                print("it's wrong box is", bb)
                print("-" * 60)
                continue

            if bb[1] > 1 or bb[3] > 1 or bb[2] > 1 or bb[0] > 1:
                print(b, bb, w, h)
                continue

            class_list_sts.append(cls)
            fw.write(str(cls_id) + " " + " ".join([str(a) if a > 0 else str(-a) for a in bb]) + '\n')
def split_data_and_rename_func(src_dir,brand_files,class_list_sts,class_list_sts_total,file_num,file_num_total,get_obj_dict):

    for files in brand_files:
        random.seed(random_seed)
        random.shuffle(files)
        for file in files:
            file_num_total.append(file)
            xml_file = Path(os.path.join(src_dir,file))
            objs,size = get_xml_obj_num(xml_file)
            if objs == -1:
                continue
            for obj in objs:
                cls = obj.find('name').text
                if cls!=None:
                    class_list_sts_total.append(cls.strip())
        if MAX_NUM_PER_BRAND:
            files = files[:MAX_NUM_PER_BRAND]
        val_num = int(len(files) * train_val_test_ratio[1])
        test_num = int(len(files) * train_val_test_ratio[2])
        for index, file_i in tqdm(enumerate(files)):
            xml_file = Path(os.path.join(src_dir,file_i))
            objs,size = get_xml_obj_num(xml_file)
            if objs == -1:
                continue
            cls_boxes = []
            for obj in objs:
                cls = obj.find('name').text
                if cls == None:
                    continue
                xmlbox = obj.find('bndbox')
                xmin, xmax, ymin, ymax = float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), \
                                         float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)
                cls_boxes.append([cls, xmin, xmax, ymin, ymax])
                if cls not in get_obj_dict:
                    get_obj_dict[cls] = 1
                else:
                    get_obj_dict[cls] += 1
            if MAX_OBJ_NUM_PER_BRAND:
                donot_need = 1
                cls_per_img = set([i[0] for i in cls_boxes if i[0] in classes_list])
                for cl in cls_per_img:
                    if get_obj_dict[cl] < MAX_OBJ_NUM_PER_BRAND:
                        donot_need = 0
                if donot_need:
                    continue
            # annotiaon_file = xml_file
            # fr = open(annotiaon_file, 'rb')
            # data = fr.read()
            # dst_annotion_file = ospathjoin([yolo_dataset_dir, "Annotations",
            #                                 xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" + file_i.replace(
            #                                     '-', '').replace(' ', '').replace('&', '')])
            # cp images
            xml_file_temp = str(xml_file)
            if os.path.exists(xml_file_temp.replace('.xml', '.jpg')):
                img_path = xml_file_temp.replace('.xml', '.jpg')
            elif os.path.exists(xml_file_temp.replace('.xml', '.jpeg')):
                img_path = xml_file_temp.replace('.xml', '.jpeg')
            elif os.path.exists(xml_file_temp.replace('.xml', '.JPG')):
                img_path = xml_file_temp.replace('.xml', '.JPG')
            elif os.path.exists(xml_file_temp.replace('.xml', '.JPEG')):
                img_path = xml_file_temp.replace('.xml', '.JPEG')
            elif os.path.exists(xml_file_temp.replace('.xml', '.png')):
                img_path = xml_file_temp.replace('.xml', '.png')
            elif os.path.exists(xml_file_temp.replace('.xml', '.PNG')):
                img_path = xml_file_temp.replace('.xml', '.PNG')
            else:
                print('Image File Not Found')
                continue
            file_num.append(file_i)
            fimg = open(img_path, 'rb')
            img_data = fimg.read()
            fimg.close()
            eval_txt_path = ospathjoin([yolo_dataset_dir, 'JPEGImages/eval/labels',xml_file.parent.name.replace(' ', '').replace("'", "").replace('&','') + "_" +xml_file.name.replace('-', '').replace(' ', '').replace('&', '').replace(".xml",".txt")])
            if index < val_num:
                if index<detect_num and detect_img_dir!=None:
                    detect_img_path = ospathjoin([detect_img_dir,
                                               xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" +
                                               img_path.split('/')[-1].replace('-', '').replace(' ', '').replace('&','')])

                    with open(detect_img_path, 'wb') as fw:
                        fw.write(img_data)
                    # detect_annotion_file = ospathjoin([detect_img_dir, "Annotations",
                    #                                    xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" +
                    #                                    file_i.replace('-', '').replace(' ', '').replace('&', '')])
                    # annotiaon_file = xml_file
                    # fr = open(annotiaon_file, 'rb')
                    # data = fr.read()
                    # with open(detect_annotion_file, 'wb') as fw:
                    #     fw.write(data)

                dst_img_path = ospathjoin([yolo_dataset_dir, 'JPEGImages/eval/images',
                                           xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" +
                                           img_path.split('/')[-1].replace('-', '').replace(' ', '').replace('&', '')])
                with open(dst_img_path, 'wb') as fw:
                    fw.write(img_data)
                xml2txt(eval_txt_path,cls_boxes,size,class_list_sts)

            elif index>=val_num and index<(val_num+test_num):
                dst_img_path = ospathjoin([yolo_dataset_dir, 'JPEGImages/test/images',
                                           xml_file.parent.name.replace(' ', '').replace("'", "").replace('&',
                                                                                                          '') + "_" +
                                           img_path.split('/')[-1].replace('-', '').replace(' ', '').replace('&', '')])
                with open(dst_img_path, 'wb') as fw:
                    fw.write(img_data)
                test_txt_path = eval_txt_path.replace('eval', 'test')
                xml2txt(test_txt_path, cls_boxes, size, class_list_sts)

            else:
                dst_img_path = ospathjoin([yolo_dataset_dir, 'JPEGImages/train/images',
                                           xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" +
                                           img_path.split('/')[-1].replace('-', '').replace(' ', '').replace('&', '')])
                with open(dst_img_path, 'wb') as fw:
                    fw.write(img_data)
                train_txt_path = eval_txt_path.replace('eval', 'train')
                xml2txt(train_txt_path, cls_boxes, size, class_list_sts)
def split_data_and_rename(src_dir):

    if detect_img_dir:
        detect_dir = Path(detect_img_dir)
        check_dir(detect_dir)
    yolo_dataset_dir_path = Path(yolo_dataset_dir)
    check_dir(yolo_dataset_dir_path)
    check_dir(yolo_dataset_dir_path / "JPEGImages/train/images")
    check_dir(yolo_dataset_dir_path / "JPEGImages/eval/images")
    check_dir(yolo_dataset_dir_path / "JPEGImages/test/images")
    check_dir(yolo_dataset_dir_path / "JPEGImages/train/labels")
    check_dir(yolo_dataset_dir_path / "JPEGImages/eval/labels")
    check_dir(yolo_dataset_dir_path / "JPEGImages/test/labels")
    brand_files = {}
    files = os.listdir(src_dir)
    for f in files:
        if f.split(".")[-1]=="xml":
            if f.find("_") != -1:
                brand = f.split("_")[0]
                if brand not in brand_files:
                    brand_files[brand] = []
                    brand_files[brand].append(f)
                else:
                    brand_files[brand].append(f)
            else:
                if "other" not in brand_files:
                    brand_files["other"] = []
                else:
                    brand_files["other"].append(f)
    brand_lists = []
    for k, v in brand_files.items():
        brand_lists.append(v)
    all_nums = int(len(files)/2)
    print("all Datasets file num is: ", all_nums)
    val_nums = int(all_nums * train_val_test_ratio[1])
    test_nums = int(all_nums * train_val_test_ratio[2])
    print("train file num is: ", all_nums - val_nums - test_nums)
    print("val file num is: ", val_nums)
    print("test file num is: ", test_nums)
    print("detect file num is: ", detect_num)

    WORKERS_spilt_ = WORKERS_spilt
    if len(brand_lists) < WORKERS_spilt:
        WORKERS_spilt_ = len(brand_lists)
    file_num = Manager().list()
    class_list_sts = Manager().list()
    file_num_total = Manager().list()
    class_list_sts_total = Manager().list()
    get_obj_dict = Manager().dict()
    pool = Pool(processes=WORKERS_spilt_)
    for i in range(0, WORKERS_spilt_):
        xmls = brand_lists[i:len(brand_lists):WORKERS_spilt_]
        pool.apply_async(split_data_and_rename_func, (src_dir, xmls,class_list_sts,class_list_sts_total,file_num,file_num_total,get_obj_dict,))
    pool.close()
    pool.join()

    #print(get_obj_dict)
    print("all labels: ", classes_list)
    print("all labels's nums: ", len(classes_list))
    assert len(classes_list) == len(set(classes_list)), "reapeat labels error."

    file_num_dict = dict()
    for file in file_num:
        if len(file.split('_')) <= 1:
            continue
        mid = file.split('_')[0]
        if mid not in file_num_dict:
            file_num_dict[mid] = 1
        else:
            file_num_dict[mid] += 1

    file_num_dict_total = dict()
    for file in file_num_total:
        if len(file.split('_')) <= 1:
            continue
        mid = file.split('_')[0]
        if mid not in file_num_dict_total:
            file_num_dict_total[mid] = 1
        else:
            file_num_dict_total[mid] += 1

    brand_names = set()
    check_brand = dict()
    check_label = dict()
    check_brand_total = dict()
    check_label_total = dict()

    for name_i in classes_list:
        bname = name_i.split('-')[0]
        brand_names.add(bname)

    res = list(brand_names)
    res.sort(key=str.lower)
    print("brand name: ", res)
    print("brand num: ", len(brand_names))
    print("total object num:", len(class_list_sts))
    for cls_i in class_list_sts:
        if cls_i not in check_label:
            check_label[cls_i] = 1
        else:
            check_label[cls_i] += 1
        bname = cls_i.split('-')[0]
        if bname not in check_brand:
            check_brand[bname] = 1
        else:
            check_brand[bname] += 1

    for cls_i in class_list_sts_total:
        if cls_i not in check_label_total:
            check_label_total[cls_i] = 1
        else:
            check_label_total[cls_i] += 1
        bname = cls_i.split('-')[0]
        if bname not in check_brand_total:
            check_brand_total[bname] = 1
        else:
            check_brand_total[bname] += 1

    if export_data_info_csv:
        pd_label = pd.DataFrame(check_label, index=["dataset_style_num"]).T
        pd_brand = pd.DataFrame(check_brand, index=["dataset_brand_num"]).T
        pd_file_num = pd.DataFrame(file_num_dict, index=["dataset_file_num"]).T

        pd_label_total = pd.DataFrame(check_label_total, index=["total_style_num"]).T
        pd_brand_total = pd.DataFrame(check_brand_total, index=["total_brand_num"]).T
        pd_file_num_total = pd.DataFrame(file_num_dict_total, index=["total_file_num"]).T

        pd_label_merge = pd.concat([pd_label_total,pd_label], axis=1)#.fillna(0, inplace=True)
        pd_brand_merge = pd.concat([pd_brand_total, pd_brand], axis=1)#.fillna(0, inplace=True)
        pd_file_merge = pd.concat([pd_file_num_total, pd_file_num], axis=1)#.fillna(0, inplace=True)

        pd_label_merge.to_csv("./data_info/%s_label_info.csv" % yolo_dataset_name.replace("yolo_dataset_", ""))
        pd_brand_merge.to_csv("./data_info/%s_brand_info.csv" % yolo_dataset_name.replace("yolo_dataset_", ""))
        pd_file_merge.to_csv("./data_info/%s_file_num_info.csv" % yolo_dataset_name.replace("yolo_dataset_", ""))

    print("checkout_brand", check_brand.keys())
    print("this dataset has brands:", len(list(check_brand.keys())))
    # assert len(list(check_brand.keys())) == len(res)
    # for key, value in check_brand.items():
    #     print("brand name : {}, num: {}".format(key, value))
    #     if value < 20:
    #         print("{} is in trouble.".format(key))
    #     else:
    #         pass
# def makeyolodir(voc_dir):
#     train_label_path = os.path.join(voc_dir, 'JPEGImages/train/labels/')
#     check_dir(train_label_path)
#     val_label_path = train_label_path.replace('train', 'eval')
#     check_dir(val_label_path)
#     test_label_path = train_label_path.replace('train', 'test')
#     check_dir(test_label_path)
#     return
def walk_xml(xml_dir):
    for root, dirs, files in os.walk(xml_dir, topdown=False):
        for name in files:
            xml_str = os.path.join(root, name)
            post_str = os.path.splitext(xml_str)[-1]
            if post_str == ".xml":
                yield xml_str
    return
# def get_xml(xml_dir):
#     for xml_file in os.listdir(xml_dir):
#         xml_str = os.path.join(xml_dir, xml_file)
#         post_str = os.path.splitext(xml_str)[-1]
#         if post_str == ".xml":
#             yield xml_str
#         else:
#             pass
#     return
def convert(size, box):
    x = ((box[0] + box[1]) / 2.0) / size[0]
    y = ((box[2] + box[3]) / 2.0) / size[1]
    w = (box[1] - box[0]) / size[0]
    h = (box[3] - box[2]) / size[1]
    return (x, y, w, h)
def wrong_xml_mv(src_dir):
    files = [file_xml for file_xml in walk_xml(src_dir)]
    pool = Pool(processes=WORKERS_xml)
    wrong_list = Manager().list()
    for i in range(0, WORKERS_xml):
        xmls = files[i:len(files):WORKERS_xml]
        pool.apply_async(wrong_xml_mv_func, (xmls,wrong_list))
    pool.close()
    pool.join()
    print("wrong_num: ",len(wrong_list))
def wrong_xml_mv_func(xml_ps,wrong_list):
    #print(len(xml_ps))
    for anno_file in tqdm(xml_ps):
        try:
            root = ET.parse(anno_file).getroot()
        except:
            if not os.path.exists(wrong_xml_dir):
                os.mkdir(wrong_xml_dir)
            wrong_list.append(anno_file)
            shutil.move(anno_file, wrong_xml_dir)
            print("find wrong xml: ", anno_file.split('/')[-1])

def add_white_sample_func(yolo_dataset_dir,white_sample_list):
    train_img = yolo_dataset_dir + '/' + 'JPEGImages/train/images'
    eval_img = yolo_dataset_dir + '/' + 'JPEGImages/eval/images'
    test_img = yolo_dataset_dir + '/' + 'JPEGImages/test/images'
    label_train = yolo_dataset_dir + '/' + 'JPEGImages/train/labels'
    label_eval = yolo_dataset_dir + '/' + 'JPEGImages/eval/labels'
    label_test = yolo_dataset_dir + '/' + 'JPEGImages/test/labels'
    #print(white_sample_dir)
    #white_sample_list = os.listdir(white_sample_dir)
    white_sample_num = len(white_sample_list)
    train_white_num = int(white_sample_num * train_val_test_ratio[0])
    eval_white_num = int(white_sample_num * train_val_test_ratio[1])
    test_white_num = white_sample_num - train_white_num - eval_white_num
    for i in tqdm(range(white_sample_num)):
        if not is_img(white_sample_list[i]):
            continue
        if i < test_white_num:
            shutil.copy(white_sample_list[i],
                        os.path.join(test_img, "checked_WhiteSample_" + white_sample_list[i].name))
            with open(os.path.join(label_test, "checked_WhiteSample_" + white_sample_list[i].name[:-(
                    len(white_sample_list[i].name.split('.')[-1]))] + 'txt'), 'w') as f:
                pass
        elif i < test_white_num + eval_white_num:
            shutil.copy(white_sample_list[i],
                        os.path.join(eval_img, "checked_WhiteSample_" + white_sample_list[i].name))
            with open(os.path.join(label_eval, "checked_WhiteSample_" + white_sample_list[i].name[:-(
                    len(white_sample_list[i].name.split('.')[-1]))] + 'txt'), 'w') as f:
                pass
        else:
            shutil.copy(white_sample_list[i],
                        os.path.join(train_img, "checked_WhiteSample_" + white_sample_list[i].name))
            with open(os.path.join(label_train, "checked_WhiteSample_" + white_sample_list[i].name[:-(
                    len(white_sample_list[i].name.split('.')[-1]))] + 'txt'), 'w') as f:
                pass

def add_white_sample(yolo_dataset_dir,white_sample_dir_list,WHITE_SAMPLE_COUNT):

    image_list_total = []
    for white_sample_dir in white_sample_dir_list:
        white_sample_list = os.listdir(white_sample_dir)
        if os.path.isdir(os.path.join(white_sample_dir,white_sample_list[0])):
            for dir in white_sample_list:
                white_sample_dir_ = os.path.join(white_sample_dir,dir)
                image_list_total += [p for p in Path(white_sample_dir_).rglob('*.*')]
        else:
            image_list_total += [p for p in Path(white_sample_dir).rglob('*.*')]
    random.shuffle(image_list_total)
    print("white samples total:",len(image_list_total))
    print("we need:",WHITE_SAMPLE_COUNT)
    image_list_total = image_list_total[:WHITE_SAMPLE_COUNT]
    add_white_sample_func(yolo_dataset_dir, image_list_total)

if show_data_info:
    if be_merged_dir:
        print("-" * 20 + "merge data start" + "-" * 20)
        merge_data(be_merged_dir, src_dir)
        print("-" * 20 + "merge data end" + "-" * 20)
    print("-"*20+"wrong xml search start"+"-"*20)
    wrong_xml_mv(src_dir)
    print("-"*20+"wrong xml search end"+"-"*20)

    print("-"*20+"empty search start"+"-"*20)
    empty_mv(src_dir)
    print("-"*20+"empty search end"+"-"*20)

    print("-" * 20 + "label & brand search start" + "-" * 20)
    class_list, _ = get_brands_and_labels(src_dir)
    print("-" * 20 + "label & brand search end" + "-" * 20)
else:
    if be_merged_dir:
        print("-" * 20 + "merge data start" + "-" * 20)
        merge_data(be_merged_dir, src_dir)
        print("-" * 20 + "merge data end" + "-" * 20)

    print("-"*20+"wrong xml search start"+"-"*20)
    #wrong_xml_mv(src_dir)
    print("-"*20+"wrong xml search end"+"-"*20)

    print("-"*20+"not pair search start"+"-"*20)
    #not_pair_mv(src_dir)
    print("-"*20+"not pair search end"+"-"*20)

    print("-"*20+"empty search start"+"-"*20)
    empty_mv(src_dir)
    print("-"*20+"empty search end"+"-"*20)

    print("-"*20+"label & brand search start"+"-"*20)
    if CLASS_list:
        classes_list = CLASS_list
        print("use defined:",classes_list)
        print(len(classes_list))
    else:
        classes_list, _ = get_brands_and_labels(src_dir)
    print("-"*20+"label & brand search end"+"-"*20)


    print("-"*20+"split data and rename start"+"-"*20)
    split_data_and_rename(src_dir)
    print("-" * 20 + "split data and rename start" + "-" * 20)

    if white_sample_dir_list:
        for white_sample_dir, num in white_sample_dir_list.items():
            print("-" * 20 + "add white sample start" + "-" * 20)
            add_white_sample(yolo_dataset_dir,[white_sample_dir],num)
            print("-" * 20 + "add white sample end" + "-" * 20)

    print("-"*20+"dataset check start"+"-"*20)
    dataset_check(yolo_dataset_dir)
    print("-"*20+"dataset check end"+"-"*20)
