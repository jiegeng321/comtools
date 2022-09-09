#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
#learn from https://gallery.pyecharts.org

cate = ['卡通', '鞋包','衣物','其他']
data = [0.35,0.30,0.25,0.10 ]
title = ""
save_name = "./saved_data_images/pie.html"

pie = (Pie()
       .add('', [list(z) for z in zip(cate, data)])
       .set_global_opts(title_opts=opts.TitleOpts(title=title))
       .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))

       )

pie.render(save_name)