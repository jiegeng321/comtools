# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:27:06 2020

@author: Administrator
"""

import os
from tqdm import tqdm

big = './big'
small = './small'

def delete_unlabeled_image(big,small):
    big_list = os.listdir(big)
    small_list = os.listdir(small)
    del_num = 0
    for i in tqdm(range(len(big_list))):
        if  not os.path.exists(small + '/'+big_list[i].split('.')[0] + '.' + small_list[0].split('.')[-1]):
            os.remove(big + '/'+big_list[i])
            print(big + '/'+big_list[i]+'is deleted')
            del_num+=1
    print('%d unlabeled images are deleted done'%del_num)
delete_unlabeled_image(big,small)





































































