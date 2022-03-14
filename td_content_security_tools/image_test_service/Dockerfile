
FROM python:3.7.6-slim

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx && apt-get install -y libglib2.0-dev

WORKDIR /home/admin/playground

ADD . .

RUN pip install pip --upgrade -i https://mirror.baidu.com/pypi/simple
RUN pip install -r requirements.txt -i https://mirror.baidu.com/pypi/simple


EXPOSE 8088

CMD ["python", "service.py"]
# https://mirrors.aliyun.com/pypi/simple