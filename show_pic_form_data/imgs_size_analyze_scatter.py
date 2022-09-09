#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import cv2
from pathlib import Path
from comfunc.tools import *
import shutil
import pyecharts.options as opts
from pyecharts.charts import Scatter
from tqdm import tqdm
import numpy as np
src_dir = Path("/data01/xu.fx/dataset/BAG_DATASET/comb_data/checked")
img_list = [i for i in src_dir.rglob("*") if is_img(i)]
# size_th = 2000
# dst_dir = "/data01/xu.fx/comtools/content_security_tools/locust_load_test/big_size"
hs = []
ws = []
low = 0
for img in tqdm(img_list):
    try:
        image = cv2.imread(str(img))
        h,w=image.shape[:2]
        hs.append(h)
        ws.append(w)
        if h*w<400*400:
            low+=1
    except Exception as e:
        print(e)
        continue
    # print(h,w)
    # if min(image.shape)<size_th:
    #     print(min(image.shape))
    #     check_dir(dst_dir)
    #     shutil.move(img,dst_dir)



# data.sort(key=lambda x: x[0])
x_data = ws
y_data = hs
print("mean w:",np.mean(x_data))
print("mean h:",np.mean(y_data))
print(low,low/len(hs))
(
    Scatter(init_opts=opts.InitOpts(width="1000px", height="800px"))
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="",
        y_axis=y_data,
        symbol_size=20,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_series_opts()
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False),
    )
    .render("basic_scatter_chart2.html")
)

