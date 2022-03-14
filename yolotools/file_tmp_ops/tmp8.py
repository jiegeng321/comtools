#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from pathlib import Path
from comfunc.funcxml import readxml
import cv2
import random
from comfunc.print_color import bcolors
import os
import shutil
from comfunc.check import check_dir
from comfunc.tools import is_img
from comfunc.tools import check_dir
from tqdm import tqdm
src_dir = "/data01/xu.fx/dataset/LOGO_DATASET/comb_data/checked"

select_out_list = ['miffy', 'baby_shark', 'victorias_secret', '511_tactical', 'tous', 'fendi', 'fc_bayern_munchen', 'michael_kors', 'dc_shoes', 'gucci', 'roger_vivier', 'giuseppe_zanotti', 'louis_vuitton', 'palace', 'burberry', 'reebok', 'salomon', 'asics', 'vans', 'batman', 'salvatore_ferragamo', 'bottega_veneta', 'maserati', 'paul_frank', 'patek_philippe', 'versace', 'hello_kitty', 'chopard', 'lamborghini', 'dragon_ball', 'alexander_mcqueen', 'pinko', 'land_rover', 'stussy', 'franck_muller', 'mercedes_benz', 'porsche', 'honda', 'palm_angels', 'balenciaga', 'hermes', 'chrome_hearts', 'evisu', 'marvel', 'vlone', 'tottenham_hotspur', 'pandora', 'ugg', 'bentley', 'bmw', 'swarovski', 'balmain', 'tissot', 'monster_energy', 'armani', 'new_balance', 'mlb', 'cartier', 'bvlgari', 'amiri', 'coach', 'citizen', 'marc_jacobs', 'chanel', 'tods', 'comme_des_garcons', 'moncler', 'philipp_plein', 'chevrolet', 'zenith', 'bally', 'longines', 'franco_moschino', 'timberland', 'pokemon', 'apple', 'fossil', 'paul_shark', 'vacheron_constantin', 'harley_davidson', 'miu_miu', 'omega', 'fila', 'givenchy', 'calvin_klein', 'new_era', 'manolo_blahnik', 'los_angeles_dodgers', 'liverpool_fc', 'valentino_garavani', 'converse', 'under_armour', 'daniel_wellington', 'the_rolling_stones', 'red_bull', 'chaumet', 'guess', 'kappa', 'jimmy_choo', 'bosch', 'mcm', 'piaget', 'christian_louboutin', 'nfl', 'mizuno', 'rolex']
select_out_list2 = [i.replace("_","") for i in select_out_list]
dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/logo_data_check"

#select_out_folder = os.listdir(select_out_dir)
for file in tqdm(os.listdir(src_dir)):
    if file.split("_")[0].lower() in select_out_list2:
        if not os.path.exists(os.path.join(dst_dir,file.split("_")[0])):
            os.makedirs(os.path.join(dst_dir,file.split("_")[0]))
        shutil.copy(os.path.join(src_dir, file), os.path.join(dst_dir,file.split("_")[0],file))

image_list = [p for p in Path(image_dir).rglob('*.*')]