import cv2
import os

path = "image_total"
save_path = "blk"
if os.path.exists(save_path) == False:
	os.mkdir(save_path)
	
files = os.listdir(path)

def FindRect(locs):
	all_minx = []
	all_miny = []
	all_maxx = []
	all_maxy = []
	
	for loc in locs:
		minx = min(loc[0],loc[2],loc[4],loc[6])
		miny = min(loc[1],loc[3],loc[5],loc[7])
		maxx = max(loc[0],loc[2],loc[4],loc[6])
		maxy = max(loc[1],loc[3],loc[5],loc[7])
		all_minx.append(minx)
		all_miny.append(miny)
		all_maxx.append(maxx)
		all_maxy.append(maxy)
	
	left = min(all_minx)
	top = min(all_miny)
	right = max(all_maxx)
	bot = max(all_maxy)
	
	return left,top,right,bot
		
def Merge(left,top,right,bot,img_wd,img_ht):
	cx = (left + right)/2
	cy = (top + bot)/2
	new_wd = (right - left)*1.1
	new_ht = (bot - top)*1.2
	
	new_left = int(cx - new_wd/2)
	new_top = int(cy - new_ht/2)
	new_right = int(cx + new_wd/2)
	new_bot = int(cy + new_ht/2)
	
	if new_left < 0:
		new_left = 0
	if new_top < 0:
		new_top = 0
	if new_right > img_wd - 1:
		new_right = img_wd - 1
	if new_bot > img_ht - 1:
		new_bot = img_ht - 1
		
	return new_left,new_top,new_right,new_bot
	
def CvtTxt(src_name, dst_name, left, top):
	f = open(src_name, "r")
	lines = f.readlines()
	f.close()
	locs = []
	for line in lines:
		line = line.strip().split(",")
		loc = line[0:8]
		loc = [float(v) for v in loc]
		loc[0] -= left
		loc[2] -= left
		loc[4] -= left
		loc[6] -= left		
		loc[1] -= top
		loc[3] -= top
		loc[5] -= top
		loc[7] -= top				
		locs.append(loc)
	
	f = open(dst_name, "w")
	infos = []
	for loc in locs:
		tmp = "%d,%d,%d,%d,%d,%d,%d,%d,chinese,####\n"%(int(loc[0]),int(loc[1]),int(loc[2]),int(loc[3]),int(loc[4]),int(loc[5]),int(loc[6]),int(loc[7]))
		infos.append(tmp)
	f.writelines(infos)
	f.close()
	

for file in files:
    name = path + "/" +file
    if name.find(".jpg") != -1:
        print(name)
        img = cv2.imread(name, 1)
        img_wd = img.shape[1]
        img_ht = img.shape[0]
        txt_name = name.replace(".jpg", ".txt")
        f = open(txt_name, "r")
        lines = f.readlines()
        f.close()
        locs = []
        for line in lines:
            line = line.strip().split(",")
            loc = line[0:8]
            loc = [float(v) for v in loc]
            locs.append(loc)
		#print(locs)
        left,top,right,bot = FindRect(locs)
        wd = right - left + 1
        left -= wd
        if left < 0:
            left = 0
        left,top,right,bot = Merge(left,top,right,bot,img_wd,img_ht)
        dst = img[top:bot,left:right,:]
        save_name = save_path + "/" + file
        cv2.imwrite(save_name, dst)
        save_txt = save_name.replace(".jpg",".txt")
        CvtTxt(txt_name,save_txt,left,top)
