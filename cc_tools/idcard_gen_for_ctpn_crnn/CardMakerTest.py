from CardMaker import CardMaker
from threading import Thread
import os
import time
import pandas as pd
from PIL import Image
import numpy as np
import uuid

SAVE_PATH = './IDC' # 保存完整的图片（1000 * 1000），正反面在一起
THREAD_COUNT = 4 # 生产线程数量
MAKE_COUNT = 2 * THREAD_COUNT  # 生成图片数量 (没有处理余数，所以最好能被线程数整除：线程数的整数倍）

# -------------------不用修改---------------
NO_STAMP_DIR = 'IDC_front_image'
WITH_STAMP_DIR = 'IDC_back_image'
txt_front_dir = 'IDC_front_txt'
txt_back_dir = 'IDC_back_txt'
image_crop_dir = 'IDC_image_crop_dir'
TEMP_MAX_LINE = 100
IMAGE_SAVE_QUALITY = 95
IMAGE_SINGLE_SIDE_W = 480
IMAGE_SINGLE_SIDE_H = 350

def ThreadCardMaker(maker_count = 100, t_name="t1"):

    maker = CardMaker()
    for index in range(maker_count):

        person_info,image_front2,image_back2,txt_f,txt_b,image_list_crop,image_name_list_crop =  maker.get_train_image2()
        image_f_path = os.path.join(SAVE_PATH, NO_STAMP_DIR, '{0}_{1}_f.jpg'.format(person_info['id_code'], person_info['uuid']))
        image_b_path = os.path.join(SAVE_PATH, WITH_STAMP_DIR, '{0}_{1}_b.jpg'.format(person_info['id_code'], person_info['uuid']))
        txt_f_path = os.path.join(SAVE_PATH, txt_front_dir,
                                     '{0}_{1}_f.txt'.format(person_info['id_code'], person_info['uuid']))
        txt_b_path = os.path.join(SAVE_PATH, txt_back_dir,
                                     '{0}_{1}_b.txt'.format(person_info['id_code'], person_info['uuid']))
        for i in range(len(image_list_crop)):
            crop_name  =uuid.uuid4().hex
            image_crop_dir_dir_path = os.path.join(SAVE_PATH, image_crop_dir,'{0}.jpg'.format(crop_name))
            txt_crop_dir_dir_path = os.path.join(SAVE_PATH, image_crop_dir,'{0}.txt'.format(crop_name))
            image_list_crop[i].save(image_crop_dir_dir_path,quality=IMAGE_SAVE_QUALITY)
            with open(txt_crop_dir_dir_path,'w') as f:
                f.write(image_name_list_crop[i].replace(' ',''))
            '''
            image_crop_dir_dir_path = os.path.join(SAVE_PATH, image_crop_dir,
                                                   '{0}@{1}.jpg'.format(image_name_list_crop[i],
                                                                        person_info['id_code'] + '_' + person_info[
                                                                            'uuid']))
            image_list_crop[i].save(image_crop_dir_dir_path, quality=IMAGE_SAVE_QUALITY)
            '''
        # 保存图片
        image_front2.save(image_f_path, quality=IMAGE_SAVE_QUALITY)
        image_back2.save(image_b_path, quality=IMAGE_SAVE_QUALITY)
        with open(txt_f_path,mode='w',encoding='utf-8') as f:
            f.write(txt_f)
        with open(txt_b_path,mode='w',encoding='utf-8') as f:
            f.write(txt_b)

        print(t_name, index, person_info['name'], person_info['province'],person_info['id_code'])

def CheckAndMakeDirs():
    # 数据根目录是否存在
    save_txt_f = os.path.join(SAVE_PATH, txt_front_dir)
    save_txt_b = os.path.join(SAVE_PATH, txt_back_dir)
    save_txt_c = os.path.join(SAVE_PATH, image_crop_dir)
    if not os.path.exists(save_txt_c):
        os.makedirs(save_txt_c)
    if not os.path.exists(save_txt_f):
        os.makedirs(save_txt_f)
    if not os.path.exists(save_txt_b):
        os.makedirs(save_txt_b)
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    no_stamp_path = os.path.join(SAVE_PATH, NO_STAMP_DIR)
    if not os.path.exists(no_stamp_path):
        os.makedirs(no_stamp_path)
    with_stamp_path = os.path.join(SAVE_PATH, WITH_STAMP_DIR)
    if not os.path.exists(with_stamp_path):
        os.makedirs(with_stamp_path)
