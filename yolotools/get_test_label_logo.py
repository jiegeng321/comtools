#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import os
import json

with open('/data01/xu.fx/comtools/human_label_to_model_label/l2l_dict.json', 'r') as f:
    data = json.load(f)
print(data)
#print(data["ac/dc"])

raw_test_data = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/brand_labeled_old/"
#raw_test_data = "/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/pattern_test_data_labeled/"
save_label_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/label.json"
test_files_list = os.listdir(raw_test_data)
label = {}
for files in test_files_list:
    mid = ""
    # if files=="ac":
    #     mid = "dc"
    for file in os.listdir(os.path.join(raw_test_data,files,mid)):
        #files = files.split("-")[0]
        if files not in data:
            files = files.lower().replace(" ", "_")
        else:
            files = data[files].split("/")[-1]
        if mid == "dc":
            files = "acdc"
        if files == "new_york_yankees":
            files = "mlb"
        if files == "blue's_clues":
            files = "blues_clues"
        if files == "beats_by_dr.dre":
            files = "beats_by_drdre"
        if files == "a_cold_wall":
            files = "acoldwall"
        if files == "usa_soccer":
            files = "usa"
        if files == "trxtraining":
            files = "trx_training"
        if files == "psv_eindhoven":
            files = "psv"
        if files == "olympique_de_marseille":
            files = "olympique_marseille"
        if files == "m.a.c":
            files = "mac"
        if files == "kiehl's":
            files = "kiehls"
        if files == "jack_daniel's":
            files = "jack_daniels"
        if files == "g_star_raw":
            files = "gstar_raw"
        if files == "fc_barcelona(fcb)":
            files = "fc_barcelona_fcb"
        if files == "dooney__bourke":
            files = "dooney_bourke"
        if files == "death_wish_coffee_co.":
            files = "death_wish_coffee_co"
        if files == "d'addario":
            files = "daddario"
        if files == "carter's":
            files = "carters"
        if files == "bell__ross":
            files = "bell_ross"
        if files == "a._lange_sohne":
            files = "a_lange_sohne"
        if files == "5.11_tactical":
            files = "511_tactical"
        if files == "ac_dc":
            files = "acdc"
        if files == "headshoulders":
            files = "head_shoulders"
        if files == "l.o.l._surprise!":
            files = "lol_surprise"
        if files == "bunch_o_balloons":
            files = "bunch_o_ballons"
        if files == "dr._martens":
            files = "dr_martens"
        if files == "s.h.i.e.l.d.":
            files = "shield"
        if files == "u_boat":
            files = "uboat"
        label[file] = files

with open(save_label_json, 'w') as f:
    json.dump(label, f)
print(len(label))
print(label.popitem())


