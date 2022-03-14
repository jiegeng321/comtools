#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""
#

import os
import numpy as np
from pathlib import Path

#图片级分析品牌数量分布，图片中某品牌出现次数最多的作为该图片的品牌
names = ['dior-w-1', 'golden goose-1', 'coach-w-1', 'fendi-1', 'balenciaga-w-1', 'prada-w-1', 'ck-2', 'ysl-w-1', 'ysl-1', 'lv-2', 'lv-1', 'versace-w-1', 'versace-1', 'fendi-w-1', 'dolce-1', 'Givenchy-w-1', 'the north face-1', 'dior-w-2', 'golden goose-2', 'chanel-2', 'chanel-1', 'dolce-w-3', 'dolce-w-2', 'nike-1', 'nike-w-1', 'off-white-w-1', 'burberry-w-1', 'supreme-1', 'gucci-3', 'dsquared2-w-1', 'burberry-1', 'gucci-2', 'ck-1', 'armani-1', 'Michael Kors-1', 'burberry-2', 'Kenzo-1', 'Givenchy-1', 'Hermes-w-1', 'fendi-2', 'Hermes-2', 'Hermes-1', 'Michael Kors-w-1', 'nike-6', 'dior-1', 'Moncler-1', 'Moncler-2', 'off-white-1', 'balenciaga-1', 'Moncler-w-1', 'supreme-2', 'armani-w-1', 'armani-w-2', 'dior-2', 'gucci-1', 'dolce-3', 'the north face-w-1', 'nike-2', 'ck-3', 'dsquared2-w-2', 'nike-5', 'armani-2', 'nike-3', 'dolce-2', 'nike-8', 'nike-4']
src_dir = "/gpudata/erwei.wang/datasets/logoBrand/LogoOwn/logo_1_0123/JPEGImages/train/images"
src_dir = Path(src_dir)
label_dir = src_dir.parent / "labels"
brand_res = {i.split('-')[0]:0 for i in names}
print(brand_res)


img_files = os.listdir(src_dir)
for img in img_files:
    postfix = os.path.splitext(img)[-1]
    lens = len(postfix)
    imglen = len(img)
    label_path = os.path.join(label_dir, img[:imglen-lens]+'.txt')
    try:
        txt = np.loadtxt(label_path).reshape(-1, 5)
    except:
        txt = np.array([])
    if txt.shape[0] == 0:
        continue
    res = list(txt[:, 0].astype(int))
    index = max(res, key=res.count)
    # res = np.bincount(txt[:, 0].astype(int))
    # index = np.argmax(res)
    brand_res[names[index].split('-')[0]] += 1

brand_res = dict(sorted(brand_res.items()))
print(brand_res)


#{'Givenchy': 241, 'Hermes': 254, 'Kenzo': 283, 'Michael Kors': 185, 'Moncler': 156, 'armani': 173, 'balenciaga': 588, 'burberry': 283, 'chanel': 433, 'ck': 228, 'coach': 177, 'dior': 406, 'dolce': 302, 'dsquared2': 36, 'fendi': 395, 'golden goose': 466, 'gucci': 322, 'lv': 399, 'nike': 401, 'off': 194, 'prada': 279, 'supreme': 132, 'the north face': 293, 'versace': 452, 'ysl': 370}






