import argparse
from pathlib import Path
import requests
import json
from tqdm import tqdm
import time

parser = argparse.ArgumentParser(description='test for terror service')

parser.add_argument("--image_dir", type=str, default='.')
parser.add_argument('--output', type=str, default='result.csv')
parser.add_argument('--url_terror_cls', type=str, default='http://localhost:4000')
parser.add_argument('--url_logo_det', type=str, default='http://localhost:4001')
parser.add_argument('--url_terror_det', type=str, default='http://localhost:4002')
parser.add_argument('--conf_thresh_logo_det', type=float, default=0.5)
parser.add_argument('--conf_thresh_ter_det', type=float, default=0.5)

args = parser.parse_args()

BINARY_API_ENDPOINT_LOGO_DET = "{}/logo_rec_binary".format(args.url_logo_det)
BINARY_API_ENDPOINT_TERROR_DET = "{}/logo_rec_binary".format(args.url_terror_det)
BINARY_API_ENDPOINT_TERROR_CLS = "{}/upload_binary".format(args.url_terror_cls)

image_list = [str(p) for p in Path(args.image_dir).rglob('*.jpg')]

found_num_ter_cls = 0
found_num_ter_det = 0
found_num_logo_det = 0
found_num_ter_cls_det_logo = 0
total_num = len(image_list)

with open(args.output, 'w') as output:
    for image_path in tqdm(image_list):
        bool_ter_cls = False
        bool_ter_det=False
        bool_logo_det = False
        with open(image_path, 'rb') as image_file:
            data = image_file.read()
            response_logo_det = requests.post(url=BINARY_API_ENDPOINT_LOGO_DET, data=data)
            response_ter_det = requests.post(url=BINARY_API_ENDPOINT_TERROR_DET, data=data)
            response_ter_cls = requests.post(url=BINARY_API_ENDPOINT_TERROR_CLS, data=data)
            
            result_logo_det = json.loads(response_logo_det.text)
            result_ter_det = json.loads(response_ter_det.text)
            result_ter_cls = json.loads(response_ter_cls.text)

            
            if 'res' in result_ter_det:
                pred_ter_det = result_ter_det['res']
                for ter_det_instance in pred_ter_det:
                    if ter_det_instance['score'] > args.conf_thresh_ter_det:
                        bool_ter_det = True
                        #output.write(f'ter_det:{json.dumps(pred)},')
                        break

            if 'res' in result_logo_det:
                pred_logo_det = result_logo_det['res']
                for logo_instance in pred_logo_det:
                    if logo_instance['score'] > args.conf_thresh_logo_det:
                        bool_logo_det = True
                        #output.write(f'logo_det:{json.dumps(pred)},')
                        break
            if  result_ter_cls['type'] != 'NORMAL':
                bool_ter_cls = True
                #output.write(f'ter_cls:{json.dumps(pred)},{image_path}\n')
            if bool_ter_cls == True:  found_num_ter_cls+=1
            if bool_ter_det == True:  found_num_ter_det+=1
            if bool_logo_det == True:  found_num_logo_det+=1

            if bool_ter_cls == True  or  bool_logo_det == True or  bool_ter_det == True:
                found_num_ter_cls_det_logo += 1
                output.write(f'ter_det:{json.dumps(pred_ter_det)},logo_det:{json.dumps(pred_logo_det)},ter_cls:{json.dumps(result_ter_cls)},{image_path}\n' )
            else:
                print (image_path)

			
			

		        


print('='*20 + 'Summary' + '='*20)
if total_num > 0:
    print(f'valid test image num: \t{total_num}')
    print(f'decline image num: \t{found_num_ter_cls_det_logo}')
    print(f'decline rate: \t\t{1.0*found_num_ter_cls_det_logo/total_num*100:.2f}%')
else:
    print('There are no image for testing.')
