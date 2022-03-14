#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import json
with open("config.json", 'r') as f:
    pt_onnx_trt = json.load(f)
print(pt_onnx_trt["logo_id_to_name"])