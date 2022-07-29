#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import torch
import onnx
from clip.model import *
import clip
import onnxsim
pt_path = "RN101.pt"
save_onnx_img_path = "RN101_img.onnx"
#save_onnx_text_path = "ViT-L-14-336px_text.onnx"
device = "cuda:1"
# model = torch.load(pt_path,map_location=device)
model, preprocess = clip.load(pt_path, device=device)
print(model.visual)
model.float()
#print(model.transformer)
im = torch.zeros(1, 3, *(224,224)).to(device)
#text = torch.zeros(1,1, 768).to(device).half()
torch.onnx.export(model.visual, im, save_onnx_img_path, verbose=False, opset_version=12,
                  input_names=['images'],
                  output_names=['output'],
                  dynamic_axes=None)
# torch.onnx.export(model.transformer, text, save_onnx_text_path, verbose=False, opset_version=12,
#                   input_names=['text'],
#                   output_names=['output'],
#                   dynamic_axes=None)
model_onnx = onnx.load(save_onnx_img_path)  # load onnx model
onnx.checker.check_model(model_onnx)  # check onnx model
# model_onnx = onnx.load(save_onnx_text_path)  # load onnx model
# onnx.checker.check_model(model_onnx)  # check onnx model
# model_onnx, check = onnxsim.simplify(model_onnx)
# onnx.save(model_onnx, save_onnx_img_path)
