### 简介
通过命令行方式与对象存储交互，实现上传、下载文件

### 依赖
- boto3

### 基本使用

1. 配置环境变量，包含accesskey等信息
```shell
source config.sh # 应用app目录中的相关环境变量配置
```
使用文档见 `python updown_model.py --help` 
```
usage: updown_model.py [-h] -l LOCAL_DIR -b BUCKET -r REMOTE_DIR -a
                       {upload,download}

download/upload file to object storage service

optional arguments:
  -h, --help            show this help message and exit
  -l LOCAL_DIR, --local LOCAL_DIR
                        local file dir
  -b BUCKET, --bucket BUCKET
                        bucket name
  -r REMOTE_DIR, --remote REMOTE_DIR
                        remote file dir
  -a {upload,download}, --action {upload,download}
                        upload or download
```

2. 上传文件
```shell
python updown_model --action upload --local xxx.onnx --remote ai-logo-gen/v1.5/xxx.onnx
```
3. 下载文件
```shell
python updown_model --action download --local model/ --remote ai-logo-gen/v1.5/
```

**注意**
当前版本上传是文件为单位， 下载是文件夹为单位