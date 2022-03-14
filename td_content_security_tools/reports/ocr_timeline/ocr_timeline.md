
# OCR 模型耗时分布统计分析

统计OCR模型耗时分布， 定位速度瓶颈， 确定优化目标。

## 1. 测试流程及指标
![png](output_1_0.png)

## 2. 测试数据

  - 数据名称：RB500
  - 样本数量：503
  - boxes数量：min 1, max 15, mean 2.37



## 3. 快速版ai-adver-ocr测试 

  - 检测模型
    - 输入分辩率 960x960：小图用padding补足， 大图最长边resize至960再将短边pad补齐
  
  - 识别模型
    - 输入分辨率 320x32：高度resize至32， 宽度等比例缩放（长边大于320使用策略剪切分多张图片识别， 小于320的pad 补齐）
    - batchsize: 8
  
### 3.1 单worker、单用户请求测试
  - 请求网络：TONGDUN 办公内网
  - 部署机器：td10
  - 显卡类型：Tesla P100
  - WORKER：1
  - 请求并发：1


```python

import pandas as pd
import numpy as np
from tools.timeline_kit import timeline_show
columns = [
    'image_id',        # 图片
    'total',           # 总流程耗时（服务端）
    'download',        # 图片下载耗时
    'decode',          # 图片解码耗时
    
    'det_preproc',     # 检测前处理耗时
    'det_infer',       # 检测模型推理耗时
    'det_postproc',    # 检测后处理耗时
    
    'transition',      # 检测框处理、结构化、图片裁切耗时
    
    'rec_preproc',     # 文字识别前处理耗时（多个minibatch合并） 
    'rec_infer',       # 文字识别模型推理耗时（多个minibatch合并）
    'rec_postproc',    # 文字识别模型后处理耗时（多个minibatch合并）
    'rec_batch',       # 文字识别模型 mini batch 数量 
]


selected_cols = [
    'download',        # 图片下载耗时
    'decode',          # 图片解码耗时
    
    'det_preproc',     # 检测前处理耗时
    'det_infer',       # 检测模型推理耗时
    'det_postproc',    # 检测后处理耗时
    
    'transition',      # 检测框处理、结构化、图片裁切耗时
    
    'rec_preproc',     # 文字识别前处理耗时（多个minibatch合并） 
    'rec_infer',       # 文字识别模型推理耗时（多个minibatch合并）
    'rec_postproc',    # 文字识别模型后处理耗时（多个minibatch合并）
]
```


```python
# ai-adver-ocr single
path = '/home/lijun.clj/data/ocr_test_doc/xdocr_single_timer.csv' 

data = pd.read_csv(path, header=None, index_col=None)
data.columns = columns
data.sort_values(by=['total'], ascending=[top_k < 0], inplace=True)

timeline_show(data[selected_cols], selected_cols, top_k=5, figsize=(7.2, 12.8))

```


![png](output_3_0.png)


  
### 3.2 多worker、多用户请求测试
  - 请求网络：TONGDUN 办公内网
  - 部署机器：td10
  - 显卡类型：Tesla P100
  - WORKER：10
  - 请求并发：15


```python
# ai-adver-ocr multi
path = '/home/lijun.clj/data/ocr_test_doc/xdocr_multi_timer.csv'

data = pd.read_csv(path, header=None, index_col=None)
data.columns = columns
data.sort_values(by=['total'], ascending=[top_k < 0], inplace=True)

timeline_show(data[selected_cols], selected_cols, top_k=5, figsize=(7.2, 12.8))
```


![png](output_5_0.png)


## 4. 高精版ai-adver-ocr-acc测试 

  - 检测模型
    - 输入分辩率 960x960：小图用padding补足， 大图最长边resize至960再将短边pad补齐
  
  - 识别模型
    - 输入分辨率 320x32：高度resize至32， 宽度等比例缩放（长边大于320使用策略剪切分多张图片识别， 小于320的pad 补齐）
    - batchsize: 8
  
### 4.1 单worker、单用户请求测试
  - 请求网络：TONGDUN 办公内网
  - 部署机器：td10
  - 显卡类型：Tesla P100
  - WORKER：1
  - 请求并发：1


```python
# ai-adver-ocr-acc single
path = '/home/lijun.clj/data/ocr_test_doc/xdocr_acc_single_timer.csv' 

data = pd.read_csv(path, header=None, index_col=None)
data.columns = columns
data.sort_values(by=['total'], ascending=[top_k < 0], inplace=True)

timeline_show(data[selected_cols], selected_cols, top_k=5, figsize=(7.2, 12.8))
```


![png](output_7_0.png)


### 4.2 多worker、多用户请求测试
  - 请求网络：TONGDUN 办公内网
  - 部署机器：td10
  - 显卡类型：Tesla P100
  - WORKER：4
  - 请求并发：6


```python
# ai-adver-ocr-acc multi
path = '/home/lijun.clj/data/ocr_test_doc/xdocr_acc_multi_timer.csv'

data = pd.read_csv(path, header=None, index_col=None)
data.columns = columns
data.sort_values(by=['total'], ascending=[top_k < 0], inplace=True)

timeline_show(data[selected_cols], selected_cols, top_k=5, figsize=(7.2, 12.8))
```


![png](output_9_0.png)


## 结论

- [x] 多worker高并发请求下，模型GPU推理部分仍然是OCR模型的瓶颈

## TODO
- [ ] OCR模型耗时与识别框数量关系分析
