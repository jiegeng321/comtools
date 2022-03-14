#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie , Line
import matplotlib.pyplot as plt

# dr martens Dr. Martens-w-1
# seiko  grandseiko
save_pic_flag = False
show_data_flag = False
search_brand = "zenith"
brand_csv = "./data_info/comb_777bs_1401ks_bal3000_brand_info.csv"
label_csv = "./data_info/comb_777bs_1401ks_bal3000_label_info.csv"
file_num_csv = "./data_info/comb_777bs_1401ks_bal3000_file_num_info.csv"

result_csv = "./data_info/comb_444bs_803ks_test_result.csv"
rpfc_info_csv = "./data_info/comb_444bs_803ks_rpfc_info.csv"

save_name_head = brand_csv.split("/")[-1].split(".")[0].split("_")[0]+"_"+brand_csv.split("/")[-1].split(".")[0].split("_")[1]
print("save name:",save_name_head)
colors = ["#5793f3", "#d14a61", "#675bba"]
x_data = ["v0.1", "v0.2", "v0.3", "v0.4","v0.5","v0.6","v0.7","v0.8","v0.9"]
legend_list = ["品牌数量", "样式数量"]
brand_num_capacity = [38,95,171,209,259,364,364,444,440]
style_num_capacity = [80,169,289,345,443,634,634,803,704]

result_csv_data = pd.read_csv(result_csv)
brand_csv_data = pd.read_csv(brand_csv)
label_csv_data = pd.read_csv(label_csv)
file_num_csv_data = pd.read_csv(file_num_csv)
rpfc_info_csv_data = pd.read_csv(rpfc_info_csv)


brand_csv_data = brand_csv_data.iloc[:,1:]
result_csv_data = result_csv_data.iloc[:,1:]
label_csv_data = label_csv_data.iloc[:,1:]
file_num_csv_data = file_num_csv_data.iloc[:,1:]

brand_csv_data.sort_values(by=0,axis=1,ascending=False,inplace=True)
result_csv_data.sort_values(by=0,axis=1,ascending=False,inplace=True)
label_csv_data.sort_values(by=0,axis=1,ascending=False,inplace=True)

total_num = file_num_csv_data.iloc[0,0]
train_num = int(file_num_csv_data.iloc[0,1])
val_num = int(file_num_csv_data.iloc[0,2])

file_num_csv_data = file_num_csv_data.iloc[:,3:]
file_num_csv_data.sort_values(by=0,axis=1,ascending=False,inplace=True)

file_num_columns = file_num_csv_data.columns.values[:].tolist()
file_num = file_num_csv_data.iloc[0,:].values.tolist()

columns = result_csv_data.columns.values[:].tolist()
recall = np.round(result_csv_data.iloc[0,:].values,2).tolist()
precision = np.round(result_csv_data.iloc[1,:].values,2).tolist()

recall_all = np.round(rpfc_info_csv_data.iloc[0,1],3)
precision_all = np.round(rpfc_info_csv_data.iloc[0,2],3)
f1_all = np.round(rpfc_info_csv_data.iloc[0,3],3)
acc_all = np.round(rpfc_info_csv_data.iloc[0,4],3)

brand_columns = brand_csv_data.columns.values[:].tolist()
brand_num = brand_csv_data.iloc[0,:].values.tolist()
label_columns = label_csv_data.columns.values[:].tolist()
label_num = label_csv_data.iloc[0,:].values.tolist()

def show_data():
    print("1. Dataset info: ")
    print("total_num: ",total_num)
    print("train_num: ",train_num)
    print("val_num: ",val_num,"\n")

    print("2. Brand info (box num): ")
    print("brand: ", brand_columns)
    print("brand num: ", brand_num)
    print("brand size: ", len(brand_columns),"\n")

    print("3. Style info (box num): ")
    print("label: ", label_columns)
    print("label num: ", label_num)
    print("label size: ", len(label_columns),"\n")

    print("4. File info: ")
    print("file_info: ", file_num_columns)
    print("file num: ", file_num)
    print("file size: ", len(file_num_columns),"\n")

    print("5. Result info: ")
    print("brand: ", brand_columns)
    print("recall: ", recall)
    print("precision: ", precision)
    print("recall_all: ", recall_all)
    print("precision_all: ", precision_all)
    print("f1_all: ", f1_all)
    print("acc_all: ", acc_all)
    #label_columns.sort(key=str.lower)
    #print(label_columns)
    #print(len(label_columns))
