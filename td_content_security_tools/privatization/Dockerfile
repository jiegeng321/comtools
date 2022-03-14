ARG PYTHON_VERSION=3.7.6
FROM python:${PYTHON_VERSION}-slim
WORKDIR /home/admin/playground
ADD . .
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -yy build-essential
RUN pip install Cython pycrypto -i https://mirrors.aliyun.com/pypi/simple
