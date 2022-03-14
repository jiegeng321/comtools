#!/bin/bash

export APPNAME=ai-brand-logo-tm
export USER_HOME=/home/admin
export APP_HOME=${USER_HOME}/${APPNAME}
export APP_HOME=.
export MODEL_HOME=./model
export MODEL_LOCAL_PATH=${MODEL_HOME}
export MODEL_REMOTE_PATH=${APPNAME}/0.4/20210817_yolov5m_brand209_style345.onnx
export CONFIG_REMOTE_PATH=${APPNAME}/0.4/config.py
export MODEL_BUCKET=ai_vision
export S3_ACCESS_KEY=8KNQVOU27LTFQ32LD3DT
export S3_SECRET_KEY=VZM9KfGqFn6Q6DeYKY8wsR10l1K1DPWu8W4YA0JM
export S3_ENDPOINTS=http://s3.td:8080