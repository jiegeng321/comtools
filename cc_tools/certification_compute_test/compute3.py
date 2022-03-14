import numpy as np
import os
import json
import io
import PIL.Image
from tqdm import tqdm
import shutil
#import Levenshtein
import pandas as pd
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
#diff_path = 'compare_with_ten_files_compute/total_for_compute'

label_path = './card_cert_test_label'
list_path_real = os.listdir(label_path)

for i in tqdm(range(0, len(list_path_real))):
    path_real = os.path.join(label_path, list_path_real[i])
    #path_our = os.path.join(predict_path, list_path_our[i])
    with open(path_real,'r',encoding='utf-8') as f_r:
        #print(path_real)
        lines_r = f_r.readlines()
        lines_r += '发证日期：'
    with open(path_real,'w',encoding='utf-8') as f_p:
        f_p.writelines(lines_r)