if __name__ == '__main__':

    # ----------单线程----------
    # 创建身份证生成器
    maker = CardMaker()
    start = time.clock()

    CheckAndMakeDirs()

    # 计算每个线程 生成的图片数量
    thread_make_count = MAKE_COUNT // THREAD_COUNT

    thread_list = []
    for i in range(THREAD_COUNT):

        # ----------多线程 测试（文件生成）----------
        thread_maker = Thread(target=ThreadCardMaker,args=(thread_make_count, "t{0}".format(i),))
        thread_list.append(thread_maker)

    # 启动子线程
    for t in thread_list:
        t.setDaemon(True)
        t.start()

    # 等待合并csv文件
    for t in thread_list:
        t.join()

    print('Total time(s) : ',int(time.process_time() - start))
    print('finish')









    #----------------------以下内容 临时保存文件 暂时不要删除u-------------------

    #
    # # 获取随机用户信息（速度估算：不保存文件 12.8s/百张， 保存文件 24s/百张)
    # for i in range(1):
    #     # ------- 快速生成图片（0.10s~0.15s/每张)-------#
    #     '''
    #     person_info: 用户信息（dict）
    #          'addr': '内蒙古包头市达尔罕茂明安联合旗大连路',# 身份证正面 信息 户籍地址
    #          'area_code': '150223',       # 身份证正面 隐藏信息 地址所在区的编码
    #          'back_angle': 3,             # 身份证背面 旋转角度
    #          'back_new_loc': (334, 626),  # 身份证背面 填充背景后 坐标
    #          'back_new_size': (464, 306), # 身份证背面 证件旋转后 新尺寸
    #          'back_rotate_180': 0,        # 身份证背面 是否翻转（180 或 0）
    #          'back_stamp_alpha': 169,     # 身份证背面 印章 透明度 (例如：169÷255 ≈ 66%透明度）
    #          'back_stamp_angle': -19,     # 身份证背面 印章 旋转角度（负值 逆时针）
    #          'birthday_d': '16',          # 身份证正面 信息 生日（日） 注意：不足两位时，左侧填充空白对齐
    #          'birthday_m': '  8',         # 身份证正面 信息 生日（月） 注意：不足两位时，左侧填充空白对齐
    #          'birthday_y': '1940',        # 身份证正面 信息 生日（年）
    #          'front_angle': -1,           # 身份证正面 旋转角度
    #          'front_new_loc': (339, 141), # 身份证正面 填充背景后 坐标
    #          'front_new_size': (454, 290),# 身份证正面 证件旋转后 新尺寸
    #          'front_rotate_180': 0,       # 身份证正面 是否翻转（180 或 0）
    #          'front_stamp_alpha': 169,    # 身份证正面 印章 透明度 (例如：169÷255 ≈ 66%透明度）
    #          'front_stamp_angle': -13,    # 身份证正面 印章 旋转角度（负值 逆时针）
    #          'brightness_rate': 0.86,     # 训练图片 亮度值（调整后的亮度）
    #          'gaussian_blur_radius': 0.76,# 训练图片 高斯模糊滤波 （随机值域 0.2~1.2)
    #          'id_code': '150223194008167001', # 身份证正面 信息 身份证号码 注意：10%概率生成17位错误号码
    #          'id_code_err': 0,            # 身份证正面 信息 身份证号码错误标示（0 或 1）
    #          'name': '朱伟豪',             # 身份证正面 信息 姓名（随机 姓名 列表）
    #          'nationality': '拉祜',        # 身份证正面 信息 民族（随机 民族 列表）
    #          'office': '包头市达尔罕茂明安联合旗公安局',# 身份证背面 信息 发证机关（根据地址自动生成）
    #          'province': '内蒙古',         # 身份证背面 隐藏信息 所在省
    #          'sex': '男',                  # 身份证正面 信息 性别（男、女）
    #          'valid': '1978.04.25-长期',   # 身份证背面 信息 有效期间
    #          'valid_end': '长期',          # 身份证背面 隐藏信息 有效开始日
    #          'valid_start': '1978.04.25'   # 身份证背面 隐藏信息 有效截止日
    #          'birth_area_code': '430623'   # 身份证正面 隐藏信息 出生地址区域（身份证前六位、模拟人口迁移 20%概率）
    #          'front_stamp_loc': (367, 203) # 身份证正面 印章 印章位置（x,y)
    #          'front_stamp_size': (180, 50) # 身份证正面 印章 旋转后印章新尺寸
    #          'back_stamp_loc': (186, 574)  # 身份证背面 印章 印章位置（x,y)
    #          'back_stamp_size': (188, 90)  # 身份证背面 印章 旋转后印章新尺寸
    #
    #     train_source_image：不含印章的图片
    #     train_target_image：包含印章的图片
    #     '''
    #     person_info, train_source_image, train_target_image = maker.get_train_image()
    #
    #     elapsed = (time.clock() - start)
    #     # print(i, elapsed, person_info['name'], person_info['province'], person_info['id_code'])
    #     print(i, elapsed, person_info)
    #
    #     # person_info['front_new_loc']
    #     #
    #     # front_box = (person_info['front_new_loc'][0], person_info['front_new_loc'][1],\
    #     #        person_info['front_new_loc'][0] + person_info['front_new_size'][0], person_info['front_new_loc'][1] + person_info['front_new_size'][1])
    #     # front_roi = train_source_image.crop(front_box)
    #     # front_roi.save('c:/temp/front_roi.jpg')
    #     #
    #     # front_box = (person_info['back_new_loc'][0], person_info['back_new_loc'][1],\
    #     #        person_info['back_new_loc'][0] + person_info['back_new_size'][0], person_info['back_new_loc'][1] + person_info['back_new_size'][1])
    #     # front_roi = train_source_image.crop(front_box)
    #     # front_roi.save('c:/temp/back_roi.jpg')
    #
    #     # 正面
    #     front_img_512 = SaveSingleSide(train_target_image, person_info['front_new_loc'], person_info['front_new_size'])
    #     # 反面
    #     back_img_512 = SaveSingleSide(train_target_image, person_info['back_new_loc'], person_info['back_new_size'])
    #
    #     front_img_512.save('c:/temp/front_roi.jpg')
    #     back_img_512.save('c:/temp/back_roi.jpg')
    #     # # 保存图片（灰度图)
    #     train_source_image.save('c:/temp/test_source.jpg',quality=95)
    #     train_target_image.save('c:/temp/test_target.jpg',quality=95)

    # ----------多线程 测试（文件生成）----------
    # thread_01 = Thread(target=ThreadCardMaker,args=(25,"t01",))
    # thread_01.start()
    #
    # thread_02 = Thread(target=ThreadCardMaker,args=(25,"t02",))
    # thread_02.start()
    #
    # thread_03 = Thread(target=ThreadCardMaker,args=(25,"t03",))
    # thread_03.start()
    #
    # thread_04 = Thread(target=ThreadCardMaker,args=(25,"t04",))
    # thread_04.start()

