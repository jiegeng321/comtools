#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""
import os
import random

import numpy as np
from pathlib import Path
import xml.etree.ElementTree as ET

from evaluator.eval_api import Evaluation

gs = [".jpg", '.png', '.jpeg']


class YOLOTest(Evaluation):

    def parse_rec(self, filename):
        """Parse a PASCAL VOC xml file."""
        tree = ET.parse(filename)
        objects = []
        for obj in tree.findall('object'):
            obj_struct = {}
            obj_struct['name'] = "LOGO"
            obj_struct['pose'] = obj.find('pose').text
            obj_struct['truncated'] = int(obj.find('truncated').text)
            obj_struct['difficult'] = int(obj.find('difficult').text)
            bbox = obj.find('bndbox')

            x1 = int(float(bbox.find('xmin').text))
            y1 = int(float(bbox.find('ymin').text))
            x2 = int(float(bbox.find('xmax').text))
            y2 = int(float(bbox.find('ymax').text))
            xmin = min(x1, x2)
            ymin = min(y1, y2)
            xmax = max(x1, x2)
            ymax = max(y1, y2)

            obj_struct['bbox'] = [xmin,ymin,xmax,ymax]
            objects.append(obj_struct)

        return objects

    def get_anno(self, xml_path):
        if not xml_path.is_file():
            return []
        return self.parse_rec(xml_path)

    def get_detboxes(self):
        self.det_boxes = {}
        for img_name, value in self.val_boxes.items():
            ds = np.empty([0, 6])
            for v in value:
                ds = np.vstack([ds, np.array([0] + v['bbox']+ [random.random()])])
            self.det_boxes[img_name] = ds


    def get_valboxes(self):
        self.annos = Path(self.root) / "Annotations"
        self.xmls = [i for i in self.annos.rglob('*.xml')]
        self.val_boxes = {}
        self.img_path = Path(self.root) / "JPEGImages/eval/images"
        self.image_names = [i.name for i in self.img_path.rglob("*.*") if i.suffix.lower() in gs]

        for img_name in self.image_names:
            exp = Path(img_name)
            xml_name = exp.stem
            self.val_boxes[img_name] = self.get_anno(self.annos / (xml_name+".xml"))


if __name__=="__main__":
    eval_exp = YOLOTest(["LOGO"], None, "/data01/erwei.wang/dataset/yolo_dataset_comb_38bs_80ks")
    # eval_exp = YOLOTest(["LOGO"], None, "/data01/erwei.wang/50bsx20_logoness_test")
    # print(eval_exp.val_boxes)
    eval_exp.get_detboxes()
    eval_exp.evaluate_detections()