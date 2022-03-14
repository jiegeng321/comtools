import os
import cv2

path = "blk_resize"
save_path = "show"
if os.path.exists(save_path) == False:
    os.mkdir(save_path)

files = os.listdir(path)

for file in files:
    name = path + "/" + file
    if name.find(".jpg") != -1:
        img = cv2.imread(name, 1)
        txt_name = name.replace(".jpg",".txt")
        f = open(txt_name, "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.strip().split(",")
            locs = line[0:8]
            locs = [int(v) for v in locs]
            cv2.line(img, (locs[0],locs[1]), (locs[2],locs[3]), (0,255,0), 1)
            cv2.line(img, (locs[2],locs[3]), (locs[4],locs[5]), (0,255,0), 1)
            cv2.line(img, (locs[4],locs[5]), (locs[6],locs[7]), (0,255,0), 1)
            cv2.line(img, (locs[6],locs[7]), (locs[0],locs[1]), (0,255,0), 1)
            save_name = save_path + "/" + file
            cv2.imwrite(save_name, img)
            
