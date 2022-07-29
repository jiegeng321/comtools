#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import cv2
from pathlib import Path
from comfunc.tools import *
import shutil
import pyecharts.options as opts
from pyecharts.charts import Scatter

src_dir = Path("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/wholee_for_logo_arfa_0725")
img_list = [i for i in src_dir.rglob("*") if is_img(i)]
size_th = 2000
dst_dir = "/data01/xu.fx/comtools/content_security_tools/locust_load_test/big_size"
hs = []
ws = []
for img in img_list:
    image = cv2.imread(str(img))
    h,w=image.shape[:2]
    hs.append(h)
    ws.append(w)
    # print(h,w)
    # if min(image.shape)<size_th:
    #     print(min(image.shape))
    #     check_dir(dst_dir)
    #     shutil.move(img,dst_dir)


data = [
    [10.0, 8.04],
    [8.0, 6.95],
    [13.0, 7.58],
    [9.0, 8.81],
    [11.0, 8.33],
    [14.0, 9.96],
    [6.0, 7.24],
    [4.0, 4.26],
    [12.0, 10.84],
    [7.0, 4.82],
    [5.0, 5.68],
]
# data.sort(key=lambda x: x[0])
x_data = ws
y_data = hs

(
    Scatter(init_opts=opts.InitOpts(width="1600px", height="1000px"))
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
    .render("basic_scatter_chart.html")
)

