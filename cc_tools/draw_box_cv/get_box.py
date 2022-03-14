import os
import cv2
from tqdm import tqdm
import numpy as np
img_path = "3"
txt_path = "face_out3"
save_path = "face_pts_img_3rd"
if os.path.exists(save_path) == False:
    os.mkdir(save_path)

files = os.listdir(txt_path)

for file in tqdm(files[:]):
    name = txt_path + "/" + file
    img_name = img_path + "/" + file.replace(".txt",".jpg")
    if os.path.exists(img_name):
        img = cv2.imread(img_name, 1)
        f = open(name, "r")
        line = f.readline()
        f.close()
        line = [int(i) for i in line.strip().split(" ")]
        w = line[2]-line[0]
        h = line[3]-line[1]
        #print(img.shape)
        y1 = np.clip(int(line[1]-w*0.15),0,img.shape[0])
        y2 = line[3]
        x1 = np.clip(int(line[0]-h*0.15),0,img.shape[1])
        x2 = np.clip(int(line[2]+h*0.15),0,img.shape[1])
        img = img[y1:y2,x1:x2]
        save_name = save_path + "/" + file.replace(".txt",".jpg")
        cv2.imwrite(save_name, img)


            
