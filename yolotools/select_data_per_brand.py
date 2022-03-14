#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""
import random
import os.path
from pathlib import Path
# from func.funcxml import readxml
from comfunc.check import check_dir
from multiprocessing import Pool, Manager


def readxml(annotion_path):
    # print(annotion_path)
    res = []
    labels = []
    from xml.etree import ElementTree as ET
    try:
        root = ET.parse(annotion_path).getroot()
    except FileExistsError:
        assert "the file is not found."
    else:
        bboxes = root.find("object")
        for index, subtree in enumerate(root.iter('object')):
            label = subtree.find("name").text
            bbox = subtree.find('bndbox')
            x1 = float(bbox.find('xmin').text)
            y1 = float(bbox.find('ymin').text)
            x2 = float(bbox.find('xmax').text)
            y2 = float(bbox.find('ymax').text)
            res.append((label, x1, y1, x2, y2))
            labels.append(label)
    return labels



#获取xml中的所有样式
def get_styles(xml_path):
    xml_path = Path(xml_path)
    xmls = [xml for xml in xml_path.rglob("*.xml")]
    styles = []
    pool = Pool(20)
    for index, item in enumerate(xmls):
        styles.append(pool.apply_async(readxml, args=(str(item),)))
    pool.close()
    pool.join()
    styles_list = [i.get() for i in styles]
    style_res = []
    for i in styles_list:
        style_res += i
    return list(set(style_res))

#新建yolo dir
def makeyolodir(dst_dir):
    dst_dir = Path(dst_dir)
    check_dir(dst_dir)
    check_dir(dst_dir / "Annotations")
    check_dir(dst_dir / "JPEGImages/train/images")
    check_dir(dst_dir / "JPEGImages/eval/images")

#根据xml寻找对应图片
def find_image(xml):
    fix_str = [".jpg", '.png', '.jpeg', '.JPEG', ".PNG", ".JPG"]
    for i in fix_str:
        img_path = xml.replace("Annotations", "JPEGImages/train/images").replace(".xml", i)
        if os.path.exists(img_path):
            return img_path
        img_path = img_path.replace("train", "eval")
        if os.path.exists(img_path):
            return img_path
    return None


def copy_file(xml, dst_dir):
    anno_dir = os.path.join(dst_dir, "Annotations")
    image_dir = os.path.join(dst_dir, "JPEGImages/train/images")
    stem = xml.stem

    # copy image
    img_path = find_image(str(xml))
    if img_path is None:
        return
    img_path = Path(img_path)
    with open(str(img_path), 'rb') as fr_img:
        data = fr_img.read()
        img_p = os.path.join(image_dir, img_path.name)
        fw_i = open(img_p, 'wb')
        fw_i.write(data)
        fw_i.close()

    # copy xml
    with open(str(xml), 'rb') as fr:
        data = fr.read()
        xml_path = os.path.join(anno_dir, xml.name)
        fw = open(xml_path, 'wb')
        fw.write(data)
        fw.close()




def select_data(styles_dict, anno_dir, dst_dir, min_num=25):
    xml_path = Path(anno_dir)
    xmls = [xml for xml in xml_path.rglob("*.xml")]
    random.shuffle(xmls)
    for xml in xmls:
        labels = readxml(str(xml))

        iscopy = False
        for label in labels:
            if label in styles_dict:
                if styles_dict[label]>=min_num:
                    continue
                else:
                    iscopy = True
                    break
            else:
                iscopy = True
                break

        if iscopy:
            copy_file(xml, dst_dir)
            for label in labels:
                if label in styles_dict:
                    styles_dict[label] +=1
                else:
                    styles_dict[label] =1


if __name__=="__main__":

    #原始的xml文件集
    src_path = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/checked"

    #被选中的数据copy的新的目录
    dst_path = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data_per20"

    makeyolodir(dst_path)
    final_dict = {}
    select_data(final_dict, src_path, dst_path)
    print(final_dict)




