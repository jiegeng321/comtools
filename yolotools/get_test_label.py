#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import os
import json

raw_test_data = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/brand_labeled"
save_label_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/label.json"

# raw_test_data = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_labeled/"
# save_label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/label.json"

test_files_list = os.listdir(raw_test_data)
label = {}
for files in test_files_list:
    for file in os.listdir(os.path.join(raw_test_data,files)):
        label[file] = files
#print(label)
with open(save_label_json, 'w') as f:
    json.dump(label, f)



