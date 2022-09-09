#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import fiftyone as fo
import fiftyone.zoo as foz
#print(foz.list_zoo_datasets())
print(fo.list_datasets())
# dataset = foz.load_zoo_dataset("quickstart")
# name = "yolodataset_pattern_18bs_26ks_0815"
# dataset_dir = "/data02/xu.fx/dataset/PATTERN_DATASET/comb_data/yolodataset_pattern_18bs_26ks_0815/JPEGImages"
# splits = ["train", "eval"]
# dataset = fo.Dataset(name)
# for split in splits:
#     dataset.add_dir(
#         dataset_dir=dataset_dir,
#         dataset_type=fo.types.YOLOv5Dataset,
#         split=split,
#         tags=split,
#         yaml_path="/data01/xu.fx/yolov5v6.0/yolov5/data/yolodataset_pattern_18bs_26ks.yaml"
# )
name = "yolodataset_cartoon_54bs_57ks_0818"
dataset_dir = "/data02/xu.fx/dataset/CARTOON_DATASET/comb_data/yolodataset_cartoon_54bs_57ks_0818/JPEGImages"
splits = ["train", "val"]
dataset = fo.Dataset(name)
for split in splits:
    dataset.add_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.YOLOv5Dataset,
        split=split,
        tags=split,
        yaml_path="/data01/xu.fx/yolov5v6.0/yolov5/data/yolodataset_cartoon_54bs_57ks.yaml"
)
print(dataset)
dataset.persistent=True
# Print the first few samples in the dataset
# print(dataset.head())

# view = dataset.view()
# print(view)
# print(dataset.info)
# session = fo.launch_app(dataset)
# session.wait()

# dataset_cartoon = fo.load_dataset("yolodataset_cartoon_54bs_57ks_0818")
# from fiftyone import ViewField as F
# view = dataset.filter_labels("ground_truth", F("label").is_in(["圣诞老人"]))
# view.export(
#     export_dir="/data02/xu.fx/dataset/CARTOON_DATASET/comb_data/圣诞老人_dataset_voc",
#     dataset_type=fo.types.VOCDetectionDataset,
#     label_field="ground_truth",
# )
