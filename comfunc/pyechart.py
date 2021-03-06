#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""


from pyecharts.charts import Bar
from pyecharts import options as opts

model_num = ["ads logo"]

data = (
{'bilibili': [0.966, 0.94], '康巴赫': [0.924, 0.717], 'haokan': [0.983, 0.955], '阿道夫': [0.981, 0.987], '小程序码': [0.957, 0.932], '微店': [0.972, 0.933], '腾讯视频': [0.873, 0.821], 'lishipin': [0.965, 0.971], '蓝帽子': [0.594, 1.0], '优酷': [0.948, 0.927], '京东':[0.933, 0.933], 'douyin': [0.962, 0.946], '西瓜视频': [0.939, 0.884], '二维码': [0.95, 0.913], 'weishi': [0.962, 0.974], '天猫': [0.899, 0.894], '拼多多': [0.941, 0.977], '唯品会': [0.941, 1.0], '花西子': [0.92, 0.852], '芒果TV': [0.873, 0.897], '淘宝': [0.961, 0.898], 'kuaishou': [0.955, 0.98], '爱奇艺': [0.805, 0.754], 'miaopai': [0.991, 0.966], 'huoshan': [0.948, 0.973], '蘑菇街': [1.0, 1.0]}
,
# {'天猫': [0.921, 0.911], 'lishipin': [0.96, 0.971], '康巴赫': [0.897, 0.788], '芒果TV': [0.882, 0.874], 'bilibili': [0.963, 0.942], '二维码': [0.97, 0.87], 'kuaishou': [0.95, 0.988], '京东': [0.933, 0.959], '蘑菇街': [1.0, 1.0], '阿道夫': [0.984, 0.99], 'huoshan': [0.97, 0.97], '腾讯视频': [0.848, 0.817], '优酷': [0.931, 0.92], 'weishi': [0.956, 0.994], '小程序码': [0.949, 0.962], '淘宝': [0.948, 0.925], '花西子': [0.88, 0.88], '唯品会': [1.0, 1.0], '微店': [0.958, 0.932], 'miaopai': [0.996, 0.962], '爱奇艺': [0.822, 0.829], 'haokan': [0.98, 0.9], '西瓜视频':[0.904, 0.972], '拼多多': [0.948, 0.985], '蓝帽子': [0.719, 0.958], 'douyin': [0.971, 0.947]}
# ,
# {'golden goose': [0.996, 0.981], 'the north face': [0.884, 0.989], 'nike': [0.916, 0.914], 'Kenzo': [0.947, 0.971], 'coach': [0.565, 0.909], 'dolce': [0.897, 0.954], 'supreme': [0.786, 0.326], 'dior': [0.891, 0.986], 'armani': [0.983, 0.574], 'dsquared2': [0.778, 0.286], 'Michael Kors': [0.914, 0.923], 'off': [0.925, 0.804], 'Moncler': [0.897, 0.819], 'Hermes': [0.775, 0.86], 'ysl': [0.973, 0.986], 'burberry': [0.89, 0.913], 'gucci': [0.947, 0.916], 'lv': [0.985, 0.871], 'fendi': [0.927, 0.976], 'prada': [0.785, 0.948], 'balenciaga': [0.963, 0.942], 'chanel': [0.931, 0.944], 'versace': [0.962, 0.986], 'ck': [0.904, 0.698], 'Givenchy': [0.9, 0.858]}
# ,
# {'chanel': [0.922, 0.973], 'gucci': [0.941, 0.935], 'dolce': [0.9, 1.0], 'Hermes': [0.798, 0.94], 'dior': [0.881, 0.997], 'nike': [0.887, 0.95], 'balenciaga': [0.957, 0.984], 'supreme': [0.794, 0.413], 'ck': [0.93, 0.8], 'burberry': [0.908, 0.955], 'fendi': [0.914, 0.981], 'coach': [0.661, 0.886], 'dsquared2': [0.806, 0.203], 'Michael Kors': [0.914, 0.955], 'Moncler': [0.885, 0.847], 'the north face': [0.891, 0.992], 'prada': [0.796, 0.91], 'Givenchy': [0.909, 0.905], 'armani': [0.965, 0.72], 'Kenzo': [0.972, 0.968], 'ysl': [0.973, 0.989], 'lv': [0.972, 0.869], 'off': [0.914, 0.89], 'versace': [0.962, 0.998], 'golden goose': [0.996, 1.0]}
# ,
# {'weishi': [0.93, 0.976], 'kuaishou': [0.95, 0.985], 'huoshan': [0.97, 0.966], '二维码': [0.987, 0.855], 'miaopai': [0.991, 0.966], 'haokan': [0.988, 0.95], 'bilibili': [0.975, 0.946], '小程序码': [0.965, 0.859], 'douyin': [0.964, 0.952], 'lishipin': [0.955, 0.978]}
# ,
# {'bilibili': [0.972, 0.98], 'weishi': [0.968, 0.991], 'haokan': [0.988, 0.983], '二维码': [0.98, 0.988], 'lishipin': [0.967, 0.972], 'douyin': [0.972, 0.983], 'huoshan': [0.961, 0.982], '小程序码': [0.954, 0.992], 'miaopai': [0.991, 0.975], 'kuaishou': [0.95, 0.983]}
# ,
# {'the north face': [0.884, 0.989], 'dolce': [0.9, 0.954], 'ysl': [0.973, 0.986], 'lv': [0.985, 0.871], 'chanel': [0.931, 0.944], 'Givenchy': [0.9, 0.858], 'gucci': [0.947, 0.916], 'Hermes': [0.775, 0.86], 'dior': [0.891, 0.986], 'burberry': [0.89, 0.913], 'prada': [0.785, 0.948], 'Michael Kors': [0.914, 0.923], 'armani': [0.983, 0.574], 'golden goose': [0.996, 0.981], 'off': [0.925, 0.808], 'coach': [0.565, 0.909], 'fendi': [0.927, 0.976], 'balenciaga': [0.963, 0.942], 'versace': [0.962, 0.986], 'nike': [0.916, 0.914], 'Kenzo': [0.947, 0.971], 'ck': [0.904, 0.698], 'dsquared2': [0.778, 0.286], 'Moncler': [0.897, 0.819], 'supreme': [0.786, 0.326]}
# ,
# {'dsquared2': [0.75, 0.397], 'Kenzo': [0.968, 0.932], 'golden goose': [0.996, 0.985], 'Hermes': [0.802, 0.898], 'nike': [0.912, 0.918], 'prada': [0.781, 0.916], 'ck': [0.943, 0.76], 'off': [0.919, 0.872], 'coach': [0.571, 0.935], 'dolce': [0.907, 0.989], 'Moncler': [0.891, 0.874], 'chanel': [0.929, 0.971], 'armani': [0.977, 0.593], 'supreme': [0.794, 0.124], 'Givenchy': [0.909, 0.839], 'the north face': [0.918, 0.985], 'ysl': [0.97, 0.986], 'dior': [0.904, 0.997], 'versace': [0.965, 0.986], 'fendi': [0.939, 0.976], 'gucci': [0.95, 0.908], 'balenciaga': [0.968, 0.95], 'Michael Kors': [0.892, 0.922], 'lv': [0.97, 0.891], 'burberry': [0.922, 0.922]}
# ,
# {'burberry': [0.922, 0.891], 'Moncler': [0.878, 0.721], 'ysl': [0.981, 0.968], 'Givenchy': [0.913, 0.634], 'nike': [0.912, 0.912], 'supreme': [0.794, 0.2], 'versace': [0.96, 0.984], 'Michael Kors': [0.924, 0.919], 'chanel': [0.917, 0.968], 'dior': [0.931, 0.987], 'armani': [0.988, 0.474], 'coach': [0.61, 0.947], 'fendi': [0.932, 0.966], 'prada': [0.749, 0.878], 'the north face': [0.915, 0.964], 'Hermes': [0.791, 0.866], 'dsquared2': [0.694, 0.216], 'dolce': [0.914, 0.975], 'lv': [0.977, 0.855], 'Kenzo': [0.979, 0.871], 'balenciaga': [0.969, 0.886], 'ck': [0.947, 0.584], 'golden goose': [0.996, 0.987], 'off': [0.903, 0.8], 'gucci': [0.947, 0.859]}
# ,
# {'chanel': [0.917, 0.99], 'Michael Kors': [0.924, 0.994], 'coach': [0.61, 1.0], 'gucci': [0.947, 0.99], 'dsquared2': [0.694, 0.833], 'the north face': [0.912, 1.0], 'Kenzo': [0.979, 1.0], 'dior': [0.931, 1.0], 'armani': [0.988, 0.994], 'lv': [0.977, 0.985], 'ysl': [0.981, 0.997], 'versace': [0.96, 0.995], 'Givenchy': [0.913, 0.991], 'ck': [0.947, 1.0], 'balenciaga': [0.969, 0.988], 'Moncler': [0.878, 0.958], 'golden goose': [0.996, 1.0], 'off': [0.903, 0.994], 'fendi': [0.932, 0.992], 'nike': [0.912, 0.992], 'burberry': [0.922, 0.974], 'prada': [0.749, 0.995], 'supreme': [0.794, 0.945], 'dolce': [0.914, 1.0], 'Hermes': [0.791, 1.0]}
# ,
)


bar = Bar(opts.InitOpts(width="100%"))
keys = list(sorted(data[0].keys()))
# keys = data[0].keys()
print(list(keys))
print(len(list(keys)))
bar.add_xaxis(list(keys)[:])

for index, data_i in enumerate(data):
    recall = []
    precisions = []
    for key_i in keys:
        print(data_i[key_i][0])
        recall.append(data_i[key_i][0])
        precisions.append(data_i[key_i][1])
    print(recall)
    bar.add_yaxis('召回率', recall[:], gap="0%")
    bar.add_yaxis("查准率", precisions[:], gap="0%")

bar.set_global_opts(title_opts={"text":"AdsLOGO20210323", 'subtext': "Recall: 0.95164 Pecision:0.931891 F1-score: 0.94166"}, xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=True,rotate=30), interval=10))
bar.render("test.html")



