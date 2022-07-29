#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import torch
import clip
from ptflops import get_model_complexity_info
import torchvision.models as models
from torchsummary import summary
device = "cuda:0" if torch.cuda.is_available() else "cpu"
# model, preprocess = clip.load("RN101.pt", device=device)#['RN50', 'RN101', 'RN50x4', 'RN50x16', 'RN50x64', 'ViT-B/32', 'ViT-B/16', 'ViT-L/14', 'ViT-L/14@336px']
# model = model.visual
# model.float()
model = models.resnet101().cuda()
shape = (3,224,224)
summary(model,shape)
with torch.cuda.device(0):
    macs, params = get_model_complexity_info(model, shape, as_strings=True,
                                               print_per_layer_stat=True, verbose=True)
    print('{:<30}  {:<8}'.format('Computational complexity: ', macs))
    print('{:<30}  {:<8}'.format('Number of parameters: ', params))