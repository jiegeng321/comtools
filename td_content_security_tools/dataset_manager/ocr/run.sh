#!/bin/bash

#### 镜像名称
export IMAGES_NAME=ocr_dataset_manager:0.1

#### 容器名称
export CONTAINER_NAME=ocr_dataset_manager_server

export PORT=9009
export DATASET_DIR=/home/lijun.clj/data/public_datasets
export DATASET2_DIR=/data02/lijun.clj/iceberg_labeling


#### 编译
build() {
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
    docker rmi ${IMAGES_NAME}
    docker build -t ${IMAGES_NAME} .
}

#### 后台运行容器
run() {
    docker run -d  \
           --restart=always \
           -p ${PORT}:8088 \
           -v /etc/localtime:/etc/localtime \
           -v ${DATASET_DIR}:/home/lijun.clj/data/public_datasets \
           -v ${DATASET2_DIR}:/home/lijun.clj/data/iceberg_labeling \
           --name=${CONTAINER_NAME} \
           ${IMAGES_NAME}
}


build
run

