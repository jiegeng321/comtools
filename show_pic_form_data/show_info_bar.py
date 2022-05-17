#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie , Line
import matplotlib.pyplot as plt

colors = ["#5793f3", "#d14a61", "#675bba"]
x_data = ["v0.1", "v0.2", "v0.3", "v0.4","v0.5","v0.6","v0.7","v0.8","v0.9"]
legend_list = ["品牌数量", "样式数量"]
brand_num_capacity = [38,95,171,209,259,364,364,444,440]
style_num_capacity = [80,169,289,345,443,634,634,803,704]

bar = (
    Bar(init_opts=opts.InitOpts())
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        "品牌数量",
        brand_num_capacity,
        bar_width=40,
        color=colors[0],

        yaxis_index=0,
        #color=colors[1],
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="品牌数量",
            type_="value",
            min_=0,
            #max_=500,
            #max_interval=50,
            position="left",
            axisline_opts=opts.AxisLineOpts(
                #linestyle_opts=opts.LineStyleOpts(width=2,color=colors[0])
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
        )
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="样式数量",
            type_="value",
            min_=0,
            max_=803,
            position="right",
            axisline_opts=opts.AxisLineOpts(
                #linestyle_opts=opts.LineStyleOpts(width=2, color=colors[1])
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
        )
    )
    .set_global_opts(
    #xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=True,rotate=-30,font_size=8)),
    title_opts=opts.TitleOpts(title="品牌迭代趋势图"),
)
)
line = (
    Line()
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="样式数量", y_axis=style_num_capacity,yaxis_index=2
    )
)
bar.overlap(line).render("./data_info/Version_of_the_iteration.html")



# brands = ["Longchamp",
# 'manolo blahnik',
# 'Maybelline',
# 'Patek Philippe',
# 'puma',
# 'Scotty Cameron',
# 'Sennheiser',
# 'as seen on TV',
# 'Dyson',
# 'Jurlique',
# 'Shimano',
# 'Skullcandy',
# 'SWAROVSKI',
# 'Taylormade',
# 'Timberland',
# 'Tissot',
# "Tod's",
# 'Efest',
# 'Emoji',
# 'Games Workshop',
# 'tous',
# 'Valentino Garavani',
# 'Vans',
# 'viviennewstwood',
# 'Yonex',
# 'Zegna',
# 'Baby Shark',
# 'Barbie',
# 'Blackberry Smoke',
# 'Care Bears',
# 'chad wild clay',
# 'Fox Head',
# 'Frida Kahlo',
# 'Harley Davidson',
# 'Hatchimals',
# 'Monchhichi',
# 'Monster Energy',
# 'MOTORHEAD',
# 'Movado',
# 'Bright Bugz',
# 'Iron Maiden',
# 'Marshall',
# 'Stussy',
# '3M',
# '3T',
# '5.11 Tactical',
# '7up',
# 'A. Lange Sohne',
# 'ac/dc',
# 'Acer',
# 'footjoy',
# 'Addicted',
# 'gazelle',
# 'stan smith',
# 'Ado Den Haag',
# 'Aeronautica Militare',
# 'affliction',
# 'Agnes B',
# 'AKG by Harmon',
# 'Alberta Ferretti',
# 'Alfar Romeo',
# 'Allsaints',
# 'Alpinestars',
# 'AS Roma',
# 'Asos',
# 'Aspinal of London',
# 'Atl�tico de Madrid',
# 'Audioquest',
# 'avengers',
# 'AWT',
# 'Azzaro',
# 'Babyliss',
# 'Bakugan',
# 'Ben Sherman',
# 'Benetton',
# 'BENQ',
# 'Bentley',
# 'Beretta',
# 'Berluti',
# 'Bestway',
# 'Betty Boop',
# 'Big Green Egg',
# 'Bill Blass',
# 'Billabong',
# 'Bioderma',
# 'Biotherm',
# 'BitDefender',
# 'black berry',
# 'black panther',
# 'Blancpain',
# 'BMC Racing',
# 'BMW',
# 'Bobbi Brown',
# 'Bontrager',
# 'BRABUS',
# 'Cadillac',
# 'Callaway',
# 'CAMELBAK',
# 'Cannondale',
# 'canon',
# 'captain america',
# 'Cards Against Humanity',
# 'Carhartt',
# 'Chopard',
# 'christian audigier',
# 'Chrome Hearts',
# 'Cisco',
# 'citizen',
# 'CLARINS',
# 'Clarisonic',
# 'bulova',
# 'bunch o balloons',
# 'Bunchems',
# 'Burts Bees',
# 'bushnell',
# 'BVB',
# 'c1rca',
# 'Cacharel',
# 'Led Zeppelin',
# 'CLUSE',
# 'Conair',
# 'concord',
# "D'Addario",
# 'Daiwa',
# 'deadpool',
# 'Dean Guitar',
# 'Def Leppard',
# 'L.O.L. SURPRISE!',
# 'Dell',
# 'Dettol',
# 'DeWALT',
# 'DHC',
# 'Diesel',
# 'Snow White',
# 'Doctor Strange',
# 'Donna Karan New York(DKNY)',
# 'Dr. Martens',
# 'Dunhill',
# 'ESS',
# 'Franck Muller',
# 'Franco Moschino',
# 'Fuji film',
# 'Furla',
# 'FURminator',
# 'Game of Thrones',
# 'Converse',
# 'Copper Fit',
# 'corum',
# 'coty',
# 'Crabs Adjust Humidity',
# 'Fischer',
# 'Fitbit',
# 'FJALLRAVEN',
# 'FLEXFIT',
# 'Foreo',
# 'GANT',
# 'GAP',
# 'Garmin',
# 'ghd',
# 'Giro',
# 'Kingston',
# 'KNVB',
# 'Lilo Stitch',
# 'Aeronautica Militare']
#
# for b in brands:
#     search_brand_info(b)