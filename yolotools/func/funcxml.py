#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""
import os

def save_xml(image_name, bbox, labels, save_dir='./VOC2007/Annotations', width=1609, height=500, channel=3):
    from lxml.etree import Element, tostring
    from lxml.etree import SubElement
    from xml.dom.minidom import parseString
    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = save_dir

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = '%s' % width

    node_height = SubElement(node_size, 'height')
    node_height.text = '%s' % height

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '%s' % channel

    for index, (x, y, w, h) in enumerate(bbox):
        left, top, right, bottom = x, y, w, h
        name = labels[index]
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = name
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = '%s' % left
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = '%s' % top
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = '%s' % right
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = '%s' % bottom

    xml = tostring(node_root, pretty_print=True)
    #dom = parseString(xml)

    # save_xml = os.path.join(save_dir, image_name.replace('jpg', 'xml'))
    # with open(save_xml, 'wb') as f:
    #     f.write(xml)

    return xml


def change2xml(label_dict={}):
    for image in label_dict.keys():
        image_name = os.path.split(image)[-1]
        bbox = label_dict.get(image, [])
        save_xml(image_name, bbox)
    return


def readxml(annotion_path):
    # print(annotion_path)
    res = []
    from xml.etree import ElementTree as ET
    try:
        root = ET.parse(annotion_path).getroot()
    except :
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
    return res



