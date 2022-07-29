#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
#learn from https://gallery.pyecharts.org

cate = ['未支持品牌/样式', '卡阈值', '漏检','遮挡严重',"模糊","边缘过滤"]
data = [9246, 1685, 582,144,241,156]
title = ""
save_name = "./show_tmp.html"

pie = (Pie()
       .add('', [list(z) for z in zip(cate, data)])
       .set_global_opts(title_opts=opts.TitleOpts(title=title))
       .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))

       )

pie.render(save_name)