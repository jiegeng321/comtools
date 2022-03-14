#!/bin/bash

#### 镜像名称
export IMAGES_NAME=brand_dataset_manager:0.2

#### 容器名称
export CONTAINER_NAME=brand_tm_traindata_surveillance

export PORT=9010
export HOME_DIR=/data01/xu.fx/


#### 编译
build() {
    docker rmi ${IMAGES_NAME}
    docker build -t ${IMAGES_NAME} .
}

## 后台启动容器
run() {
    docker run -d  \
            --restart=always \
           -p ${PORT}:8088 \
           -v ${HOME_DIR}:/data01/xu.fx/ \
           --name=${CONTAINER_NAME} \
           ${IMAGES_NAME}
}

# 脚本执行
build
run

