#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import json
with open("pt_onnx_trt.json", 'r') as f:
    pt_onnx_trt = json.load(f)
with open("pt_wts_trt.json", 'r') as f:
    pt_wts_trt = json.load(f)
#pt_onnx_trt = json.loads("pt_onnx_trt.json")
#pt_wts_trt = json.loads("pt_wts_trt.json")
print(len(pt_onnx_trt))
print(len(pt_wts_trt))
# for i in range(len(pt_wts_trt)):
#     if abs(pt_wts_trt[i+5]["averageMs"]-pt_onnx_trt[i+9]["averageMs"]) >= 0.1:
#         print(i,pt_wts_trt[i+5]["name"],pt_wts_trt[i+5]["averageMs"],pt_onnx_trt[i+9]["name"],pt_onnx_trt[i+9]["averageMs"])

#for i in range(len(pt_wts_trt)):
#    print(i,pt_wts_trt[i+5]["name"],"||",pt_onnx_trt[i+9]["name"],"---",pt_wts_trt[i+5]["averageMs"],pt_onnx_trt[i+9]["averageMs"])
pt_wts_trt = sorted(pt_wts_trt[1:],key=lambda x:x["percentage"],reverse=True)
print(pt_wts_trt)
pt_onnx_trt = sorted(pt_onnx_trt[1:],key=lambda x:x["percentage"],reverse=True)
print(pt_onnx_trt)