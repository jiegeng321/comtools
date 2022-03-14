# encoding:utf-8
import json
import requests
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from timeit import default_timer as timer

from tqdm import tqdm
import ast

AK = 'LTAI5tL286LAhrLdNPaSDRXz'
SK = '83kqmHetSvw7OEyhvqlfod17ZfsILn'

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkimageaudit.request.v20191230.ScanImageRequest import ScanImageRequest
import oss2
import os
import time
from tqdm import tqdm
auth = oss2.Auth(AK, SK)
bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'ali-logo-test-data')
client = AcsClient(AK, SK, 'cn-shanghai')
request = ScanImageRequest()
request.set_Scenes(["logo"])

# API调用
def DetectALi(file_name):
  try:
    img_url = bucket.sign_url('GET', 'ali-per20-test-data/'+file_name, 60, slash_safe=True)
    request.set_Tasks([{"ImageURL": img_url}])
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)
    res = ast.literal_eval(str(response, encoding='utf-8'))
    if res['Data']['Results'][0]['SubResults'][0]['Label']=="normal":
        return []
    res = res['Data']['Results'][0]['SubResults'][0]['LogoDataList']
  except Exception as e:
    print(file_name,"get some error:",e)
    if "QPS Limit" in str(e):
        time.sleep(0.21)
        return DetectALi(file_name)
    else:
        return 0
  return res

if __name__ == "__main__":
    imagedir = "/data01/xu.fx/dataset/LOGO_DATASET/logo_per20_test/per20_raw_data"
    save_json = "/data01/xu.fx/dataset/LOGO_DATASET/logo_per20_test/ali_logo_test_per20.json"

    file_list = os.listdir(imagedir)
    ali_result = {}
    for index,file in enumerate(file_list[:]):
        time.sleep(0.3)
        try:
            res = DetectALi(file)
            #print(res)
            if res == 0:
                continue
            result = []
            if res != []:
                for re in res:
                    brand = re["Name"].split("/")[0].lower().replace(" ","_")
                    result.append(brand)
            else:
                result.append("empty")
        except Exception as e:
            print(e)
            continue
        print(index, result)
        ali_result[file] = result
        if index%100==0:
            with open(save_json, 'w') as f:
                json.dump(ali_result, f)
    with open(save_json, 'w') as f:
        json.dump(ali_result, f)
    with open(save_json, 'r') as f:
        model_result = json.load(f)
    #print(model_result)
    print("total processed imgs:",len(model_result))





