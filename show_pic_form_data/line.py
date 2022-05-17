#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
#learn from https://gallery.pyecharts.org

cate = ['Apple', 'Huawei', 'Xiaomi', 'Oppo', 'Vivo', 'Meizu']
data1 = [123, 153, 89, 107, 98, 23]
data2 = [110, 120, 111, 107, 98, 23]
title = "测试标题"
save_name = "./show_tmp.html"

c = (
    Bar()
    .add_xaxis(cate)
    .add_yaxis("A", data1)
    .add_yaxis("B", data2)
    .set_global_opts(
        title_opts=opts.TitleOpts(title=title, subtitle=""),
        #brush_opts=opts.BrushOpts(),
        datazoom_opts=opts.DataZoomOpts(),
        toolbox_opts=opts.ToolboxOpts()
    )
    .render(save_name)
)