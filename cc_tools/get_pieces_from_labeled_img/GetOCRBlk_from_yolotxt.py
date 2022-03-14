# -*-coding：utf-8 -*-
import os
import time
import shutil
import numpy as np
import cv2
from math import *
from PIL import Image
from glob import glob

image_files = glob('./idcard_box/*.jpg')
save_img_dir = "crop_img"

def resize_im(im, scale, max_scale=None):
    f = float(scale) / min(im.shape[0], im.shape[1])
    if max_scale != None and f * max(im.shape[0], im.shape[1]) > max_scale:
         f = float(max_scale) / max(im.shape[0], im.shape[1])
    return cv2.resize(im, None, None, fx=f, fy=f, interpolation=cv2.INTER_LINEAR), f


def dumpRotateImage(img, degree, pt1, pt2, pt3, pt4):
    height, width = img.shape[:2]
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    matRotation = cv2.getRotationMatrix2D((width // 2, height // 2), degree, 1)
    matRotation[0, 2] += (widthNew - width) // 2
    matRotation[1, 2] += (heightNew - height) // 2
    imgRotation = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))
    pt1 = list(pt1)
    pt3 = list(pt3)

    [[pt1[0]], [pt1[1]]] = np.dot(matRotation, np.array([[pt1[0]], [pt1[1]], [1]]))
    [[pt3[0]], [pt3[1]]] = np.dot(matRotation, np.array([[pt3[0]], [pt3[1]], [1]]))
    ydim, xdim = imgRotation.shape[:2]
    imgOut = imgRotation[max(1, int(pt1[1])) : min(ydim - 1, int(pt3[1])), max(1, int(pt1[0])) : min(xdim - 1, int(pt3[0]))]

    return imgOut


if __name__ == '__main__':

    for image_file in sorted(image_files):
        #print(image_file)
        img = cv2.imread(image_file,1)
        xDim, yDim = img.shape[1], img.shape[0]

        txt_name = image_file.replace(".jpg",".txt")
        f = open(txt_name, "r")
        lines = f.readlines()
        f.close()

        img_name = image_file.split("\\")[-1]
        img_name = img_name.split('.')[0]
        #cur_dir = save_path + "/" + img_name
        if os.path.exists(save_img_dir) == False:
            os.mkdir(save_img_dir)


        for line in lines:
            loc = line.strip().split(":")[0]
            #print(loc)
            if len(loc) == 0:
                continue
            rec = loc.split(" ")

            x1 = np.clip(int(xDim*float(rec[1]) - xDim*float(rec[3])/2),1,xDim)
            x2 = np.clip(int(xDim * float(rec[1]) + xDim * float(rec[3])/2),1,xDim)
            y1 = np.clip(int(yDim * float(rec[2]) - yDim * float(rec[4])/2),1,yDim)
            y2 = np.clip(int(yDim * float(rec[2]) + yDim * float(rec[4])/2),1,yDim)
            crop = img[y1:y2,x1:x2]

            #pt1 = (max(1, int(rec[0])), max(1, int(rec[1])))
            #pt2 = (int(rec[2]), int(rec[3]))
            #pt3 = (min(int(rec[6]), xDim - 2), min(yDim - 2, int(rec[7])))
            #pt4 = (int(rec[4]), int(rec[5]))
            #degree = degrees(atan2(pt2[1] - pt1[1], pt2[0] - pt1[0]))  # 图像倾斜角度
            #partImg = dumpRotateImage(img, degree, pt1, pt2, pt3, pt4)
            #if crop.shape[0] < 1 or crop.shape[1] < 1 or crop.shape[0] > crop.shape[1]:  # 过滤异常图片
            #    continue
            
            #num += 1
            save_pth = save_img_dir + '/' + img_name + ".jpg"
            #save_pth = save_path + "/" + text + "@%s.jpg"%name
            print(save_pth)
            cv2.imwrite(save_pth, crop)