import argparse
import json
import os
import time
from datetime import date
import pandas as pd
from tqdm import tqdm
from loguru import logger
import docker
import requests
import yaml

from sklearn.metrics import classification_report
from database_util import get_dataset_session
from metrics.brand_metric import BrandMetric

parser = argparse.ArgumentParser(description="model regression test")
parser.add_argument("--test-config", type=str, default="porn_config.prototxt")
parser.add_argument("--endpoint", type=str, default="upload_binary")
parser.add_argument("--port", type=str, default="8091")
parser.add_argument("--write_database", type=bool, default=False)
args = parser.parse_args()

logger.remove()
logger.add("output-{time}.log", format="{message}")
logger.info("version,precision,recall,label")

with open('/data01/xu.fx/comtools/human_label_to_model_label/l2l_dict.json', 'r') as f:
    l2l_data = json.load(f)
def porn_id_converter(fine_label):
    return 0 if fine_label == 0 else 1


def predict_on_testset(label_result, api_endpoint, port):
    service_url = f"http://10.57.31.15:{port}/{api_endpoint}"
    predictions = []
    ground_truth = []
    for key in tqdm(os.listdir(config["test_data"]["test_img_dir"])):
        if key not in label_result:
            continue
        #with open(image_path, "rb") as image_file:
            #data = image_file.read()
        img_path = os.path.join(config["test_data"]["test_img_dir"],key)
        if not os.path.exists(img_path):
            continue
        try:
            payload = {'imageId': '00003'}
            file_temp = [('img', (key, open(img_path, 'rb'), 'image/jpeg'))]
            resq1 = requests.request
            response = resq1("POST", service_url, data=payload, files=file_temp)
            result = json.loads(response.text)
            #print(result)
            #result = response.json()  ### exception, image order corresponding
        except Exception as e:
            print(img_path, str(e))

        else:
            # from response to coarse id
            # if result==None:
            #     continue
            if 'res' in result:
                pred = result['res']
                # if pred==None:
                #     continue
                if pred == []:

                    brand_name = "empty"
                    predictions.append(brand_name)
                    #print(label_result[key])
                    ground_truth.append(label_result[key])
                else:
                    logo_list = []
                    for logo_instance in pred:
                        logo = logo_instance['logo_name']
                        if logo not in l2l_data:
                            logo = logo.lower().replace(" ", "_")
                        else:
                            logo = l2l_data[logo].split("/")[-1]
                        if logo == "new_york_yankees":
                            logo = "mlb"
                        logo_list.append(logo)
                    if label_result[key] in logo_list:
                        predictions.append(label_result[key])
                        ground_truth.append(label_result[key])
                    else:
                        predictions.append(max(logo_list, key=logo_list.count))
                        ground_truth.append(label_result[key])
            else:
                #ground_truth.pop(index)
                #brand_name = "empty"
                #predictions.append(brand_name)
                print("no res in result")
    return predictions,ground_truth


def test_one_version(version, label_result, api_endpoint, port):
    try:
        # start container
        print(f"start container {version['image']}...")
        service_container = client.containers.run(
            version["image"],
            auto_remove=True,
            ports={"8088/tcp": port},
            detach=True,
            environment={"WORKERS": 4},
        )
        service_container.logs(stream=True)
        time.sleep(3)
        print(f"begin to test version: {version['version_tag']}")
        predictions,ground_truth = predict_on_testset(label_result, api_endpoint, port)
    except Exception as e:
        print(str(e))
    else:
        # compute metrics
        report = classification_report(ground_truth, predictions, output_dict=True)
        # print(report)
        # print(ground_truth)
        # print(predictions)
        new_class_result = {}
        for key, ite in report.items():
            if key == "accuracy" or key == "weighted avg" or key == "macro avg" or key == "empty":
                continue
            if ite["support"] == 0:
                continue
            ite["precision"] = round(ite["precision"], 2)
            ite["recall"] = round(ite["recall"], 2)
            ite["f1-score"] = round(ite["f1-score"], 2)
            new_class_result[key] = [ite["support"], ite["recall"], ite["precision"], ite["f1-score"]]
        pd_data = pd.DataFrame(new_class_result, index=["support", "recall", "precision", "f1-score"])
        pd_data = pd.DataFrame(pd_data.values.T, index=pd_data.columns, columns=pd_data.index)
        pd_data = pd_data.sort_values(by="support", ascending=False)
        # write metrics
        precision = pd_data[pd_data["support"]>=50]["precision"].mean()
        recall = pd_data[pd_data["support"]>=50]["recall"].mean()
        logger.info(f"{version['version_tag']},{precision},{recall}")
        return precision, recall

    finally:
        service_container.kill()
    return


if __name__ == "__main__":
    # config = satelite.TestConfig()
    with open(args.test_config, "r") as f:
        config = yaml.safe_load(f)
    print(config)
    image_list = []
    ground_truth = []
    with open(config["test_data"]["examples"], 'r') as f:
        label_result = json.load(f)
    # for key, value in label_result.items():
    #     image_list.append(os.path.join(config["test_data"]["test_img_dir"],key))
    #     ground_truth.append(value)
    #with open(config["test_data"]["examples"], "r") as f:
    #    for line in f.readlines():
    #         image_path, label = line.strip().split(",")
    #         image_list.append(image_path)
    #         ground_truth.append(porn_id_converter(int(label)))

    # 远程控制容器:
    client = docker.DockerClient(base_url='tcp://10.57.31.15:10000')
    #client = docker.from_env()

    if not config["test_data"]["is_modified"]:
        # test last version
        version = config["versions"][-1]
        precision, recall = test_one_version(
            version, label_result, args.endpoint, args.port
        )
    else:
        for version in config["versions"]:
            precision, recall = test_one_version(
                version, label_result, args.endpoint, args.port
            )
            print(f"{precision}, {recall}, {version['brand_num']},{version['style_num']}, {version['version_tag']}")
            if args.write_database:
                DBSession = get_dataset_session()
                session = DBSession()
                new_metric = BrandMetric(
                    model_name=config["model_name"],
                    model_version=version["version_tag"],
                    recall=recall,
                    precision=precision,
                    brand_num=int(version['brand_num']),
                    style_num=int(version['style_num']),
                    date=date.today(),
                )
                session.add(new_metric)
                session.commit()
                session.close()
            time.sleep(10)
