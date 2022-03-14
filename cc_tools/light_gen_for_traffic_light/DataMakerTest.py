from HD_MAP_LIGHT_Dataset_Maker import data_maker
from threading import Thread
import multiprocessing
import os
import time
import pandas as pd
from PIL import Image
import numpy as np
from tqdm import tqdm

SAVE_PATH = './HD_MAP_LIGHT' 
THREAD_COUNT = 4 # 生产线程数量
MAKE_COUNT = 20 * THREAD_COUNT  # 生成图片数量 (没有处理余数，所以最好能被线程数整除：线程数的整数倍）
MULTIPROCESSING = False
# -------------------不用修改---------------
TRAIN_IMG_DIR = 'train_images'
TRAIN_LABEL_DIR = 'train_label'
VAL_IMG_DIR = 'val_images'
VAL_LABEL_DIR = 'val_label'

TEMP_MAX_LINE = 100
IMAGE_SAVE_QUALITY = 100


def ThreadCardMaker(maker_count = 100, t_name="t1"):


    for index in tqdm(range(maker_count)):

        img,label,name =  data_maker()
        if index%10 in (0,1,2,3,4,5,6,7,8):
            image_path = os.path.join(SAVE_PATH, TRAIN_IMG_DIR, 'train_{0}.jpg'.format(name))
            txt_path = os.path.join(SAVE_PATH, TRAIN_LABEL_DIR, 'train_{0}.txt'.format(name))
        else:
            image_path = os.path.join(SAVE_PATH, VAL_IMG_DIR, 'val_{0}.jpg'.format(name))
            txt_path = os.path.join(SAVE_PATH, VAL_LABEL_DIR, 'val_{0}.txt'.format(name))

        img.save(image_path, quality=IMAGE_SAVE_QUALITY)
        with open(txt_path,mode='w',encoding='utf-8') as f:
            f.write(label)


def CheckAndMakeDirs():
    # 数据根目录是否存在
    save_img_t = os.path.join(SAVE_PATH, TRAIN_IMG_DIR)
    save_txt_t = os.path.join(SAVE_PATH, TRAIN_LABEL_DIR)
    save_img_v = os.path.join(SAVE_PATH, VAL_IMG_DIR)
    save_txt_v = os.path.join(SAVE_PATH, VAL_LABEL_DIR)
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    if not os.path.exists(save_img_t):
        os.makedirs(save_img_t)
    if not os.path.exists(save_txt_t):
        os.makedirs(save_txt_t)
    if not os.path.exists(save_img_v):
        os.makedirs(save_img_v)
    if not os.path.exists(save_txt_v):
        os.makedirs(save_txt_v)
if __name__ == '__main__':

    start = time.time()
    CheckAndMakeDirs()

    # 计算每个线程 生成的图片数量
    thread_make_count = MAKE_COUNT // THREAD_COUNT

    thread_list = []
    if MULTIPROCESSING:
        for i in range(THREAD_COUNT):
            thread_maker = multiprocessing.Process(target=ThreadCardMaker,args=(thread_make_count, "t{0}".format(i),))
            thread_list.append(thread_maker)
    else:
        for i in range(THREAD_COUNT):
            thread_maker = Thread(target=ThreadCardMaker,args=(thread_make_count, "t{0}".format(i),))
            thread_list.append(thread_maker)


    for t in thread_list:
        t.daemon = True
        t.start()
    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("child   p.name:" + p.name + "\tp.id" + str(p.pid))

    for t in thread_list:
        t.join()

    print('Total time(s) : ',int(time.time() - start))
    print('finish')
