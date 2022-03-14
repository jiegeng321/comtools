#-*- coding:utf-8 -*-
import sys
import hashlib
import os
import time
import requests
import multiprocessing as mp
import cv2
import argparse
from pathlib import Path

#tupu 小红书100w数据分析
#图普暴恐分类模型输出label的对应关系
tupu_cls_label_map= {
                     '0':'正常',
                     '1':'特殊着装人物',
                     '2':'特殊符号',
                     '3':'武器或持武器',
                     '4':'血腥',
                     '5':'暴乱场景',
                     '6':'战争场景'
 }


def mkpath(out):
    if not out.exists():
        out.mkdir(parents=True)    


#imageIds;imageTerrorIdentifyResultId;imageTerrorIdentifyResultScore
#"[\"c230aea066e344e3b3ebc8224702f0b3\"]";0;0.9238560199737549


#图普的分类建立文件夹
def mkpath_tupu(out,tupu_cls_label_map,th):
    cls_chi = tupu_cls_label_map.values()
    for i in cls_chi:
        out_cls_chi_small_tmp = out + '/' + i + '/'+'small_'+ str(th)
        out_cls_chi_small = Path(out_cls_chi_small_tmp)
        out_cls_chi_big_tmp = out + '/' + i + '/'+'big_'+ str(th)
        out_cls_chi_big = Path(out_cls_chi_big_tmp)
        mkpath(out_cls_chi_small)
        mkpath(out_cls_chi_big)

#根据拉的csv统计 每类的数量
#imageid,cls,score
#异常处理 csv中会有很多无效的数据
def parse_csv_static(csv_path,out):
    files = open(csv_path,'r').readlines()
    label_cls_dict = {}
    for i in files[1:]:
        try:
            line = i.strip()
            imageid_tmp,eng_cls,score = line.split(';')
            imageid = imageid_tmp[4:-4]
            chi_cls = tupu_cls_label_map[eng_cls]
            if chi_cls not in label_cls_dict.keys():
                label_cls_dict[chi_cls] = []
                label_cls_dict[chi_cls].append(imageid)
                #print chi_cls,imageid,score
            else:
                label_cls_dict[chi_cls].append(imageid)
        except:
            print ("line",line)
            continue



#按类别存储,多线程加速，获取图片失败异常处理,分数+imageid
def parse_csv_multi(csv_path,out,num_process,th):
    mkpath_tupu(out,tupu_cls_label_map,th)
    files = open(csv_path,'r').readlines()
    pool = mp.Pool(processes = num_process)
    for i in files[1:]:
        try:
            line = i.strip()
            imageid_tmp,eng_cls,score_ori = line.split(';')
            score = round(float(score_ori),5)
            imageid = imageid_tmp[4:-4]
            chi_cls = tupu_cls_label_map[eng_cls]
            print ("score,imageid,chi_cls",chi_cls,imageid,score)
            res = pool.apply_async(download_single_save_score,args=(imageid,chi_cls,score,out,th))
        except:
            print ("Exception",line)
            continue 
    pool.close()
    pool.join()     


#type  score_imageid 按照type存放,图片名用score_imageid来保存
def  download_single_save_score(imageid,cls_chi,score,out,th):
    timestamp = int(round((time.time()+10*60)*1000))
    str_salt = str(timestamp) +"_"+ str(salt)
    m2 = hashlib.md5(str_salt.encode(encoding='utf-8'))
    token = m2.hexdigest()
    imageUrl = url.format(imageid,str(timestamp),token)
    try:
        img_out = ''
        resp = requests.get(imageUrl)
        if float(score) <= float(th):
            img_out = os.path.join(out+'/'+cls_chi+'/'+'small_'+str(th),str(score)+'_'+imageid + ".jpg")
        else:
            img_out = os.path.join(out+'/'+cls_chi+'/'+'big_'+str(th),str(score)+'_'+imageid + ".jpg")
        if len(resp.content)>100:
            print ("imgout",img_out)
            open(img_out,'wb').write(resp.content)
            print ("len_content",len(resp.content))
        else:
            resp = requests.get(imageUrl)
            if len(resp.content)>100:
                open(img_out,'wb').write(resp.content)
            else:
                print ("DOWNLOAD CONTENT_ERROR",imageid)
    except:
        print ("multi download error",imageid)    







if __name__ == '__main__':
    url  = "https://gleaner.tongdun.cn/resource/image?type=image_id&image_id={}&timestamp={}&token={}"
    salt = '7c8c01906b3faeaafebb0d6fc9296f08'
    
    #csv ["8de3835235b14a0193d87ef756709c65"],4,0.7241600751876831"
    parser =  argparse.ArgumentParser(description = "download_imageid_images")
    parser.add_argument("-l","--imageid_csv",type=str)
    parser.add_argument("-m_p","--multi_process",type=int)
    parser.add_argument("-th","--score_threshold",type=float)
    args = parser.parse_args()
    imglist = args.imageid_csv
    num_processes = args.multi_process
    th = args.score_threshold
    imgshow_dir = imglist +'.imshow'
    multi_down_start = time.time()
    #分类下载多线程保存
    parse_csv_multi(imglist,imgshow_dir,num_processes,th)
    
    multi_down_end = time.time()
    print ("total", multi_down_end-multi_down_start)
