# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:27:06 2020

@author: Administrator
"""

import os
import json
import shutil

from tqdm import tqdm

img_path = './traffic_light_test_img'
label_path = './traffic_light_test_img_label/outputs'

cut_img_path = img_path+'_cut'
cut_label_path = './json_cut'
txt_label_path = './txt_label_cut'
if not os.path.exists(cut_img_path):
    os.makedirs(cut_img_path)
else:
    shutil.rmtree(cut_img_path)
    os.makedirs(cut_img_path)
if not os.path.exists(cut_label_path):
    os.makedirs(cut_label_path)
else:
    shutil.rmtree(cut_label_path)
    os.makedirs(cut_label_path)
if not os.path.exists(txt_label_path):
    os.makedirs(txt_label_path)
else:
    shutil.rmtree(txt_label_path)
    os.makedirs(txt_label_path)
def shapes_to_label(json_file_path,savaFileName):
    list_path = os.listdir(json_file_path)
    useful_file = 0
    print('-----translating-----')
    for i in tqdm(range(0,len(list_path))):
        jpath = os.path.join(json_file_path,list_path[i])
        if os.path.isfile(jpath):
            data = json.load(open(jpath))
            data = data['outputs']
            if data != {} and data['object'] != []:
                data = data['object']
                file_handle = open(savaFileName + '/'+list_path[i].replace('.json','.txt'), mode='w')
                useful_file += 1
                for shape in data:
                    if 'bndbox' in shape.keys():
                        bndboxs = shape['bndbox']
                        file_handle.write("traffic_light")
                        file_handle.write(",")
                        file_handle.write(str(bndboxs['xmin']))
                        file_handle.write(",")
                        file_handle.write(str(bndboxs['ymin']))
                        file_handle.write(",")
                        file_handle.write(str(bndboxs['xmax']))
                        file_handle.write(",")
                        file_handle.write(str(bndboxs['ymax']))
                        file_handle.write("\n")   
                file_handle.close()
    print('\n%d useful file json to txt done'%useful_file)


def delete_unlabeled_image(im_path,la_path):
    image_path = os.listdir(im_path)
    del_num = 0
    print('-----copying useful files-----')
    for i in tqdm(range(len(image_path))):
        if os.path.exists(la_path + '/'+image_path[i].replace('.jpg','.txt')):
            shutil.copy(im_path + '/'+image_path[i],cut_img_path)
            shutil.copy(label_path + '/' + image_path[i].replace('.jpg','.json'), cut_label_path)
            #shutil.rmtree(im_path + '/'+image_path[i].split('.')[0] +'.jpg')
            del_num+=1
    print('%d unlabeled images are deleted done'%(len(image_path)-del_num))


def check_image_label(im_path,la_path):
    print('-----checking-----')
    image_path = os.listdir(im_path)
    for i in tqdm(range(len(image_path))):
        if not os.path.exists(la_path + '/'+image_path[i].replace('.jpg','.txt')):
            print('%s is not exist'%(la_path + '/'+image_path[i].replace('.jpg','.txt')))
    label_path = os.listdir(la_path)
    for i in tqdm(range(len(label_path))):
        if not os.path.exists(im_path + '/'+label_path[i]):
            print('%s is not exist'%(im_path + '/'+label_path[i]))
    print('check done')


def copy(im_path,txt_label_path,times):
    times_im_path = im_path+'_times'
    times_txt_label_path = txt_label_path + '_times'
    if not os.path.exists(times_im_path):
        os.makedirs(times_im_path)
    else:
        shutil.rmtree(times_im_path)
        os.makedirs(times_im_path)
    if not os.path.exists(times_txt_label_path):
        os.makedirs(times_txt_label_path)
    else:
        shutil.rmtree(times_txt_label_path)
        os.makedirs(times_txt_label_path)
    images = os.listdir(im_path)
    labels = os.listdir(txt_label_path)
    print()
    for i in range(times):
        print('-----copying---%d times-----'%i)
        for img in tqdm(images):
            shutil.copy(im_path+'/'+img, times_im_path+'/'+img.replace('.jpg','')+'_'+str(i)+'.jpg')
        for txt in tqdm(labels):
            shutil.copy(txt_label_path+'/'+txt, times_txt_label_path+'/'+txt.replace('.jpg','')+'_'+str(i)+'.txt')
    print('copy done')

def json2txt(img_path,label_path,txt_label_path,times = None):
    shapes_to_label(label_path,txt_label_path)
    delete_unlabeled_image(img_path,txt_label_path)
    #check_image_label(cut_img_path,txt_label_path)
    if times!=None:
        copy(cut_img_path,txt_label_path,times)


if __name__ == '__main__':
    json2txt(img_path,label_path,txt_label_path)


































































