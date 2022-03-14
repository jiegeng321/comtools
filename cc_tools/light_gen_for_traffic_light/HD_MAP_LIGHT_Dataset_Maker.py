from PIL import Image, ImageDraw, ImageFont,ImageFilter,ImageEnhance
import pandas as pd
import numpy as np
import random
import math
import uuid
import os
bg_dir = './gen_data/bg_frames/'
light_dir = './gen_data/light_1_kinds/'
is_not_light_dir = './gen_data/is_not_light/'
enhance = random.randint(9, 14)/10
noise_max = 30
fr_img_num = (6,12)
is_not_light_num = (6,12)
RESIZE_MIN_PIC = (100,400)
OUTPUT_SIZE = (1920,1080)

light_kind_list= os.listdir(light_dir)
is_not_light_list= os.listdir(is_not_light_dir)
bg_dir_list = os.listdir(bg_dir)
def min_size():
    size_all = []
    for mid_dir in light_kind_list:
        light_last_list = os.listdir(light_dir+mid_dir)
        for last_dir in light_last_list:
            img = Image.open(light_dir+mid_dir+'/'+last_dir)
            size_all.append(min(img.size[0],img.size[1]))
    return min(size_all)
MIN_SIZE = min_size()
def enhance_lab(img):
    ran_index = random.randint(0, 19)
    if ran_index==0 or ran_index==12 or ran_index==16:
        ran = enhance
        img = ImageEnhance.Color(img).enhance(ran)
    elif ran_index==1 or ran_index==13 or ran_index==17:
        ran = enhance
        img = ImageEnhance.Contrast(img).enhance(ran)
    elif ran_index==2 or ran_index==14 or ran_index==18:
        ran = enhance
        img = ImageEnhance.Brightness(img).enhance(ran)
    elif ran_index==3 or ran_index==15 or ran_index==19:
        ran = enhance
        img = ImageEnhance.Sharpness(img).enhance(ran)
    elif ran_index == 4:
        ran = np.random.randint(1,noise_max,(img.size[1],img.size[0],3))
        img = np.array(img, dtype='int32')
        img[:,:,:] += ran
        img = Image.fromarray(np.uint8(np.clip(img,0,255)))
    elif ran_index == 5:
        ran = np.random.randint(1,noise_max,(img.size[1],img.size[0],3))
        img = np.array(img, dtype='int32')
        img[:,:,:] += ran
        img = Image.fromarray(np.uint8(np.clip(img,0,255)))
    elif ran_index == 6:
        ran = np.random.randint(1,noise_max,(img.size[1],img.size[0]))
        img = np.array(img, dtype='int32')
        img[:,:,0] += ran
        img = Image.fromarray(np.uint8(np.clip(img,0,255)))
    elif ran_index == 7:
        ran = np.random.randint(1,noise_max,(img.size[1],img.size[0]))
        img = np.array(img, dtype='int32')
        img[:,:,1] += ran
        img = Image.fromarray(np.uint8(np.clip(img,0,255)))
    elif ran_index == 8:
        ran = np.random.randint(1,noise_max,(img.size[1],img.size[0]))
        img = np.array(img, dtype='int32')
        img[:,:,2] += ran
        img = Image.fromarray(np.uint8(np.clip(img,0,255)))
    elif ran_index == 9:
        ran = np.random.randint(1,noise_max)
        img = np.array(img, dtype='int32')
        img[:,:,0] += ran-int(noise_max/2)
        img = Image.fromarray(np.uint8(np.clip(img,0,255)))
    elif ran_index == 10:
        ran = np.random.randint(1,noise_max)
        img = np.array(img, dtype='int32')
        img[:,:,1] += ran-int(noise_max/2)
        img = Image.fromarray(np.uint8(np.clip(img,0,255)))
    elif ran_index == 11:
        ran = np.random.randint(1,noise_max)
        img = np.array(img, dtype='int32')
        img[:,:,2] += ran-int(noise_max/2)
        img = Image.fromarray(np.uint8(np.clip(img,0,255)))
    return img
