### 初次私有化部署镜像生成流程
1. 代码中通过增加环境变量`is_private`, 控制加载加密模型。
2. 确认基础镜像的python版本，在registry中查看是否存在， 若不存在，根据`Dockerfile`生成py2so镜像（只需生成一次）
3. 参考`Dockerfile.private.example`, 对已有sass程序进行改造，兼容pass部署。采用multistage build方式，一键完成模型加密、授权导入、代码加密等加固环节
4. 后续如果基础框架不做改动，模型更新直接重新构建即可:  `docker build -f Dockerfile.private --build-args PYTHON_VERSION=py3.8`

#### sass程序代码兼容pass私有化部署示例
##### onnxruntime
```python
# when load trained model file
model_path = 'xxx.onnx' 
is_private = os.environ.get('PRIVATE', Fasle)
with open(model_path, 'rb') as f:
  model_data = f.read()
  if is_private: # decrypt model in private deployment scene
    from encrypter import AEScoder
    aes_decrypter = AEScoder()
    model_data = aes_decrypter.decrypt(model_data)
  model = ort.InferenceServer(model_data, ...)
```
##### tensorrt
```python
model_path = 'xxx.onnx' 
is_private = os.environ.get('PRIVATE', Fasle)

with open(engine_file_path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
  model_data = f.read()
    if is_private: # decrypt model in private deployment scene
      from encrypter import AEScoder
      aes_decrypter = AEScoder()
      model_data = aes_decrypter.decrypt(model_data)
  return runtime.deserialize_cuda_engine(model_data)
```

### 镜像构建
### python 3.8
```shell
docker build -t registry.tongdun.me/xdsec/privatization:py3.8-0.1 . --build-arg PYTHON_VERSION=3.8.5 # for tensorrt.base
```
#### python 3.7
```shell
docker build -t registry.tongdun.me/xdsec/privatization:py3.7-0.1 . --build-arg PYTHON_VERSION=3.7.6
```
#### python3.6
```shell
docker build -t registry.tongdun.me/xdsec/privatization:py3.6-0.2 . --build-arg PYTHON_VERSION=3.6.9  # for onnxruntime base
```

### 功能描述
1. 使用py2so将python脚本编译为so文件，起到加密作用


### 使用方法：
```shell
python py2so.py --help
usage: py2so.py [-h] [--build_dir BUILD_DIR] [--source_dir SOURCE_DIR]

optional arguments:
  -h, --help            show this help message and exit
    --build_dir BUILD_DIR
      --source_dir SOURCE_DIR
```

### 参数：
- source_dir: 要加固的文件夹路径
- build_dir: 编译文件夹

编译后在build_dir下会生成同名的文件夹，保持原文件目录结构
