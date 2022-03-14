# coding:utf-8
#import cv2
from flask import Flask,render_template,request
from PIL import Image, ImageDraw, ImageFont
app = Flask(__name__)
import base64
import requests
import json
#import cv2
# import os
# import numpy as np
# import pandas as pd
#from tqdm import tqdm
from io import BytesIO
# url
#ai_brand_logo_url = "http://10.57.31.15:5032/v2/logo_brand_rec"
ai_brand_logo_url = "https://ai-brand-logostg.tongdun.cn/v2/logo_brand_rec"
#ai_brand_logo_tm_url = "http://10.58.14.38:55902/v2/logo_brand_rec"
#ai_brand_logo_tm_url = "https://ai-brand-logo-tmstg.tongdun.cn/v2/logo_brand_rec"
brand_pattern_url = "https://ai-brand-pattern.tongdun.me/v2/pattern_brand_rec"#"http://10.58.14.38:55903/v2/pattern_brand_rec"
cartoon_url = "https://ai-cartoon-detstg.tongdun.cn/v2/cartoon_rec"
#https://ai-brand-pattern.tongdun.me/v2/pattern_brand_rec
url_dict = {"logo":ai_brand_logo_url,"pattern":brand_pattern_url,"cartoon":cartoon_url}

save_result_path = "./static/images/tmp_result.jpg"
tmp_file = "./static/images/tmp_raw.jpg"

def url_res(img_data,file_name, url):
    #img = byte2cv(imgdata)
    payload = {'imageId': '00003'}
    file_temp = [('img', (file_name, img_data, 'image/jpeg'))]
    resq1 = requests.request
    response = resq1("POST", url, data=payload, files=file_temp)
    result = json.loads(response.text)
    return result["res"]

def main(img_path,img_data):
    img_after_dec = Image.open(img_path).convert("RGB")
    img_draw = ImageDraw.Draw(img_after_dec)
    #img = byte2cv(img_path)
    result_total = {}
    result_one = []
    for model_name,url in url_dict.items():
        res = url_res(img_data,"noname",url)
        result = []
        if model_name=="logo":
            color = "red"
        # elif model_name=="logo-tm":
        #     color = "blue"
        elif model_name=="cartoon":
            color = "yellow"
        else:
            color = "green"
        for logo_instance in res:
            box = logo_instance['box']
            name = logo_instance['logo_name']
            result_one.append(name)
            score = round(logo_instance['score'], 2)
            result.append(name+":"+str(score))
            x1 = box['x1']
            y1 = box['y1']
            x2 = box['x2']
            y2 = box['y2']
            try:
                img_draw.rectangle((x1, y1, x2, y2), outline=color, width=2)
                #font = ImageFont.truetype(size=5)
                img_draw.text((x1, y1-11), name+":"+str(score), fill=color)
                #cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                #cv2.putText(img, name+"_"+str(score), (x1 - 6, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 0, 0], 1, cv2.LINE_AA)
            except:
                continue
        if result==[]:
            result.append("未检测到logo")
        result_total[model_name]=result
    img_after_dec.save(save_result_path)
    #cv2.imwrite(save_result_path, img)
    if result_one==[]:
        result_one = '未检测到logo'
    else:
        result_one.sort()
        result_one = max(result_one, key=result_one.count)
    return result_total,result_one


@app.route('/logo_server', methods=['POST', 'GET'])
def logo_server():
    if request.method == 'POST':
        try:
            f = request.files['file']
            #base64_str = base64.b64encode(f)
            #image_binary = base64.b64decode(f)
            img = Image.open(f)

            output_buffer = BytesIO()
            img.save(output_buffer, format="PNG")
            byte_data = output_buffer.getvalue()
            #base64_str = base64.b64encode(byte_data)
            img.save(tmp_file)
            result_total,result_one = main(tmp_file,byte_data)
            return render_template('logo_ok_dec.html',upload_path=tmp_file,
                                   result_one=result_one,img_after_dec_path=save_result_path,
                                   logo_result=result_total["logo"],
                                   pattern_result=result_total["pattern"],cartoon_result=result_total["cartoon"]
                                   )
        except:
            render_template('logo_error.html')
    return render_template('logo_dec.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8088,debug = False)