def bg_img_gen(exten=True,rot=True):
    ran_index = random.randint(0,len(bg_dir_list)-1)
    bg_img = Image.open(bg_dir+bg_dir_list[ran_index])
    if exten:
        if random.random()<0.45:            
            bg_img = bg_img.resize((bg_img.size[0]*2,bg_img.size[1]*2))
    if bg_img.size[0]>OUTPUT_SIZE[0] and bg_img.size[1]>OUTPUT_SIZE[1]:
        random_index_x = random.randint(0, bg_img.size[0] - OUTPUT_SIZE[0])
        random_index_y = random.randint(0, bg_img.size[1] - OUTPUT_SIZE[1])
        box = (random_index_x,random_index_y,random_index_x+OUTPUT_SIZE[0],random_index_y+OUTPUT_SIZE[1])
        bg_img = bg_img.crop(box)
    elif bg_img.size[0]<OUTPUT_SIZE[0] and bg_img.size[1]<OUTPUT_SIZE[1]:
        bg_img = bg_img.resize([OUTPUT_SIZE[0],OUTPUT_SIZE[1]])
    if rot:
        if random.random()<0.4: 
            ran_rot = random.randint(-10,10)
            bg_img = bg_img.rotate(ran_rot, expand=False,resample=Image.BICUBIC)
            bg_img = bg_img.resize((int(bg_img.size[0] * 1.2), int(bg_img.size[1] * 1.2)))
            x = int((bg_img.size[0] - OUTPUT_SIZE[0]) / 2)
            y = int((bg_img.size[1] - OUTPUT_SIZE[1]) / 2)
            bg_img = bg_img.crop((x, y, x + OUTPUT_SIZE[0], y + OUTPUT_SIZE[1]))
    return bg_img
def fr_img_gen(min_num,max_num):
    num = random.randint(min_num,max_num)
    return_list = []
    label_name = []
    for i in range(num):
        mid_dir = light_kind_list[random.randint(0,len(light_kind_list)-1)]
        light_last_list = os.listdir(light_dir+mid_dir)
        last_path = light_last_list[random.randint(0,len(light_last_list)-1)]
        return_list.append(light_dir+mid_dir+'/'+last_path)
        label_name.append(mid_dir)
    return return_list,label_name
def is_not_light_gen(min_num,max_num):
    num = random.randint(min_num,max_num)
    return_list = []
    for i in range(num):
        last_path = is_not_light_list[random.randint(0,len(is_not_light_list)-1)]
        return_list.append(is_not_light_dir+'/'+last_path)
    return return_list
