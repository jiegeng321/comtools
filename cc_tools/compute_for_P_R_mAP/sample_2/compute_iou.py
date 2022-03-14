import _init_paths
from BoundingBox import BoundingBox
from BoundingBoxes import BoundingBoxes
from Evaluator import *
from utils import *
import numpy as np
import warnings
warnings.filterwarnings("ignore")

eva = Evaluator()
import glob
import os
# Read ground truths
GT_ALL = []
currentPath = os.path.dirname(os.path.abspath(__file__))
folderGT = os.path.join(currentPath, 'groundtruths')
os.chdir(folderGT)
files = glob.glob("*.txt")
files.sort()
allBoundingBoxes = BoundingBoxes()
for f in files:
    nameOfImage = f.replace(".txt", "")
    fh1 = open(f, "r")
    GT = []
    for line in fh1:
        line = line.replace("\n", "")
        if line.replace(' ', '') == '':
            continue
        splitLine = line.split(",")
        idClass = splitLine[0]  # class
        x = float(splitLine[1])  # confidence
        y = float(splitLine[2])
        w = float(splitLine[3])
        h = float(splitLine[4])
        GT.append((x,y,w,h))
    fh1.close()
    GT_ALL.append(GT)
DE_ALL = []
folderDet = os.path.join(currentPath, 'detections')
os.chdir(folderDet)
files = glob.glob("*.txt")
files.sort()
for f in files:
    # nameOfImage = f.replace("_det.txt","")
    nameOfImage = f.replace(".txt", "")
    # Read detections from txt file
    fh1 = open(f, "r")
    DE = []
    for line in fh1:
        line = line.replace("\n", "")
        if line.replace(' ', '') == '':
            continue
        splitLine = line.split(",")
        idClass = splitLine[0]  # class
        confidence = float(splitLine[1])  # confidence
        x = float(splitLine[2])
        y = float(splitLine[3])
        w = float(splitLine[4])
        h = float(splitLine[5])
        DE.append((x,y,w,h))
    fh1.close()
    DE_ALL.append(DE)
IOU_ALL = []
def compute_iou(pe_re=1):
    for i in range(len(GT_ALL)):
        if GT_ALL[i] != []:
            file_gt = GT_ALL[i]
            file_de = DE_ALL[i]
            iou_file = []
            for box_gt in file_gt:
                iou_box = []
                for box_de in file_de:
                    iou_box.append(eva.iou(box_gt,box_de))

                iou_box.sort(reverse=True)
                #print(iou_box)
                if iou_box == []:
                    iou_box.append(0)
                iou_file.append(iou_box[0])
            if pe_re != 1:
                for j in range(len(iou_file)):
                    if 0 in iou_file:
                        iou_file.remove(0)
            if iou_file==[]:
                continue
            else:
                IOU_ALL.append(np.mean(iou_file))
    return np.mean(IOU_ALL)

print('precision_IOU:%f'%compute_iou(0))
print('recall_IOU:%f'%compute_iou(1))