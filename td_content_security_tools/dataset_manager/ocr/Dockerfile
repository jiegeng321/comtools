
FROM python:3.7.6-slim

WORKDIR /home/admin/playground

RUN pip install falcon==2.0 gunicorn loguru -i https://mirror.baidu.com/pypi/simple

ADD app.py .

EXPOSE 8088

CMD ["gunicorn", "-b", "0.0.0.0:8088", "-w", "1", "app:app", "-t", "30000"]
# https://mirrors.aliyun.com/pypi/simple