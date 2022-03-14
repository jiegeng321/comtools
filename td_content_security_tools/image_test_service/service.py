#-*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Name    : service.py
Author  : lijun.chen
Contect : lijun.chen@tongdun.net
Time    : 2020-12-08 14:31
Desc    :
"""


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
from tornado.options import define, options

import json
import os
import time
import requests
import numpy as np
import cv2
import traceback


def get_rotate_crop_image(img, points):
    '''
    img_height, img_width = img.shape[0:2]
    left = int(np.min(points[:, 0]))
    right = int(np.max(points[:, 0]))
    top = int(np.min(points[:, 1]))
    bottom = int(np.max(points[:, 1]))
    img_crop = img[top:bottom, left:right, :].copy()
    points[:, 0] = points[:, 0] - left
    points[:, 1] = points[:, 1] - top
    '''
    img_crop_width = int(max(np.linalg.norm(points[0] - points[1]),
                             np.linalg.norm(points[2] - points[3])))
    img_crop_height = int(max(np.linalg.norm(points[0] - points[3]),
                              np.linalg.norm(points[1] - points[2])))
    pts_std = np.float32([[0, 0],
                          [img_crop_width, 0],
                          [img_crop_width, img_crop_height],
                          [0, img_crop_height]])
    M = cv2.getPerspectiveTransform(points, pts_std)
    dst_img = cv2.warpPerspective(img, M, (img_crop_width, img_crop_height),
                                  borderMode=cv2.BORDER_REPLICATE,
                                  flags=cv2.INTER_CUBIC)
    dst_img_height, dst_img_width = dst_img.shape[0:2]
    if dst_img_height * 1.0 / dst_img_width >= 1.5:
        dst_img = np.rot90(dst_img)
    return dst_img

##########################################################################

def call_ocr_binary(image_data, url):


    sessionF = requests.session()

    while True:
        try:
            # print('send request')
            req = sessionF.post(url, data=image_data, headers=None)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    ret = json.loads(req.text)

    return ret


def test_vis_show(image_data, img, url='https://ai-adver-ocr-accstg.tongdun.cn/upload_binary'):


    ret = call_ocr_binary(image_data, url)
    # print(ret['ocr_str'])

    polys = []
    color = np.linspace(128, 255, len(ret['textline']))
    for i, text in enumerate(ret['textline']):
        poly = [v for v in text['poly']]
        poly = np.array(poly).reshape((-1, 1, 2)).astype('int')

        polys.append(poly)

        # print(text['text'])



    for i, pts in enumerate(polys):
        _img = get_rotate_crop_image(img, pts.reshape((4, 2)).astype('float32'))
        cv2.imwrite('data/{}.jpg'.format(i), _img)

    mask = np.zeros_like(img)
    for poly in polys:
        cv2.fillPoly(mask, [poly], (1, 1, 1))

    img2 = np.uint8(img * mask + (1 - mask) * 255)
    # img2 = np.uint8(mask*255)

    h, w = img2.shape[:2]

    border = np.array([0, 0, w, 0, w, h, 0, h]).reshape((-1, 1, 2)).astype('int')
    img2 = cv2.polylines(img2, [border], True, (50, 50, 50), 2)

    img = cv2.polylines(img, polys, True, (0, 0, 255), 2)
    cv2.imwrite('data/{}.jpg'.format('src'), img)

    axis = 1 if h >= w else 0
    new_img = np.concatenate([img, img2], axis=axis)

    return new_img, ret

##########################################################################


def get_now_timestamp_str():
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))



port = 8088
define("port", default=port, help="run on the given port", type=int)

cur_path = os.path.dirname('__file__')  # current path
__PAGE__ = os.path.join(cur_path, 'index/')  # storage path for demo page


def get_now_time_ms():
    return int(time.time() * 1000)

class ImageBuff:
    def __init__(self):
        self.data = None
        self.done = False


class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.render('index/index.html')
        print('GET', self.request.remote_ip )




# image comes from my frontend page
class UploadHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        response = {
            "msg": "",
            "status": 200,
            "textline": [],
            "ocr_str": "NULL",
            "textline_num": 0,
            "alg_cost": "0ms",
            "infos": None
        }

        # 应用预发网址
        url_maps = {
            'ai-adver-ocr': 'https://ai-adver-ocrhzstg.tongdun.cn/upload_binary',
            'ai-adver-ocr-acc': 'https://ai-adver-ocr-accstg.tongdun.cn/upload_binary',
            'other': "http://0.0.0.0:8088"
        }

        image_buff.done = False

        try:

            binray_file = self.request.files['pic'][0]['body']
            method = self.get_argument('method')
            if method not in url_maps.keys():
                method = 'ai-adver-ocr-acc'

            if method == 'other':
                url_maps[method] = self.get_argument('url')

            # print(url_maps)
            print('POST', method, self.request.remote_ip)

            ####
            img_data_raw = np.asarray(bytearray(binray_file), dtype='uint8')
            img = cv2.imdecode(img_data_raw, cv2.IMREAD_COLOR)


            ### process
            img, ret = test_vis_show(binray_file, img, url=url_maps[method])

            img_encoded = cv2.imencode('.png', img)[1]
            img_encoded = np.array(img_encoded).tobytes()
            image_buff.data = img_encoded

            # 本信息回传列表，前端将回传的文本按顺序列出（也可以设置logo类别信息）
            textline = [v['text'] for v in ret['textline']]
            response['ocr_str'] = " ".join(textline)
            response['textline'] = textline
            response['alg_cost'] = ret['alg_cost']
            response['textline_num'] = ret['textline_num']
            print(response['ocr_str'])
        except Exception as e:
            traceback.print_exc()
        image_buff.done = True

        self.finish(response)


class ShowHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        # print('show', image_buff.done)

        total_cnt = 1000
        cnt = 0
        while cnt < total_cnt and (not image_buff.done):
            time.sleep(0.1)
            cnt += 1

        if cnt > total_cnt:
            image_buff.done = True


        if image_buff is not None:
            self.write(image_buff.data)
        else:
            self.write('Error')


# health check
class HealthHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('ok')

    def head(self):
        self.set_status(200)

def start_server():
    NUM_WORKERS = 2

    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/upload", UploadHandler),
            (r"/show", ShowHandler),
            (r"/ok", HealthHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': __PAGE__})
        ]
    )
    sockets = tornado.netutil.bind_sockets(options.port)
    fork_id = tornado.process.fork_processes(NUM_WORKERS)

    global image_buff
    image_buff = ImageBuff()


    # listen port
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.add_sockets(sockets)
    print("worker {} start listening port {}".format(fork_id, port))
    tornado.ioloop.IOLoop.instance().start()



if __name__ == '__main__':
    start_server()



