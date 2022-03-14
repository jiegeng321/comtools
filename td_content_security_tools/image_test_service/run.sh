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

