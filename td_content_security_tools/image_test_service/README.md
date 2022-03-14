

# 图像内容测试工具

用于测试线上单个模型的web工具

## requirement
 - `python-opencv`
 - `tornado==5.0`

## 使用
 - 修改服务端口和容器名称 `vim run.sh`
   ```bash
    #!/bin/bash
    
    #### 镜像名称
    export IMAGES_NAME=ocr_online_test:1.0
    
    #### 容器名称
    export CONTAINER_NAME=ocr_online_test
    
    export PORT=8099
    
    #### 编译
    build() {
        docker rmi ${IMAGES_NAME}
        docker build -t ${IMAGES_NAME} .
    }
    
    #### 后台运行容器
    run() {
        docker run -d  \
               --restart=always \
               -p ${PORT}:8088 \
               -v /etc/localtime:/etc/localtime \
               --name=${CONTAINER_NAME} \
               ${IMAGES_NAME}
    }
    
    
    build
    run
   ```
 - 运行脚本启动服务`sh run.sh`
 
## TODO LIST
 - [ ] web 图片调用 （URL）


