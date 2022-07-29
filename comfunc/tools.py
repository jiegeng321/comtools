#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import os
import shutil
import pandas as pd
def is_img(img_name):
    return True if str(img_name).split(".")[-1].lower() in ["jpg","png","jpeg","gif"] and str(img_name)[0] != "." else False


def check_dir(path,delete=False):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if delete:
            shutil.rmtree(path)
            os.makedirs(path)
    return path

def read_csv(csv_path):
    if csv_path.endswith('.csv'):
        csv = pd.read_csv(csv_path, keep_default_na=False)
    else:
        print("the format is not support!")
        return None
    return csv

def read_xlsx(csv_path):
    if csv_path.endswith('.xlsx'):
        csv = pd.read_excel(csv_path, keep_default_na=False)
    else:
        print("the format is not support!")
        return None
    return csv