#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author:panyanghui
@file:cleaner.py
@time:2021/10/19
"""
'''
  /*******************************/
  代码功能：核对两组logo集合中，是否有相似logo
    
  逻辑说明：
    1、 
    2、 
'''

import os
import numpy as np
from tqdm import tqdm
import torch
from PIL import Image

import argparse

def preproc(img):
    img = img.resize((112, 112),Image.BILINEAR)
    img = np.array(img)
    img = img[:, :, [2, 1, 0]]
    mean_vec = np.array([0.485, 0.456, 0.406],
                        dtype=np.float32).reshape((1, 1, 3))
    stddev_vec = np.array([0.229, 0.224, 0.225],
                          dtype=np.float32).reshape((1, 1, 3))
    norm_img_data = img / 255.0 - mean_vec
    norm_img_data /= stddev_vec
    input_image = np.expand_dims(norm_img_data, axis=0).transpose((0, 3, 1, 2))
    return input_image

def run_task(model_path):
    model = torch.jit.load(model_path, map_location=torch.device('cuda:0'))
    ###生成底库
    db_fea = []
    db_lable = []
    logo_nums = []
    for root, dirs, imgs in tqdm(os.walk(folder1)):
        c1 = 0
        for line in imgs:
            try:
                img = Image.open(os.path.join(root, line)).convert("RGB")
                # new_img = transform(img).to(device_i  d)
                # new_img = torch.unsqueeze(new_img, dim=0).float()
                new_img = preproc(img)
                new_img = torch.from_numpy(new_img).to(device_id).float()
                fea = model(new_img)
                feature1 = fea.detach().cpu().numpy()
                feature1 = feature1 / np.linalg.norm(feature1)
                db_fea.append(feature1.tolist()[0])
                db_lable.append(os.path.join(root, line))
                c1 = c1 + 1
            except:
                continue
        logo_nums.append(c1)

    db_fea = np.array(db_fea)
    if single_set == 'F':
        print('scaning imgcuts！')
        imgcut_fea = []
        imgcut_lable = []

        for root, dirs, imgs in tqdm(os.walk(folder2)):
            for line in imgs:
                try:
                    img = Image.open(os.path.join(root, line)).convert("RGB")
                    # new_img = transform(img).to(device_i  d)
                    # new_img = torch.unsqueeze(new_img, dim=0).float()
                    new_img = preproc(img)
                    new_img = torch.from_numpy(new_img).to(device_id).float()
                    fea = model(new_img)
                    feature1 = fea.detach().cpu().numpy()
                    feature1 = feature1 / np.linalg.norm(feature1)
                    imgcut_fea.append(feature1.tolist()[0])
                    imgcut_lable.append(os.path.join(root, line))
                except:
                    continue
        imgcut_fea = np.array(imgcut_fea)
        print('imgcut feature over!')

    c = 0
    for num in tqdm(logo_nums):
        try:
            label_list = []
            label_test1 = db_fea[c:c + num]
            label_test1 = np.array(label_test1)
            before_label = db_lable[c].split('/')[-2]

            if single_set == 'T':
            ##########单纯在b集合之间进行筛查
                label_test2 = db_fea[c+ num :]
                label_test2 = np.array(label_test2)
                label_dk_2 = db_lable[c+ num :]
                sim_matrix = np.matmul(label_test1, label_test2.transpose())
                top = np.argsort(-sim_matrix, axis=1)[:, 0].tolist()
                for j in range(len(top)):
                    if sim_matrix[j, top[j]] > thr:
                        if label_dk_2[top[j]].split('/')[-2] not in label_list:
                            label_list.append(label_dk_2[top[j]].split('/')[-2])

            elif single_set == 'F':
                ##########在a、b集合之间进行筛查
                sim_matrix = np.matmul(label_test1, imgcut_fea.transpose())
                top = np.argsort(-sim_matrix, axis=1)[:, 0].tolist()
                for j in range(len(top)):
                    if thr < sim_matrix[j, top[j]]:
                        if imgcut_lable[top[j]].split('/')[-2] not in label_list:
                            label_list.append(imgcut_lable[top[j]].split('/')[-2])
            else:
                print('the wrong single_set!')

            for k in label_list:
                f_save.write('{}#;#{}\n'.format(before_label, k))

            c = c + num

        except:
            continue
    f_save.close()

    #######将相似id每类挑两张放在一个文件夹下
    f11 = open(save_file, 'r')
    lines = f11.readlines()
    path_head1 = folder1
    if single_set == 'T':
        path_head2 = path_head1
    else:
        path_head2 = folder2

    for line in lines:
        line = line.strip()
        if line == '':
            continue
        else:
            label1, label2 = line.split('#;#')
            save_folder_i = save_folder + label1 + '*' + label2
            print(save_folder_i)
            if not os.path.exists(save_folder_i):
                os.makedirs(save_folder_i)
            for root, dirs, imgs in os.walk(os.path.join(path_head1 , label1)):
                if len(imgs) > 0:
                    for i, img in enumerate(imgs[:2]):
                        p1 = os.path.join(root, img).replace(' ', '\ ').replace('#', '\#').replace("'", "\'")
                        p2 = os.path.join(save_folder_i, label1 + '_{}.jpg'.format(i)).replace(' ', '\ ').replace(
                            '#',
                            '\#').replace(
                            "'", "\'")
                        cmd = 'cp {} {}'.format(p1, p2)
                        os.popen(cmd).readlines()
            for root, dirs, imgs in os.walk(os.path.join(path_head2 , label2)):
                if len(imgs) > 0:
                    for i, img in enumerate(imgs[2:4]):
                        p1 = os.path.join(root, img).replace(' ', '\ ').replace('#', '\#').replace("'", "\'")
                        p2 = os.path.join(save_folder_i, label2 + '_{}.jpg'.format(i + 2)).replace(' ',
                                                                                                   '\ ').replace(
                            '#',
                            '\#').replace(
                            "'", "\'")
                        cmd = 'cp {} {}'.format(p1, p2)
                        os.popen(cmd).readlines()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', '--folder1', dest='folder1', type=str, default='',
                        help='the uncover_data_file!')
    parser.add_argument('-f2', '--folder2', dest='folder2', type=str, default='',
                        help='the thread_num!')
    parser.add_argument('-s', '--single_set', dest='single_set', type=str, default='',
                        help='the thread_num!')
    parser.add_argument('-t', '--thr', dest='thr', type=int, default=0.8,
                        help='the thread_num!')
    args = parser.parse_args()
    folder1 = args.folder1
    folder2 = args.folder2
    single_set = args.single_set
    thr = args.thr

    model_path = './resource/model/pro_resnet18_54_checkpoint.pt'
    save_folder  = './resource/result/same/'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    save_file = './resource/result/same.csv'
    f_save = open(save_file,'w')

    if torch.cuda.is_available():
        device_id = 0
    else:
        device_id = "cpu"

    print('Pytorch version: {}'.format(torch.__version__))
    print('os environ: {}'.format(os.environ))
    run_task(model_path)


