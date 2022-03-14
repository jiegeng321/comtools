from PIL import Image, ImageDraw, ImageFont,ImageFilter,ImageEnhance
import numpy as np
import random
import os
from tqdm import tqdm
import shutil
from glob import glob

image_folder='gen_data'
font_folder='gen_data/font/*'

font_list = glob(font_folder)

char_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','W','V','X','Y','Z']
num_list = ['0','1','2','3','4','5','6','7','8','9']
date_list = ['年','月','日']

def info_gen(num):

    card_info = {}
    card_info['char_num'] = [''.join([random.choice(char_list+num_list) for i in range(10)]) for j in range(num)]
    #card_info['date'] = [''.join([random.choice(date_list+num_list) for i in range(10)]) for j in range(num)]
    return card_info['char_num']

def indexing(standards,txt):
    res = []
    for i in range(len(txt)):
        res.append(standards.index(txt[i] + '\n') + 1)
    return res

def data_gen(txt_info):
   # save_path = 'cnocr_gen_data'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(save_path+'/img'):
        os.makedirs(save_path+'/img')
    else:
        shutil.rmtree(save_path+'/img')
        os.makedirs(save_path + '/img')
    f_st = open('gen_data/label_insurance.txt', 'r', encoding='utf-8-sig')
    f_tr2 = open(os.path.join(save_path, 'train.txt'), 'w', encoding='utf-8')
    f_ts2 = open(os.path.join(save_path, 'test.txt'), 'w', encoding='utf-8')
    train_items = txt_info
    standards = f_st.readlines()
    f_st.close()
    for i in tqdm(range(len(train_items))):
        txt = train_items[i]
        all = 1
        for t in txt:
            if (t+'\n') not in standards:
                all = 0
                break
        if all ==  0:
            continue
        char_len = 0
        num_len = 0
        date_len = 0
        for t in txt:
            if t in char_list:
                char_len += 1
            if t in num_list:
                num_len += 1
            if t in date_list:
                date_len += 1
        idxes = indexing(standards,txt)
        bg_color = random.randint(220, 255)

        len_total = 17*num_len + 17*char_len + 31*date_len
        target = Image.new('RGB', (len_total, 32), (bg_color, bg_color, bg_color))

        draw = ImageDraw.Draw(target)
        font_color = random.randint(80, 150)
        #if random.random() < 0.75:
        font_size = 31
        #else:
        #    font_size = random.randint(26, 30)
        #font = ImageFont.truetype(random.choice(font_list), font_size)
        font = ImageFont.truetype('./gen_data/font/simsun.ttc', font_size)

        loc = (4,-1)
        draw.text(loc, txt, (font_color,font_color,font_color),font=font)

        #if random.random()<0.75:
        #    random_angle = random.randint(-27, 27)/10
        #    target = target.rotate(random_angle, Image.BICUBIC, expand=1,fillcolor=(bg_color, bg_color, bg_color))

        if random.random() < 0.8:
            image_brightness_rate = random.randint(70, 120) / 100
            enh_col = ImageEnhance.Brightness(target)
            target = enh_col.enhance(image_brightness_rate)
        if random.random() < 0.3:
            target = target.filter(ImageFilter.GaussianBlur(radius=random.randint(20, 120) / 100))

        if random.random() < 0.5:

            target1 = np.array(target, dtype='int32')
            for j in range(random.randint(300,700)):
                x = random.randint(0, target.size[1]-1)
                y = random.randint(0, target.size[0]-1)
                ran = np.random.randint(-30, 30, (3))
                target1[x, y, :] += ran
            target = Image.fromarray(np.uint8(np.clip(target1, 0, 255)))
        if random.random() < 0.5:
            h_size = random.randint(15,26)
            w_size = int(h_size/target.size[1]*target.size[0])
            target = target.resize((w_size,h_size))


            target = target.resize((170, 32),resample=Image.BOX)

        cnt = "gen_data_%06d.jpg" % i
        target.save(os.path.join(save_path+'/img', cnt), quality=100)
        for idx in idxes:
            cnt = cnt + " {}".format(idx)
        if i%9==0:
            f_ts2.write(cnt + '\n')
        else:
            f_tr2.write(cnt + '\n')
    f_tr2.close()
    f_ts2.close()
if __name__ == '__main__':
    gen_num = 50
    save_path = './cnocr_gen_train_data_multifont_len10'
    data_list = info_gen(gen_num)
    data_gen(data_list)


    
    
    
    
    
    
    
    
    
