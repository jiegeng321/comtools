#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import os
import json

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import shutil
from comfunc.tools import check_dir
fordeal_important = pd.read_excel("fordeal重点品牌分析详情1028.xlsx")
fordeal_important = fordeal_important.iloc[:,0].tolist()
fordeal_online = ['hello_kitty', 'jeep', 'salvatore_ferragamo', 'longines', 'van_cleef_arpels', 'casio', 'playboy', 'prada', 'tory_burch', 'fila', 'mlb', 'versace', 'new_balance', 'nike', 'rolex', 'converse', 'armani', 'franco_moschino', 'miu_miu', 'valentino_garavani', 'under_armour', 'calvin_klein', 'puma', 'vans', 'balenciaga', 'chanel', 'tommy_hilfiger', 'asics', 'supreme', 'patek_philippe', 'omega', 'lacoste', 'hugo_boss', 'louis_vuitton', 'swarovski', 'levis', 'chloe', 'mcm', 'hermes', 'michael_kors', 'moncler', 'loewe', 'the_north_face', 'cartier', 'ralph_lauren', 'alexander_mcqueen', 'bottega_veneta', 'coach', 'mercedes_benz', 'philipp_plein', 'juventus', 'canada_goose', 'celine', 'fendi', 'gucci', 'guess', 'adidas', 'vacheron_constantin', 'zara', 'givenchy', 'christian_louboutin', 'jimmy_choo', 'burberry', 'tiffany_co', 'bape', 'balmain', 'bvlgari', 'reebok', 'fc_barcelona_fcb', 'hublot', 'ellesse', 'panerai', 'lego', 'iwc', 'nba', 'timberland', 'porsche', 'fossil', 'citizen', 'ugg', 'nasa', 'stussy', 'tissot', 'bally', 'pandora', 'audemars_piguet']
fordeal_online2 =['dragon_ball','pinko','chrome_hearts','harry_potter','fc_barcelona_fcb','maserati','los_angeles_lakers','tous','dsquared2','playstation','diesel','chelsea','apple','coca_cola','stitch','3m','fear_of_god_essentials','chicago_bulls','avengers','disney','new_york_yankees','bosch','pokemon','oakley','valentino_garavani','paris_saint_germain','dkny','palm_angels','tods','lol_surprise']
fordeal_online = fordeal_online + fordeal_online2
baidu2l_dict = {"Comme des Garcons":"comme_des_garcons","ECCO":"ecco","Facebook":"facebook","美津浓":"mizuno",
                "雪佛兰":"chevrolet","伯爵":"piaget","Miu Miu":"miu_miu","瓦伦蒂诺":"valentino_garavani",
                "沛纳海":"panerai","大嘴猴":"paul_frank","谷歌":"google","H&M":"hm","布加迪":"bugatti_veyron",
                "奥迪":"audi","宝马":"bmw","倩碧":"clinique","西铁城":"citizen","兰博基尼":"lamborghini",
                "罗意威":"loewe","卡西欧":"casio","博世":"bosch","花花公子":"playboy","GAP":"gap","现代":"hyundai",
                "茵宝":"umbro","江诗丹顿":"vacheron_constantin","吉普":"jeep","宝珀":"blancpain","3M":"3m",
                "巴博斯":"brabus","Ellesse":"ellesse","Tory Burch":"tory_burch","雅诗兰黛":"estee_lauder",
                "DKNY":"dkny","REEBOK":"reebok","ZARA":"zara","娇韵诗":"clarins","高露洁":"colgate","登喜路":"dunhill",
                "DHC":"dhc","Everlast":"everlast","娇兰":"guerlain","霍尼韦尔":"honeywell","蜜丝佛陀":"max_factor",
                "摩托罗拉":"motorola","UGG":"ugg","宝格丽":"bvlgari","爱马仕":"hermes","泰格豪雅":"tag_heuer",
                "凯迪拉克":"cadillac","阿迪达斯":"adidas","李维斯":"levi's","路虎":"land_rover","奔驰":"mercedes_benz",
                "本田":"honda","美宝莲纽约":"maybelline","玛莎拉蒂":"maserati","保时捷":"porsche","范思哲":"versace",
                "巴黎世家":"balenciaga","哥伦比亚":"columbia","斐乐":"fila","彪马":"puma","阿玛尼":"armani","卡地亚":"cartier",
                "梵克雅宝":"van_cleef_arpels","蒙口":"moncler","蒂芙尼":"tiffany_co","JBL":"jbl","苹果":"apple",
                "Marc Jacobs":"marc_jacobs","菲拉格慕":"salvatore_ferragamo","耐克":"nike","芬迪":"fendi",
                "Calvin Klein":"calvin_klein","路易·威登":"louis_vuitton","赛琳":"celine","LACOSTE":"lacoste",
                "背靠背":"kappa","浪琴":"longines","博柏利/巴宝莉":"burberry","欧米茄":"omega","New Balance":"new_balance",
                "法拉利":"ferrari","宾利":"bentley","北面":"the_north_face","兰蔻":"lancome","七喜":"7up",
                "阿尔法·罗密欧":"alfar_romeo","红牛":"red_bull","帮宝适":"pampers","古驰":"gucci","拉尔夫·劳伦":"ralph_lauren",
                "Michael Kors":"michael_kors","Kate Spade":"kate_spade","劳力士":"rolex","百达翡丽":"patek_philippe",
                "普拉达":"prada","蔻驰":"coach","万国":"iwc","波士":"hugo_boss","碧浪":"ariel","BILLABONG":"billabong",
                "碧欧泉":"biotherm","可口可乐":"coca","康柏":"compaq","戴尔":"dell","滴露":"dettol","迪亚多纳":"diadora",
                "杜蕾斯":"durex","FOREVER 21":"forever_21","富士":"fuji_film","惠普":"hp",
                "杰克琼斯":"jack_jones","科颜氏":"kiehl's","KTM":"ktm","LG":"lg","奥林巴斯":"olympus","奥索卡":"ozark",
                "Roxy":"roxy","资生堂":"shiseido","斯柯达":"skoda","贝玲妃":"benefit","明基":"benq","宝玑":"breguet",
                "佳能":"canon","公牛":"chicago_bulls","迪奥":"dior","杜嘉班纳":"dolce_gabbana","伊丽莎白雅顿":"elizabeth_arden",
                "海飞丝":"headshoulders","讴歌":"honda","积家":"jaeger","茱莉蔻":"jurlique","KENZO":"kenzo",
                "巴黎欧莱雅":"l’oreal","万宝龙":"montblanc","潘婷":"pantene","丝芙兰":"sephora","skii":"sk","汰渍":"tide",
                "圣罗兰":"ysl"}
