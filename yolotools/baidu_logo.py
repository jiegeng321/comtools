# encoding:utf-8
import cv2
import requests
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from timeit import default_timer as timer

from tqdm import tqdm

AK = 'q2IXUGNXW0iQdsWxy6l2Ch7l'
SK = 'QWF5wBQzILDKZBMHq7FbxUzKwX6GAGuI'
# access_token = "24.0d70a32d7e0c9eecc6832234a1bcedea.2592000.1619590729.282335-23859657"
scale = 0.1

# {'result': [{'probability': 0.99838553625962, 'name': '爱马仕', 'location': {'top': 258, 'left': 53, 'width': 106, 'height': 46}, 'type': 0}, {'probability': 0.99777181395169, 'name': '范思哲', 'location': {'top': 425, 'left': 23, 'width': 166, 'height': 169}, 'type': 0}, {'probability': 0.9960784254403, 'name': '普拉达', 'location': {'top': 289, 'left': 478, 'width': 127, 'height': 34}, 'type': 0}, {'probability': 0.9846914718891, 'name': '古驰', 'location': {'top': 302, 'left': 254, 'width': 140, 'height': 96}, 'type': 0}, {'probability': 0.97710606147503, 'name': '香奈儿', 'location': {'top': 459, 'left': 476, 'width': 129, 'height': 92}, 'type': 0}, {'probability': 0.95696852947104, 'name': '爱马仕', 'location': {'top': 298, 'left': 16, 'width': 185, 'height': 34}, 'type': 0}, {'probability': 0.94097023174681, 'name': '范思哲', 'location': {'top': 554, 'left': 37, 'width': 144, 'height': 53}, 'type': 0}, {'probability': 0.9373748384673, 'name': '古驰', 'location': {'top': 251, 'left': 244, 'width': 161, 'height': 38}, 'type': 0}, {'probability': 0.8744874202599, 'name': '香奈儿', 'location': {'top': 539, 'left': 445, 'width': 191, 'height': 38}, 'type': 0}], 'log_id': 1376775560411217920, 'result_num': 9}


# 鉴权
def Authoried():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(AK, SK)
    response = requests.get(host)
    access_token = None
    if response:
        access_token = response.json()['access_token']
    return access_token

# 添加文字
def cv2ImgAddText(img, text, left, top, textColor=(255, 0, 0), textSize=10):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype(
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

# 编码转换
def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString,np.uint8)
    image = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    return image

# 画图
def DrawImg(base64_str, res):
    img = base64_cv2(base64_str)
    if res:
        for i in res['result']:
            class_name = i['name']
            prob = i['probability']
            xmin = int(i['location']['left'])
            ymin = int(i['location']['top'])
            xmax = i['location']['left'] + i['location']['width']
            ymax = i['location']['top'] + i['location']['height']
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), [0, 255, 0], 1)
            img = cv2ImgAddText(img, class_name +": " + str(round(prob, 3)), xmin, ymin - 10)
    else:
        pass
    cv2.imshow("img", img)
    cv2.waitKey(-1)

# API调用
def DetectBaiDu(img_path):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/logo"
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"custom_lib": False, "image": img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    tic = timer()
    response = requests.post(request_url, data=params, headers=headers)
    toc = timer()
    alltims = (toc-tic)*1000
    res_json = response.json()
    # res_json = {'result': [{'probability': 0.99838553625962, 'name': '爱马仕', 'location': {'top': 258, 'left': 53, 'width': 106, 'height': 46}, 'type': 0}, {'probability': 0.99777181395169, 'name': '范思哲', 'location': {'top': 425, 'left': 23, 'width': 166, 'height': 169}, 'type': 0}, {'probability': 0.9960784254403, 'name': '普拉达', 'location': {'top': 289, 'left': 478, 'width': 127, 'height': 34}, 'type': 0}, {'probability': 0.9846914718891, 'name': '古驰', 'location': {'top': 302, 'left': 254, 'width': 140, 'height': 96}, 'type': 0}, {'probability': 0.97710606147503, 'name': '香奈儿', 'location': {'top': 459, 'left': 476, 'width': 129, 'height': 92}, 'type': 0}, {'probability': 0.95696852947104, 'name': '爱马仕', 'location': {'top': 298, 'left': 16, 'width': 185, 'height': 34}, 'type': 0}, {'probability': 0.94097023174681, 'name': '范思哲', 'location': {'top': 554, 'left': 37, 'width': 144, 'height': 53}, 'type': 0}, {'probability': 0.9373748384673, 'name': '古驰', 'location': {'top': 251, 'left': 244, 'width': 161, 'height': 38}, 'type': 0}, {'probability': 0.8744874202599, 'name': '香奈儿', 'location': {'top': 539, 'left': 445, 'width': 191, 'height': 38}, 'type': 0}], 'log_id': 1376775560411217920, 'result_num': 9}
    return img, res_json, alltims