def save_pic():
    bar = Bar(opts.InitOpts(width="100%"))
    bar.add_xaxis(columns)
    bar.add_yaxis("recall", recall)
    bar.add_yaxis("precision", precision)
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=True,rotate=-30,font_size=8)),
        title_opts=opts.TitleOpts(title="Logo Detect Performance", subtitle="Recall: %0.3f Pecision: %0.3f F1-score: %0.3f"%(recall_all,precision_all,f1_all)),
    )
    bar.render("./data_info/%s_performance.html"%save_name_head)

    bar = Bar(opts.InitOpts(width="100%"))
    bar.add_xaxis(brand_columns)
    bar.add_yaxis("num", brand_num)
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30,font_size=8)),
        title_opts=opts.TitleOpts(title="品牌数量", subtitle="各品牌(object)数量"),
    )
    bar.render("./data_info/%s_brand_num_bar.html"%save_name_head)



    bar3 = Bar(opts.InitOpts(width="100%"))
    bar3.add_xaxis(label_columns)
    bar3.add_yaxis("num", label_num)
    bar3.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=True,rotate=-30,font_size=8)),
        title_opts=opts.TitleOpts(title="样式数量", subtitle="各品牌各样式(object)数量"),
    )
    bar3.render("./data_info/%s_label_num_bar.html"%save_name_head)

    c = (
        Pie(opts.InitOpts(width="100%"))
        .add("", [list(z) for z in zip(brand_columns, brand_num)],center=["60%", "60%"],)
        #.set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        .set_global_opts(title_opts=opts.TitleOpts(title="品牌数量",subtitle="各品牌(object)数量"),legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),)
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("./data_info/%s_brand_num_pie.html"%save_name_head)
    )
    c = (
        Pie(opts.InitOpts(width="100%"))
        .add("", [list(z) for z in zip(label_columns, label_num)],center=["68%", "60%"],)
        #.set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        .set_global_opts(title_opts=opts.TitleOpts(title="样式数量",subtitle="各品牌各样式(object)数量"),legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),)
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("./data_info/%s_label_num_pie.html"%save_name_head)
    )
    c = (
        Pie(opts.InitOpts(width="100%"))
        .add("", [list(z) for z in zip(file_num_columns, file_num)],center=["68%", "60%"],)
        #.set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        .set_global_opts(title_opts=opts.TitleOpts(title="文件数量",subtitle="各品牌文件数量"),legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),)
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("./data_info/%s_file_num_pie.html"%save_name_head)
    )
    c = (
        Pie(opts.InitOpts(width="100%"))
        .add("", [list(z) for z in zip(['train num','val num'], [train_num,val_num])],center=["68%", "60%"])
        #.set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        .set_global_opts(title_opts=opts.TitleOpts(title="训练/验证图片数量",subtitle="数据总量：%s 训练：验证 = 8：2"%total_num),legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),)
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("./data_info/%s_traval_num_pie.html"%save_name_head)
    )

    #if save_name_head.split("_")[0] == "comb":


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
def search_brand_info(search_brand):
    for i in brand_csv_data.columns:
        if i.replace(" ","").lower() == search_brand.replace(" ","").lower():
            print("BRAND NAME:" ,i)
            #print("\n")
            print("brand num:",brand_csv_data[i].values[0])
    for i in label_csv_data.columns:
        if i.split("-")[0].replace(" ","").lower() == search_brand.replace(" ","").lower():
            #print("style name:" ,i)
            print("%s num:"%i,label_csv_data[i].values[0])
    for i in file_num_csv_data.columns:
        if i.replace(" ","").lower() == search_brand.replace(" ","").lower():
            print("file %s num:"%i,file_num_csv_data[i].values[0])

    for i in result_csv_data.columns:
        if i.replace(" ","").lower() == search_brand.replace(" ","").lower():
            print("%s recall:"%i,result_csv_data[i].values[0])
            print("%s precision:" % i, result_csv_data[i].values[1])


if save_pic_flag:
    save_pic()
if show_data_flag:
    show_data()
if search_brand:
    search_brand_info(search_brand)

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