#"levis":"elvis_presley",
ali2l_dict = {"moschino":"franco_moschino","van_cleef_&_arpels":"van_cleef_arpels","valentino":"valentino_garavani",
              "abercrombie&fitch":"abercrombie_fitch","beats":"beats_by_drdre","hollister":"hollister_co",
              "levi’s":"levis","benz":"mercedes_benz","air_jordan":"nike","ralphlauren":"ralph_lauren",
              "ferragamo":"salvatore_ferragamo","tiffany":"tiffany_co","coca-cola":"coca","kiehl's":"kiehls",
              "l.o.l._surprise!":"lol_surprise","otterbox":"otter_box","lamborghini":"tonino_lamborghini",
              "dolce&gabbana":"dolce_gabbana","海飞丝":"head_shoulders","jaeger-lecoultre":"jaeger","levis":"levi's",
              "ray·ban":"rayban","sk-ii":"sk","s.t._dupont":"st_dupont","van_cleef_arpels":"van_cleef__arpels"
              }
model_dir = None#"/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/online_0415"
diff_dir = None#"/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/test_diff"

#logo white test
# model_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/white_test_0401.json"
# label_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/white_label.json"
#pattern white test
# model_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/white_test_0401.json"
# label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/white_label.json"
#pattern test
# model_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online_0324_2nd.json"
# label_json = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/label.json"
#logo test
model_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/clip_reebok.json"
label_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/label.json"
# score_th = {"adidas_h": 0.6, "coach_h": 0.5, "fendi_h": 0.65, "gucci_h": 0.6, "lv_h": 0.5, "michaelkors_h": 0.5, "nike_h": 0.55,
#                 'versace_h':0.7, 'christian dior_h':0.8, 'goyard_h':0.6, 'burberry_h':0.6, 'Issey miyake_h':0.6, 'celine_h':0.6,
#             "reebok_h":0.7,"mcm_h":0.75}

