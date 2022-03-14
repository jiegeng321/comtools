# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:27:06 2020

@author: Administrator
"""
import shutil
import numpy as np
import os
import json
import io
import PIL.Image
from tqdm import tqdm

json_file_path = "face_pts_prelabel_myself"
txt_save_path = "face_pts_prelabel_myself_txt"
img_save_path = "face_pts_prelabel_myself_img"
list_path = os.listdir(json_file_path)
    #print(list_path)
    #useful_file = 0
if not os.path.exists(txt_save_path):
    os.makedirs(txt_save_path)
if not os.path.exists(img_save_path):

    os.makedirs(img_save_path)
for file in tqdm(list_path):
    if os.path.splitext(file)[-1] != '.json':
        continue
    jpath = os.path.join(json_file_path,file)
    data = json.load(open(jpath))
    shapes = data["shapes"]
    if shapes!=[] and len(shapes)==4:
        with open(os.path.join(txt_save_path,os.path.splitext(file)[0]+".txt"),'w') as f:
            for shape in shapes:
                for point in shape["points"]:
                    for xy in point:
                        f.write(str(xy)+' ')
        shutil.copyfile(os.path.join(json_file_path,os.path.splitext(file)[0]+".jpg"),os.path.join(img_save_path,os.path.splitext(file)[0]+".jpg"))
'''
image_path = "./idcard_get_box_img"
label_path = "idcard_get_box_txt_label"
json_path = "./idcard_get_box_json_label"
def shapes_to_label(json_file_path,savaFileName):
    list_path = os.listdir(json_file_path)
    #print(list_path)
    useful_file = 0
    if not os.path.exists(savaFileName):
        os.makedirs(savaFileName)
    for i in tqdm(range(0,len(list_path))):
        conti = 0
        jpath = os.path.join(json_file_path,list_path[i])
        if os.path.isfile(jpath):
            data = json.load(open(jpath))
            data = data['outputs']
            if data != {} and data['object'] != []:
                data = data['object']
                #if len(data)<4:
                #    continue
                for shape in data:
                    if 'polygon' in shape.keys():
                        polygons = shape['polygon']
                        if len(polygons)!=8:
                            conti = 1
                if conti == 1:
                    continue
                file_handle = open(savaFileName + '/'+list_path[i].split('.')[0] +'.txt', mode='w')
                useful_file += 1
                for shape in data:
                    if 'polygon' in shape.keys():
                        polygons = shape['polygon'] 
                        index = ['x1','y1','x2','y2','x3','y3','x4','y4']
                        for m in range(len(polygons)):
                            file_handle.write(str(polygons[index[m]]))
                            file_handle.write(",")
                        file_handle.write("chinese")
                        file_handle.write(",")
                        file_handle.write("####")
                        file_handle.write("\n")  
                    if 'bndbox' in shape.keys():
                        bndboxs = shape['bndbox']
                        if bndboxs['xmin']:
                            file_handle.write(str(int(bndboxs['xmin'])))
                            file_handle.write(",")
                            file_handle.write(str(int(bndboxs['ymin'])))
                            file_handle.write(",")
                            file_handle.write(str(int(bndboxs['xmax'])))
                            file_handle.write(",")
                            file_handle.write(str(int(bndboxs['ymin'])))
                            file_handle.write(",")
                            file_handle.write(str(int(bndboxs['xmax'])))
                            file_handle.write(",")
                            file_handle.write(str(int(bndboxs['ymax'])))
                            file_handle.write(",")
                            file_handle.write(str(int(bndboxs['xmin'])))
                            file_handle.write(",")
                            file_handle.write(str(int(bndboxs['ymax'])))
                            file_handle.write(",")
                            file_handle.write("chinese")
                            file_handle.write(",")
                            file_handle.write("####")
                            file_handle.write("\n")
                        else:
                            print(jpath)
                file_handle.close()
    print('%d useful file json to txt done'%useful_file)
def delete_unlabeled_image(im_path,la_path):
    image_path = os.listdir(im_path)
    del_num = 0
    for i in tqdm(range(len(image_path))):
        if not os.path.exists(la_path + '/'+image_path[i].split('.')[0] +'.txt'):
            os.remove(im_path + '/'+image_path[i].split('.')[0] +'.jpg')
            del_num += 1
    print('%d unlabeled images are deleted done'%del_num)
def check_image_label(im_path,la_path):
    image_path = os.listdir(im_path)
    for i in tqdm(range(len(image_path))):
        #shutil.copyfile(im_path + '/'+image_path[i].split('.')[0] +'.jpg.bmp',
        #                'image2' + '/'+image_path[i].split('.')[0] +'.jpg' )
        if not os.path.exists(la_path + '/'+image_path[i].split('.')[0] +'.txt'):
            print('%s is not exist'%(la_path + '/'+image_path[i].split('.')[0] +'.txt'))
    label_path = os.listdir(la_path)
    for i in tqdm(range(len(label_path))):
        if not os.path.exists(im_path + '/'+label_path[i].split('.')[0] +'.jpg'):
            print('%s is not exist'%(im_path + '/'+label_path[i].split('.')[0] +'.jpg'))
    print('check done')
shapes_to_label(json_path,label_path)
delete_unlabeled_image(image_path, label_path)
check_image_label(image_path, label_path)

'''


































































