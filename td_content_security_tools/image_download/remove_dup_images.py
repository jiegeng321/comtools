# -*- coding: utf-8 -*-

import hashlib
import os, shutil
import os
import glob
import sys


def md5_value(pics_fullpath):
    with open (pics_fullpath, 'rb') as a:
        md = hashlib.md5(a.read()).hexdigest()
    return md

# 在img_path中删除重复的图片
def rm_infile_same_md5(img_path):
    fix_dir = os.walk(img_path)
    x = []
    for path, d, file in fix_dir:
        for pics in file:
           if md5_value(os.path.join(path, pics)) in x:
               os.remove(os.path.join(path, pics))
               print ("RM_PICS",pics)
           else:
               x.append(md5_value(os.path.join(path, pics)))


if __name__ == '__main__':
    img_dir = sys.argv[1]
    rm_infile_same_md5(img_dir)