#score_th = {"nintendo":0.1,"Hello Kitty":0.4,"Casio":0.4,"Playboy":0.4,"New York Yankees":0.4,"Converse":0.4,"miu miu":0.4,"Valentino Garavani":0.4,"MCM":0.4,"Philipp Plein":0.4,"VACHERON CONSTANTIN":0.4,"Audi":0.4,"Bally":0.4,"Comme Des Garcons":0.45,"Lamborghini":0.4}
score_th = {"":0.1}
score_th_other = 0.999

save_result_csv = None#"/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/online_with_label_result.csv"
support_th = 30
show_pic = False
show_detail = True
if diff_dir and model_dir:
    check_dir(diff_dir,delete=True)
with open(model_json, 'r') as f:
    model_result = json.load(f)
#print(model_result)
#tmp = []
model_result_th = {}
if score_th:
    for k,pre_list in model_result.items():
        pre_list_th = []
        for pre in pre_list:
            for brand,score in pre.items():
                # if brand=="levi's":
                #     brand="levis"
                #print(brand)
                #tmp.append(score)
                if brand in score_th:
                    if score >= score_th[brand]:
                        # if brand in baidu2l_dict:
                        #     brand = baidu2l_dict[brand]
                        # if brand in ali2l_dict:
                        #     brand = ali2l_dict[brand]
                        pre_list_th.append(brand)
                else:
                    if score >= score_th_other:
                        # if brand in baidu2l_dict:
                        #     brand = baidu2l_dict[brand]
                        # if brand in ali2l_dict:
                        #     brand = ali2l_dict[brand]
                        print(k,pre_list)
                        pre_list_th.append(brand)
        if pre_list_th==[]:
            pre_list_th.append("empty")
        model_result_th[k]=list(set(pre_list_th))

    
with open(label_json, 'r') as f:
    label_result = json.load(f)
#print(len(label_result))
model_list = []
label_list = []
total_num = 0
diff_num = 0

for key,value in label_result.items():
    # if value!="empty":
    #     value = value+"_h"
    # if value == "reebok_h":
    #     print(key, value)
    # if model_result_th[key] == "mcm_h":
    #     print(key)
    if key in model_result_th:
        total_num += 1

        if value=="empty" and len(model_result_th[key])>=2 and "empty" in model_result_th[key]:
            label_list.append(value)
            model_result_th[key].remove("empty")
            #print(model_result_th[key])
            model_list.append(max(sorted(model_result_th[key]), key=model_result_th[key].count))
        else:
            #if value.split("-")[0] in model_result_th[key]:
                #print(value)
            if value in model_result_th[key]:

                label_list.append(value)
                model_list.append(value)
            else:
                if model_result_th[key]==[]:#img has problem
                    continue
                if len(model_result_th[key])>=2 and "empty" in model_result_th[key]:
                    model_result_th[key].remove("empty")
                label_list.append(value)
                model_list.append(max(sorted(model_result_th[key]), key=model_result_th[key].count))

        if label_list[-1] != model_list[-1]:
            diff_num += 1
            print(f"diff:{diff_num},{label_list[-1]}:{model_list[-1]}")
            if diff_dir and model_dir:
                for brand in os.listdir(model_dir):
                    if key in os.listdir(os.path.join(model_dir,brand)):
                        shutil.copy(os.path.join(model_dir,brand,key),os.path.join(diff_dir,label_list[-1]+"_"+model_list[-1]+"_"+key))

