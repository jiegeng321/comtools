# -*- coding: utf-8 -*-
"""
@author: chineseocr
"""
import cv2, os
import numpy as np

from PIL import Image, ImageDraw
from glob import glob
from tqdm import tqdm
#pic = './card_type_img/2639.jpg'
img_path = 'image_resize/*.jpg'
txt_path = 'label_resize'
draw_save_path = img_path.split('/')[0]+'_draw'
txt_save_path = draw_save_path
if not os.path.exists(draw_save_path):
    os.makedirs(draw_save_path)
imgs = glob(img_path)
for pic in tqdm(imgs[:]):
    im = Image.open(pic)

    draw = ImageDraw.Draw(im)
    
    with open(txt_path+'/'+ pic.split('\\')[-1].split('.')[0]+'.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            splitted_line = line.strip().lower().split()
            x1, y1, x2, y2 = int(float(splitted_line[1]) + 1), int(float(splitted_line[2]) + 1), \
            int(float(splitted_line[3]) + 1), int(float(splitted_line[4]) + 1)
            draw.rectangle((int(x1),int(y1),int(x2),int(y2)), fill=None, outline='red', width=2)
            #draw.polygon([(int(line['box'][0]),int(line['box'][1])),(int(line['box'][2]),int(line['box'][3])),(int(line['box'][4]),int(line['box'][5])),(int(line['box'][6]),int(line['box'][7]))], fill=None, outline='red')
            #f.write(line['text']+'\n')
            #print(line['text']) 
    im.save(os.path.join(draw_save_path,pic.split('\\')[-1].split('.')[0]+'.jpg'), quality=100)
