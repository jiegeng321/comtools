import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import os
class DATASET_IMG_TXT_PAIR(Dataset):

    def __init__(self, root, train=True, transform = None, target_transform=None):
        super(DATASET_IMG_TXT_PAIR, self).__init__()
        self.train = train
        self.transform = transform
        self.target_transform = target_transform

        if self.train :
            #file_annotation = root + '/annotations/cifar10_train.json'
            self.img_folder = root + '/train/images'
            self.txt_folder = root + '/train/labels'
        else:
            self.img_folder = root + '/val/images'
            self.txt_folder = root + '/val/labels'

        self.imgnames = sorted(os.listdir(self.img_folder))
        self.labels = sorted(os.listdir(self.txt_folder))
        assert len(self.imgnames) == len(self.imgnames)

    def __getitem__(self, index):
        img_name = self.img_folder + '/' + self.imgnames[index]
        label_name = self.txt_folder + '/' + self.labels[index]
        assert img_name.split(".")[0] == label_name.split(".")[0]
        img = plt.imread(img_name)
        with open(label_name,"r") as f:
            lines = f.read()
            label = [float(i) for i in lines.strip('\n').split(' ')]
        if self.transform is not None:
            img = self.transform(img)


        return img, label

    def __len__(self):
        return len(self.imgnames)