#print(label_list)
#print(model_list)
label_out_num = len(label_list) - label_list.count("empty")
model_out_num = len(model_list) - model_list.count("empty")
print(label_out_num/total_num)
print(model_out_num/total_num)
print(total_num)
print(diff_num)
print(diff_num/total_num)

#print(label_list)
#print(model_list)
class_result = classification_report(label_list, model_list,zero_division=False,output_dict=True)
#print(class_result)
#print(class_result["mcm"])

new_class_result = {}
for key,ite in class_result.items():
    if key=="accuracy" or key=="weighted avg" or key == "macro avg":# or key == "empty":
        continue
    if ite["support"]==0:
        continue
    ite["precision"] = round(ite["precision"],4)
    ite["recall"] = round(ite["recall"], 4)
    ite["f1-score"] = round(ite["f1-score"], 4)
    new_class_result[key] = [ite["support"],ite["recall"],ite["precision"],ite["f1-score"]]
pd_data = pd.DataFrame(new_class_result,index=["support","recall","precision","f1-score"])
    #print(key,item["support"])
pd_data = pd.DataFrame(pd_data.values.T,index=pd_data.columns,columns=pd_data.index)
#pd.set_option('max_colwidth',50)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd_data = pd_data.sort_values(by="support",ascending=False)
#print(pd_data)
# tmp = pd_data[pd_data["support"]>=10]
# print(tmp[tmp["recall"]<=0.93].index.tolist())
# print(len(tmp[tmp["recall"]<=0.93].index.tolist()))
if save_result_csv:
    pd_data.to_csv(save_result_csv)
#print(new_class_result)
# new_class_result = sorted(new_class_result.items(), key = lambda kv:(kv[1]["support"], kv[0]),reverse=True)
# for i in new_class_result:
#     print(i)
#print(type(new_class_result))
# print(pd_data[pd_data["support"]>=100].index.tolist())
# print(len(pd_data[pd_data["support"]>=100].index.tolist()))
print("total test brand have:",len(pd_data[pd_data["support"]>=support_th]))
print("total test num:",pd_data["support"].sum())
# print("recall mean: ", pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]!=0.0)]["recall"].mean())
# print("recall mean: ", pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]!=0.0)]["precision"].mean())
print("recall mean: ", pd_data[pd_data["support"]>=support_th]["recall"].mean())
print("precision mean: ", pd_data[pd_data["support"]>=support_th]["precision"].mean())
if show_pic:
    pd_data_plt = pd_data["support"].iloc[:20]
    pd_data_plt.plot.bar()
    plt.rcParams['figure.figsize'] = (20.0, 4.0)
    plt.savefig("data_info/total.png",dpi=300)
if show_detail:
    print(pd_data[pd_data["support"]>=support_th])
print("\n")

fordeal_important_ = []
for i in fordeal_important:
    if i not in pd_data.index.tolist():
        continue
    fordeal_important_.append(i)
# fordeal_important_ = ["gucci_h","lv_h","adidas_h","michaelkors_h","coach_h","christian_dior_h","fendi_h","celine_h","burberry_h",
#                       "goyard_h","versace_h","issey_miyake_h","mcm_h"]
fordeal_care = pd_data.loc[fordeal_important_,:]
print("fordeal care brand:",len(fordeal_care[fordeal_care["support"]>support_th]))
print("fordeal care test num:",fordeal_care["support"].sum())
print("recall mean: ", fordeal_care[fordeal_care["support"]>support_th]["recall"].mean())
print("precision mean: ", fordeal_care[fordeal_care["support"]>support_th]["precision"].mean())
if show_pic:
    pd_data_plt = fordeal_care["support"].iloc[:20]
    pd_data_plt.plot.bar()
    plt.rcParams['figure.figsize'] = (20.0, 4.0)
    plt.savefig("data_info/fordeal_care.png",dpi=300)
