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
# print(foz.list_zoo_datasets())
# print(fo.list_datasets())
# print(fo.utils.openimages.get_classes())
# dataset = foz.load_zoo_dataset("quickstart")
# dataset = fo.load_dataset("open-images-v6-Handbag-Footwear")
from tqdm import tqdm

dataset = fo.Dataset.from_images_dir("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/shoes_bag/fordeal_wholee_shoes")
dataset_40000 = fo.Dataset()
for index,sample in tqdm(enumerate(dataset)):
    if index>=40000:
        break
    dataset_40000.add_sample(sample)
print(dataset)
print(dataset_40000)
# foz.list_zoo_models()
# foz.list_downloaded_zoo_models()
model = foz.load_zoo_model("mobilenet-v2-imagenet-torch")
embeddings = dataset_40000.compute_embeddings(model)
results = fob.compute_similarity(dataset_40000, embeddings=embeddings, brain_key="img_sim")
# viz_results = fob.compute_visualization(dataset, embeddings=embeddings, brain_key="img_viz")
results.find_unique(12000)
# results.find_duplicates(fraction=0.3)
# plot = results.visualize_unique(visualization=viz_results)
# plot.show(height=800, yaxis_scaleanchor="x")

dataset_unique = dataset_40000.select(results.unique_ids)
dataset_unique.export(
    export_dir="/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/shoes_bag/fordeal_wholee_shoes_unique12000",
    dataset_type=fo.types.ImageDirectory
)
# dataset.persistent = True
#
#dataset.info
# view = dataset.view()
# print(view)
# print(dataset.info)
# session = fo.launch_app(dataset)
# session.wait()