#def draw_line(draw,num)
LINE_COLOR = []
def data_maker():

    brightness_rate_bg = random.randint(65, 115) / 100
    #ran_index = random.randint(0,len(bg_dir_list)-1)
    #bg_img = Image.open(bg_dir+bg_dir_list[ran_index])
    bg_img = bg_img_gen(exten=False,rot=False)
    fr_img_path_list,label_name = fr_img_gen(fr_img_num[0],fr_img_num[1])
    is_not_light_path_list = is_not_light_gen(is_not_light_num[0], is_not_light_num[1])
    is_not_light_list = []
    fr_img_list = []
    alpha_list = []
    for not_light in is_not_light_path_list:
        is_not_light_img = Image.open(not_light).convert("RGBA")
        min_size = min(is_not_light_img.size[0],is_not_light_img.size[1])
        RESIZE_MIN_PIC_not = [90,230]
        times = min_size/MIN_SIZE
        resize_rate = random.randint(int(RESIZE_MIN_PIC_not[0]/times), int(RESIZE_MIN_PIC_not[1]/times)) / 100
        is_not_light_img = is_not_light_img.resize((int(is_not_light_img.size[0]*resize_rate),int(is_not_light_img.size[1]*resize_rate)),resample=Image.BICUBIC)
        is_not_light_list.append(is_not_light_img)
    for fr_img in fr_img_path_list:
        fr_img = Image.open(fr_img).convert("RGBA")
        #fr_img = fr_img.resize(MAX_SIZE)
        if random.random() < 0.65:
            min_size = min(fr_img.size[0],fr_img.size[1])
            times = min_size/MIN_SIZE
            resize_rate = random.randint(int(RESIZE_MIN_PIC[0]/times), int(RESIZE_MIN_PIC[1]/times)) / 100
            fr_img = fr_img.resize((int(fr_img.size[0]*resize_rate),int(fr_img.size[1]*resize_rate)),resample=Image.BICUBIC)
        if random.random()<0.0:
            draw = ImageDraw.Draw(fr_img)
            min_size = min(fr_img.size[0],fr_img.size[1])            
            for i in range(random.randint(1,3)):
                draw_line_point = (random.randint(0,fr_img.size[0]),random.randint(0,fr_img.size[1]),random.randint(0,fr_img.size[0]),random.randint(0,fr_img.size[1]))
                draw.line(draw_line_point,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)),width=random.randint(1,max(1,round(min_size/10))))
        
        alpha_list.append(fr_img.split()[-1])
        

        fr_img = fr_img.convert('RGB')
        if random.random() < 0.6:
            fr_img = enhance_lab(fr_img)

        gaussian_blur_radius_fr = 0
        if random.random() < 0.3:
            gaussian_blur_radius_fr = random.randint(80, 120) / 100
        fr_img = fr_img.filter(ImageFilter.GaussianBlur(radius=gaussian_blur_radius_fr))

        fr_img_list.append(fr_img)

    #draw = ImageDraw.Draw(bg_img)
    def check_superposition(point1,point2):
        p1_x1,p1_y1,p1_x2,p1_y2 = point1
        p2_x1,p2_y1,p2_x2,p2_y2 = point2
        w1 = p1_x2-p1_x1
        h1 = p1_y2-p1_y1
        w2 = p2_x2 - p2_x1
        h2 = p2_y2 - p2_y1
        def bb_overlab(x1, y1, w1, h1, x2, y2, w2, h2):
            if (x1 > x2 + w2):
                return True
            if (y1 > y2 + h2):
                return True
            if (x1 + w1 < x2):
                return True
            if (y1 + h1 < y2):
                return True
            return False
        return bb_overlab(p1_x1,p1_y1,w1,h1,p2_x1,p2_y1,w2,h2)
    point_list = []
    for i,fr_img in enumerate(fr_img_list):
        if i==0:
            rand_x = random.randint(5,bg_img.size[0]-fr_img.size[0])
            rand_y = random.randint(5,bg_img.size[1]-fr_img.size[1]-int(bg_img.size[1]*0.3))
            point_list.append((rand_x,rand_y,rand_x+fr_img.size[0],rand_y+fr_img.size[1] ))
        else:
            while True:
                rand_x = random.randint(5, bg_img.size[0] - fr_img.size[0])
                rand_y = random.randint(5, bg_img.size[1] - fr_img.size[1] - int(bg_img.size[1] * 0.3))
                new_point = (rand_x, rand_y, rand_x + fr_img.size[0], rand_y + fr_img.size[1])
                check_ok = 0
                for old_point in point_list:
                    if check_superposition(new_point,old_point):
                        check_ok+=1
                        continue
                    else:
                        break
                if check_ok == len(point_list):
                    point_list.append(new_point)
                    break
    old_point_list = [] + point_list
    is_not_light_point_list = []
    for i,is_not_light_img in enumerate(is_not_light_list):
        while True:
            rand_x = random.randint(5, bg_img.size[0] - is_not_light_img.size[0])
            rand_y = random.randint(5, bg_img.size[1] - is_not_light_img.size[1] - int(bg_img.size[1] * 0.3))
            new_point = (rand_x, rand_y, rand_x + is_not_light_img.size[0], rand_y + is_not_light_img.size[1])
            check_ok = 0
            for old_point in old_point_list:
                if check_superposition(new_point,old_point):
                    check_ok+=1
                    continue
                else:
                    break
            if check_ok == len(old_point_list):
                old_point_list.append(new_point)
                is_not_light_point_list.append(new_point)
                break
    def draw_box(point,add):
        return (point[0]-random.randint(1,add),point[1]-random.randint(1,add),point[2]+random.randint(1,add),point[3]+random.randint(1,add))
    box_list = []
    for i, not_point in enumerate(is_not_light_point_list):
        bg_img.paste(is_not_light_list[i], not_point)
    for j, point in enumerate(point_list):
        bg_img.paste(fr_img_list[j], point,mask=alpha_list[j])
        box = draw_box(point,4)
        box_list.append(box)
    def txt_label(box_list,name_list):
        label_str = ''
        for i,box in enumerate(box_list):
            label_str+=name_list[i]
            for point in box:
                label_str += ','
                label_str += str(point)
            label_str += '\n'
        return label_str
    label = txt_label(box_list,label_name)
    gaussian_blur_radius_bg = 0
    if random.random() < 0.2:
        gaussian_blur_radius_bg = random.randint(60, 120) / 100
    #bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=gaussian_blur_radius_bg))
    bg_img = bg_img.convert('RGB').point(lambda p: p * brightness_rate_bg)

    return bg_img,label,uuid.uuid4().hex

