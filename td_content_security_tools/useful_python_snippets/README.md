### 收集一些组内常用到的python脚本

#### 测试图像服务(form参数接口):
```python
import requests
url = 'ip:port/logo_rec'
with open('test.jpg', 'rb') as f:
    image_data = f.read()
params = {'imageId': 'xdfadj', 'img': image_data}
response = requests.post(url, files=params)
print(response.json())
```

#### 多线程处理:
```python
from multiprocessing import Pool

def predict(image: str, label: int):
    url = 'ip:port/porn_rec'
    with open(image, 'rb') as f:
        image_data = f.read()
    params = {'imageId': 'dfadjk', 'img': image_data}
    response = requests.post(url, files=params)
    result = response.json()
    pred = result['id']
    score = result['score']
    return pred, score, label

num_process = 30
pool = Pool(num_process)
task = [('dfadjkj.jpg', 0)] * 10000

result = []
for image, label in task():
    result.append(pool.apply_async(predict, args=(image, label)))
pool.close()
pool.join()

for r in results:
    pred, score, label = r.get()
    # calculate statistics.
```