if __name__ == "__main__":
    imagedir = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/brand_labeled_online"
    save_json = "/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/fordeal_test_online_total_baidu2.json"
    #image_path = "/gpudata/erwei.wang/data_interface/50个品牌测试百度品牌识别能力的样本/balmain/4cbee315b72352c77680f950b695d8b1.jpg"
    from timeit import default_timer as timer
    from pathlib import Path
    import json

    access_token = Authoried()
    # print(access_token)
    # #单个图片测试
    # img, res, ti = DetectBaiDu(image_path)
    # print(res)
    # DrawImg(img, res)
    l2l_dict = {"蔻依":"chloe","香奈儿":"chanel","Comme des Garcons":"comme_des_garcons","ECCO":"ecco","Facebook":"facebook","美津浓":"mizuno",
                "雪佛兰":"chevrolet","伯爵":"piaget","Miu Miu":"miu_miu","瓦伦蒂诺":"valentino_garavani",
                "沛纳海":"panerai","大嘴猴":"paul_frank","谷歌":"google","H&M":"hm","布加迪":"bugatti_veyron",
                "奥迪":"audi","宝马":"bmw","倩碧":"clinique","西铁城":"citizen","兰博基尼":"lamborghini",
                "罗意威":"loewe","卡西欧":"casio","博世":"bosch","花花公子":"playboy","GAP":"gap","现代":"hyundai",
                "茵宝":"umbro","江诗丹顿":"vacheron_constantin","吉普":"jeep","宝珀":"blancpain","3M":"3m",
                "巴博斯":"brabus","Ellesse":"ellesse","Tory Burch":"tory_burch","雅诗兰黛":"estee_lauder",
                "DKNY":"dkny","REEBOK":"reebok","ZARA":"zara","娇韵诗":"clarins","高露洁":"colgate","登喜路":"dunhill",
                "DHC":"dhc","Everlast":"everlast","娇兰":"guerlain","霍尼韦尔":"honeywell","蜜丝佛陀":"max_factor",
                "摩托罗拉":"motorola"}
    #文件夹推理并保存结果
    image_dir = Path(imagedir)

    files = [file for file in image_dir.rglob("*.*")][:]
    baidu_result = {}
    total_result = []
    for index,file in enumerate(files):
        try:
            img, res, ti = DetectBaiDu(file)
            result = []
            if res["result"] != []:
                #print(res)
                for re in res["result"]:
                    brand = re["name"]
                    score = re["probability"]
                    if brand in l2l_dict:
                        brand = l2l_dict[brand]
                    result.append({brand:score})
            else:
                result.append({"empty":1.0})
            #print(index,result)
            total_result+=result
        except Exception as e:
            print(e)
            continue
        print(index, file.name, result)
        baidu_result[file.name] = result
        if index%100==0:
            with open(save_json, 'w') as f:
                json.dump(baidu_result, f)
    with open(save_json, 'w') as f:
        json.dump(baidu_result, f)
    print(total_result)
    #print(list(set(total_result)))
    with open(save_json, 'r') as f:
        model_result = json.load(f)
    print(len(model_result))

    # files = glob(os.path.join(imagedir, "./*.jpg"))
    # num = len(files)
    # alltim = 0
    # for file in files:
    #     img, res, ti = DetectBaiDu(file)
    #     alltim = alltim + ti
    #     print(ti)
    # print("num:", num)
    # print("all time:", alltim)
    # print("mean time:", alltim/num)
    # # DrawImg(img, res)


# num: 109
# all time: 50107.50342812389
# mean time: 459.70186631306325


# num: 109
# all time: 50372.027864679694
# mean time: 462.1286960062357





