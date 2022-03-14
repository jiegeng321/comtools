import pandas as pd
import os
import requests
import time
from tqdm import tqdm
import shutil
img_dir = "face_pts_prelabel_2nd/face_pts_img_3rd"
spilt_dir = "face_pts_prelabel"
each_folder = 1000

folder_total = img_dir+"_spilt"
img_list = os.listdir(img_dir)
num_folder = len(img_list)//each_folder
img_list = sorted(img_list)
for i in tqdm(range(num_folder)):
    folder_name = folder_total+"/"+spilt_dir+"_part"+str(i)
    os.makedirs(folder_name)
    for j in range(each_folder):
        shutil.copy(img_dir + '/' + img_list[i*each_folder+j], folder_name)
