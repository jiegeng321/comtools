import math
import numpy as np
from PIL import Image, ImageStat
import os
import shutil
from tqdm import tqdm
def get_image_light_mean(dst_src):
    im = Image.open(dst_src).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]
import colorsys
def get_dominant_color(image):
#颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
#生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200, 200))
    max_score = 0
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        # 忽略高亮色
        if y > 0.9:
            continue
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color
input_dir = './notrequire'
output_dir = input_dir+'_black'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
dir_list = os.listdir(input_dir)
#a = []
for img in tqdm(dir_list):
    #a.append(get_image_light_mean(input_dir + '/' + img))
    #print(a[-1])
    #print(np.mean(get_dominant_color(Image.open(input_dir + '/' + img))))
#print(np.mean(a))
    if get_image_light_mean(input_dir+'/'+img)>8:
        #os.remove(input_dir+img)
        continue
    else:
        #os.remove(input_dir +'/'+ img)
        shutil.move(input_dir+'/'+img,output_dir)

