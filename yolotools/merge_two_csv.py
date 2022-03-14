#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import os
import json


import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import shutil
save_result_csv1 = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/online_with_label_result.csv"
save_result_csv2 = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/online_with_label_result2.csv"
save_result_csv_merge = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data/online_with_label_result_merge.csv"
pd1=pd.read_csv(save_result_csv1)
pd2=pd.read_csv(save_result_csv2)
pd2 = pd2[["Unnamed: 0","recall","precision","f1-score"]]

pd_merge=pd.merge(pd1,pd2,how="left",on="Unnamed: 0")
pd_merge.to_csv(save_result_csv_merge)
#pd_baidu = pd2[[]]
print(pd_merge)




