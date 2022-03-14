from PIL import Image, ImageDraw, ImageFont,ImageFilter,ImageEnhance
import numpy as np
import random
import os
from tqdm import tqdm
import shutil
from glob import glob
def indexing(standards,txt):
    res = []
    for i in range(len(txt)):
        res.append(standards.index(txt[i] + '\n') + 1)
    return res

train_list_path = 'insurance_ocr_train_data_cnocr/insurance_train_data_paddle.txt'
dict_path = 'insurance_ocr_train_data_cnocr/dict_list.txt'
save_cnocr_path = 'insurance_ocr_train_data_cnocr'

f_dict = open(dict_path, 'r', encoding='utf-8')
f_paddle_label = open(train_list_path, 'r', encoding='utf-8')
f_cnocr_label = open(os.path.join(save_cnocr_path, 'train.txt'), 'w', encoding='utf-8')
standards = f_dict.readlines()
paddle_label = f_paddle_label.readlines()
for line in tqdm(paddle_label):
    print(line.split('\t')[-1].strip('\n'))
    index = indexing(standards,line.split('\t')[-1].strip('\n'))
    cn_line = ''
    for i in index:
        cn_line += str(i)+ ' '
    cn_line.split(' ')
    cn_line = line.split('\t')[0] + ' ' + cn_line + '\n'
    f_cnocr_label.write(cn_line)
f_dict.close()
f_paddle_label.close()
f_cnocr_label.close()


    
    
    
    
    
    
    
    
    
