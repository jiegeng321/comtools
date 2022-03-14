#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""
import argparse
from pathlib import Path

def readxml(annotion_path):
    print(annotion_path)
    res = []
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
    res = list(set(res))
    return res

def get_label_nums(annotiton_dir):
    annotiton_dir = Path(annotiton_dir)
    xmls = annotiton_dir.rglob("*.xml")
    sums = 0
    for xml in xmls:
        add_num = len(readxml(xml))
        sums += add_num

    return sums

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, default=None, help='initial weights path')
    opt = parser.parse_args()
    opt.p = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/problem_brand/emoji/"
    sums = get_label_nums(opt.p)
    print("the fianl box num is: ", sums)
