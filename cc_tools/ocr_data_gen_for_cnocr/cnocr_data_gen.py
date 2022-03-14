from PIL import Image, ImageDraw, ImageFont,ImageFilter,ImageEnhance
import pandas as pd
import numpy as np
import random
import math
import uuid
import os
from tqdm import tqdm
import shutil

image_folder='gen_data'
word_css = "{0}/WeiRuanYaHei-1.ttf".format('gen_data')  # 默认字体
chinese_name = pd.read_csv('{0}/chinese_name.csv'.format(image_folder), encoding="gbk")
name_list = chinese_name.name.tolist()
del chinese_name

chinese_nationality = pd.read_csv('{0}/chinese_nationality.csv'.format(image_folder), encoding="gbk")
nationality_list = chinese_nationality.name.tolist()
del chinese_nationality

chinese_street = pd.read_csv('{0}/chineses_street.csv'.format(image_folder), encoding="utf8")
street_list = chinese_street.name.tolist()
del chinese_street

id_card_pd = pd.read_csv('{0}/id_card_code.csv'.format(image_folder), encoding="gbk", dtype={'code': str})
id_card_key = id_card_pd.code.values
id_card_dict = dict(zip(id_card_pd.code.values, id_card_pd.name.values))
del id_card_pd

birthday_year = [str(i) for i in list(range(1900, 2020))]
birthday_month = [str(i) for i in list(range(1, 13))]
birthday_day = [str(i) for i in list(range(1, 32))]

person_cod_list = [str(i) for i in list(range(1, 1000))]

id_code_check_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'X']

def info_gen():

    card_info = {}
    #card_info['uuid'] = uuid.uuid4().hex
    card_info['name'] = random.choice(name_list)
    #card_info['sex'] = random.choice(['男', '女'])
    #if random.random() < 0.3:
    #    card_info['nationality'] = random.choice(nationality_list)
    #else:
    #    card_info['nationality'] = '汉'
    card_info['birthday_y'] = random.choice(birthday_year)
    card_info['birthday_m'] = random.choice(birthday_month)
    card_info['birthday_d'] = random.choice(birthday_day)
    # 证件区域（身份证前六位，当前户籍地）
    card_info['area_code'] = random.choice(id_card_key)
    # 证件区域（原始户籍的身份证前六位，模拟人口迁移 20%）
    if random.random() < 0.2:
        card_info['birth_area_code'] = random.choice(id_card_key)
    else:
        card_info['birth_area_code'] = card_info['area_code']
    # 住址（随机生成住址）
    #card_info['addr'] = id_card_dict[card_info['area_code']] + random.choice(street_list)
    card_info['id_code'] = card_info['birth_area_code'] + str(card_info['birthday_y']) + card_info[
        'birthday_m'].zfill(2) + card_info['birthday_d'].zfill(2) \
                           + random.choice(person_cod_list).zfill(3) + random.choice(id_code_check_list)
    #card_info['valid_start'] = str(
     #   random.choice(birthday_year[int(card_info['birthday_y']) - 1900:])) \
     #                          + "." + random.choice(birthday_month).zfill(2) \
     #                          + "." + random.choice(birthday_day).zfill(2)
    #card_info['valid_end'] = str(random.choice(birthday_year[int(card_info['valid_start'][:4]) - 1900:])) + \
    #                         card_info['valid_start'][4:]
    #card_info['valid'] = card_info['valid_start'] + "-" + card_info['valid_end']
    return card_info

def indexing(standards,txt):
    res = []
    for i in range(len(txt)):
        res.append(standards.index(txt[i] + '\n') + 1)
    return res

def data_gen(txt_info):
    pth = 'cnocr_gen_data'
    if not os.path.exists(pth):
        os.makedirs(pth)
    if not os.path.exists(pth+'/img'):
        os.makedirs(pth+'/img')
    else:
        shutil.rmtree(pth+'/img')
        os.makedirs(pth + '/img')
    f_st = open('gen_data/label_cn.txt', 'r', encoding='utf-8-sig')
    f_tr2 = open(os.path.join(pth, 'train.txt'), 'w', encoding='utf-8')
    f_ts2 = open(os.path.join(pth, 'test.txt'), 'w', encoding='utf-8')
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
        idxes = indexing(standards,txt)
        bg_color = random.randint(200, 255)
        if len(txt)>5:
            target = Image.new('RGB', (20*len(txt), 32), (bg_color, bg_color, bg_color))
            loc = (4,-4)
        else:
            target = Image.new('RGB', (36 * len(txt), 32), (bg_color, bg_color, bg_color))
            loc = (4,-6)
        draw = ImageDraw.Draw(target)
        font_color = random.randint(80, 150)
        font = ImageFont.truetype(word_css, 32)
        draw.text(loc, txt, (font_color,font_color,font_color),font=font)
        image_brightness_rate = random.randint(70, 120) / 100
        enh_col = ImageEnhance.Brightness(target)
        target = enh_col.enhance(image_brightness_rate)
        target = target.filter(ImageFilter.GaussianBlur(radius=random.randint(20, 120) / 100))
        cnt = "gen_data_%06d.jpg" % i
        target.save(os.path.join(pth+'/img', cnt), quality=100)
        for idx in idxes:
            cnt = cnt + " {}".format(idx)
        if i%10==0:
            f_ts2.write(cnt + '\n')
        else:
            f_tr2.write(cnt + '\n')
    f_tr2.close()
    f_ts2.close()
if __name__ == '__main__':
    info_list = []
    gen_num = 10
    for i in tqdm(range(gen_num)):
        card = info_gen()
        info_list.append(card['name'])
        info_list.append(card['id_code'])
    data_gen(info_list)

    
    
    
    
    
    
    
    
    