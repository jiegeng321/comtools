#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
#learn from https://gallery.pyecharts.org

cate = ['Apple', 'Huawei', 'Xiaomi', 'Oppo', 'Vivo', 'Meizu']
data = [123, 153, 89, 107, 98, 23]
title = "测试标题"
save_name = "./show_tmp.html"

pie = (Pie()
       .add('', [list(z) for z in zip(cate, data)])
       .set_global_opts(title_opts=opts.TitleOpts(title=title))
       .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))

       )

pie.render(save_name)