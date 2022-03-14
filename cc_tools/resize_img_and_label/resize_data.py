import os
import cv2

path = "blk"

files = os.listdir(path)


def CvtTxt(src_name, dst_name, rx, ry):
    f = open(src_name, "r")
    lines = f.readlines()
    f.close()
    locs = []
    for line in lines:
        line = line.strip().split(",")
        loc = line[0:8]
        loc = [float(v) for v in loc]
        loc[0] *= rx
        loc[2] *= rx
        loc[4] *= rx
        loc[6] *= rx
        loc[1] *= ry
        loc[3] *= ry
        loc[5] *= ry
        loc[7] *= ry               
        locs.append(loc)
    
    f = open(dst_name, "w")
    infos = []
    for loc in locs:
        tmp = "%d,%d,%d,%d,%d,%d,%d,%d,chinese,####\n"%(int(loc[0]),int(loc[1]),int(loc[2]),int(loc[3]),int(loc[4]),int(loc[5]),int(loc[6]),int(loc[7]))
        infos.append(tmp)
    f.writelines(infos)
    f.close()


save_path = "blk_resize"
if os.path.exists(save_path) == False:
    os.mkdir(save_path)

for file in files:
    if file.find(".jpg") != -1:
        name = path + "/" + file
        img = cv2.imread(name, 1)
        wd = img.shape[1]
        ht = img.shape[0]
        new_wd = 800
        new_ht = new_wd*ht/wd
        new_ht = int(new_ht)
        new_img = cv2.resize(img, (new_wd,new_ht))
        save_img = save_path + "/" + file
        cv2.imwrite(save_img, new_img)
        txt_name = name.replace(".jpg",".txt")
        rx = new_wd*1.0/wd
        ry = new_ht*1.0/ht
        save_txt = save_path + "/" + file.replace(".jpg", ".txt")
        CvtTxt(txt_name, save_txt, rx, ry)
