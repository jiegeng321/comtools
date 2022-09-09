#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import fiftyone as fo
import fiftyone.zoo as foz
import fiftyone.brain as fob
from fiftyone import ViewField as F
# 加载&创建数据集
# dataset = foz.load_zoo_dataset("coco")
# dataset = fo.load_dataset("open-images-v6-Handbag-Footwear")
# dataset = fo.Dataset.from_images_dir("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/包")
#
# name = "yolodataset_cartoon_54bs_57ks_0818"
# dataset_dir = "/data02/xu.fx/dataset/CARTOON_DATASET/comb_data/yolodataset_cartoon_54bs_57ks_0818/JPEGImages"
# splits = ["train", "val"]
# dataset = fo.Dataset(name)
# for split in splits:
#     dataset.add_dir(
#         dataset_dir=dataset_dir,
#         dataset_type=fo.types.YOLOv5Dataset,
#         split=split,
#         tags=split,
#         yaml_path="/data01/xu.fx/yolov5v6.0/yolov5/data/yolodataset_cartoon_54bs_57ks.yaml"
# )

dataset = fo.Dataset("test-dataset")
# 加载&创建样本
sample = fo.Sample(filepath="/data02/xu.fx/dataset/SHOES_BAG_DATASET/comb_data/yolodataset_shoes_bag_2bs_2ks_0902/JPEGImages/val/images/rBNaFV8WtDmANRwYAAM6DVKXig4406.jpg")
# 自定义样本属性字段 Fields
sample["test_field1"] = "hard"
sample["test_field2"] = 89.7
# 添加样本标签 tags
sample = fo.Sample(filepath="/path/to/image.png", tags=["train"])
sample.tags.append("my_favorite_samples")
# 添加标注
sample["weather"] = fo.Classification(label="sunny")
sample["animals"] = fo.Detections(
    detections=[
        fo.Detection(label="cat", bounding_box=[0.5, 0.5, 0.4, 0.3]),
        fo.Detection(label="dog", bounding_box=[0.2, 0.2, 0.2, 0.4]),
    ]
)
# 添加样本
dataset.add_sample(sample)

# dataset.compute_metadata()
# fo.pprint(dataset.stats(include_media=True))
