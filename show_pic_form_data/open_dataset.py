#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import fiftyone as fo
from fiftyone.utils import openimages
import fiftyone.zoo as foz
# print(foz.list_zoo_datasets())
print(fo.list_datasets())
# print(openimages.get_classes(version="v6"))
# dataset = foz.load_zoo_dataset("quickstart")

# a = foz.datasets.ZooDatasetInfo("coco-2014",dataset_type)
# print(a.get_class_name())
# dataset = foz.load_zoo_dataset(name="coco-2014",split = "validation",classes=["handbag"],
#                                max_samples=10000,label_types=["detections"],
#                                only_matching = True,
#                                dataset_dir="/data02/xu.fx/dataset/OPEN_DATASET/fiftyone_dataset",
#                                dataset_name="coco-2014-handbag")
# dataset = foz.load_zoo_dataset(name="coco-2014",splits = ("train", "validation"),classes=["handbag"],
#                                label_types=["detections"],
#                                only_matching = True,
#                                dataset_dir="/data02/xu.fx/dataset/OPEN_DATASET/fiftyone_dataset",
#                                dataset_name="coco-2014-handbag")
# dataset.persistent = True
# dataset = foz.load_zoo_dataset(name="imagenet-2012",split = "train",classes=["running shoe"],
#                                max_samples=100,label_types=["detections"],
#                                only_matching = True,
#                                dataset_dir="/data02/xu.fx/dataset/OPEN_DATASET/fiftyone_dataset/imagenet-2012",
#                                dataset_name="imagenet-2012-runningShoe")
dataset = foz.load_zoo_dataset(name="open-images-v6", splits=("train", "validation"), classes=["Handbag","Footwear"],
                               label_types=["detections"],
                               max_samples=10000,
                               only_matching=True,
                               dataset_dir="/data02/xu.fx/dataset/OPEN_DATASET/fiftyone_dataset/open-images-v6",
                               dataset_name="open-images-v6-Handbag-Footwear")
# dataset.persistent = True
#
#dataset.info
view = dataset.view()
print(view)
print(dataset.info)
session = fo.launch_app(dataset)
session.wait()

#dataset_cartoon = fo.load_dataset("yolodataset_cartoon_54bs_57ks_0818")
dataset = fo.load_dataset("open-images-v6-Handbag-Footwear")
print(dataset.info)
print(dataset)
session = fo.launch_app(dataset)
# session.wait()
# from fiftyone import ViewField as F
# # view = dataset.filter_labels("ground_truth", F("label").is_in(["Handbag"]))
# view = dataset.filter_labels("detections", F("label").is_in(["Footwear"]))
#
# view.export(
#     export_dir="/data01/xu.fx/dataset/SHOES_DATASET/tmp",
#     dataset_type=fo.types.VOCDetectionDataset,
#     label_field="detections",
# )
import fiftyone.brain as fob
#fob.compute_uniqueness(dataset_cartoon)
