# -*- coding: utf-8 -*-
import subprocess
import os
import requests


def start_service():
    WORKER_NUM = os.environ.get('WORKER', 1)
    PORT_NUM = os.environ.get('PORT', 8088)
    SERVICE_ENTRANCE = os.environ.get('SERVICE_ENTRANCE', 'app')
    start_command = f"gunicorn -b 0.0.0.0:{PORT_NUM} -w {WORKER_NUM} -t 5000 {SERVICE_ENTRANCE}:app"
    try:
        AUTH_URL = os.environ.get('AUTH_HOST', '')
        auth_result = requests.get(
            f'http://{AUTH_URL}:8088/license/check', timeout=1)
    except Exception as e:
        print(str(e))
    else:
        if auth_result.ok:
            message = auth_result.json()
            success_res = message['success']
            if success_res:
                print('successed for authentication, start the service!')
                _ = subprocess.call(start_command, shell=True)
        else:
            print('failed to get license!')


if __name__ == '__main__':
    start_service()
