import argparse
from pathlib import Path
import requests
import json
from tqdm import tqdm
from collections import Counter

parser = argparse.ArgumentParser(description='test for porn service')

parser.add_argument("--image_dir", type=str, default='.')
parser.add_argument('--output', type=str, default='result.csv')
parser.add_argument('--base_url', type=str, default='http://localhost:8093')

args = parser.parse_args()

BINARY_API_ENDPOINT = "{}/upload_binary".format(args.base_url)

image_list = [str(p) for p in Path(args.image_dir).rglob('*.jpg')]

found_num = 0
total_num = len(image_list)
predictions = []
with open(args.output, 'w') as output:
    for image_path in tqdm(image_list):
        with open(image_path, 'rb') as image_file:
            data = image_file.read()
            response = requests.post(url=BINARY_API_ENDPOINT, data=data)

            result = json.loads(response.text)
            if 'res' in result:
                pred = result['res']
                id = pred['id']
                if id > 0:
                    found_num += 0
                predictions.append(pred['id'])
            else:
                print(result)


print('='*20 + 'Summary' + '='*20)
if total_num > 0:
    print(f'valid test image num: \t{total_num}')
    print(f'decline image num: \t{found_num}')
    print(f'decline rate: \t\t{1.0*found_num/total_num*100:.2f}%')
    for item in Counter(predictions).items():
        print(item)
else:
    print('There are no image for testing.')
