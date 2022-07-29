#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
#learn from https://gallery.pyecharts.org

cate = ['0', '1', '2', '3', '4', '5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
data1 = [0.14, 0.11, 0.09, 0.09, 0.08, 0.07,0.06,0.07,0.06,0.04,0.04,0.03,0.02,0.02,0.01,0.01,0.007,0.005,0.006,0.005,0.005]
#data2 = [110, 120, 111, 107, 98, 23]
title = "遗忘次数Top20"
save_name = "./show_tmp.html"

c = (
    Bar()
    .add_xaxis(cate)
    .add_yaxis("A", data1)
    #.add_yaxis("B", data2)
    .set_global_opts(
        title_opts=opts.TitleOpts(title=title, subtitle=""),
        xaxis_opts=opts.AxisOpts(name="遗忘次数",name_location="end"),
        yaxis_opts=opts.AxisOpts(name="比例"),
        #datazoom_opts=opts.DataZoomOpts(),
        #toolbox_opts=opts.ToolboxOpts()
    )
    .render(save_name)
)