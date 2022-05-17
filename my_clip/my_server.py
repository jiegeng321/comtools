#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import gradio as gr


def greet(name):
    return "Hello " + name + "!!"


iface = gr.Interface(fn=greet, inputs="text", outputs="text")
iface.launch()

