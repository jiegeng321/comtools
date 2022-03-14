#!/bin/bash

#### 镜像名称
export IMAGES_NAME=logo_detect_server_for_one_img:0.1

#### 容器名称
export CONTAINER_NAME=logo_detect_server_for_one_img

export PORT=55904
export HOME_DIR=/data01/xu.fx/my_app/logo_detect_server_for_one_img


#### 编译
build() {
    docker rmi ${IMAGES_NAME}
    docker build -t ${IMAGES_NAME} .
}

## 后台启动容器
run() {
    docker run -it \
           -p ${PORT}:8088 \
           -v ${HOME_DIR}:/data01/xu.fx/my_app/logo_detect_server_for_one_img \
           --name=${CONTAINER_NAME} \
           ${IMAGES_NAME}
}

# 脚本执行
build
run