if show_detail:
    print(fordeal_care[fordeal_care["support"]>support_th])
print("\n")

fordeal_online_ = []
for i in fordeal_online:
    if i not in pd_data.index.tolist():
        continue
    fordeal_online_.append(i)
fordeal_online = pd_data.loc[fordeal_online_,:]
print("fordeal online brand:",len(fordeal_online[fordeal_online["support"]>support_th]))
print("fordeal online test num:",fordeal_online["support"].sum())
print("recall mean: ", fordeal_online[fordeal_online["support"]>support_th]["recall"].mean())
print("precision mean: ", fordeal_online[fordeal_online["support"]>support_th]["precision"].mean())
if show_pic:
    pd_data_plt = fordeal_online["support"].iloc[:20]
    pd_data_plt.plot.bar()
    plt.rcParams['figure.figsize'] = (20.0, 4.0)
    plt.savefig("data_info/fordeal_online.png",dpi=300)
if show_detail:
    print(fordeal_online[fordeal_online["support"]>support_th])
print("\n")

# special_brand = ["aeronautica_militare","baume_et_mercier","beachbody","france","golds_gym","nintendo","snow_white","spibelt"]
# special_brand = pd_data.loc[special_brand,:]
# print(special_brand[special_brand["support"]>support_th])


problem_brand = pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]<=0.5)]
print("problem brands:")
print(problem_brand)
#print("total test brand fordeal have: ",len(pd_data[pd_data["recall"]!=0].iloc[:,0]))
#print(pd_data[pd_data["recall"]!=0].index)

# print(pd_data[pd_data["support"]>=50].sort_values(by="f1-score",ascending=True))
# # logo_list = sorted(pd_data[pd_data["recall"]!=0].index.tolist())
# # for i in logo_list:
# #     print(i)
# tmp = ["allsaints","american_eagle","hamilton","jack_jones","reebok","maybelline","carolina_herrera","aspinal_of_london","iron_maiden","popsockets"]
# print(pd_data.loc[tmp,:].sort_values(by="f1-score",ascending=True))

# print("recall mean: ", len(pd_data[pd_data["recall"]>0]))
# print("recall mean: ", pd_data["recall"].mean())
# print("precision mean: ", pd_data["precision"].mean())
# print("recall mean: ", pd_data[pd_data["recall"]>0]["recall"].mean())
# print("precision mean: ", pd_data[pd_data["recall"]>0]["precision"].mean())
#print(len(pd_data[pd_data["f1-score"]==0]))
#print(len(pd_data[pd_data["f1-score"]==0])/1418)

print(total_num)
print(diff_num)
print(diff_num/total_num)
print("total test brand have:",len(pd_data[pd_data["support"]>=support_th]))
print("total test num:",pd_data["support"].sum())
# print("recall mean: ", pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]!=0.0)]["recall"].mean())
# print("recall mean: ", pd_data[(pd_data["support"]>=support_th) & (pd_data["f1-score"]!=0.0)]["precision"].mean())
print("recall mean: ", pd_data[pd_data["support"]>=support_th]["recall"].mean())
print("precision mean: ", pd_data[pd_data["support"]>=support_th]["precision"].mean())
if show_pic:
    pd_data_plt = pd_data["support"].iloc[:20]
    pd_data_plt.plot.bar()
    plt.rcParams['figure.figsize'] = (20.0, 4.0)
    plt.savefig("data_info/total.png",dpi=300)
if show_detail:
    print(pd_data[pd_data["support"]>=support_th])
print("\n")