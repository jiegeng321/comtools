import falcon
from pathlib import Path
from loguru import logger
import imghdr
import os
import time

#### 实现数据集数据统计 ---------------------------------------- todo

def get_image_num(p):

    cnt = 0
    for fn in os.listdir(p):
        ext = imghdr.what(os.path.join(p, fn))
        if ext is not None and ext.upper() in ['JPG', 'JPEG', 'PNG', 'BMP']:
            cnt += 1
    return cnt

def get_dataset_num(paths):

    datasets = [
        "/home/lijun.clj/data/public_datasets/mtwi2018_det_icdar/gt_images",   # 10048
        # "ICDAR2015",            # 1000
        "/home/lijun.clj/data/public_datasets/ICDAR2017_RCTW/gt_images",       # 8034
        "/home/lijun.clj/data/public_datasets/ICDAR2017_MLT/gt_images",        # 7200
        "/home/lijun.clj/data/public_datasets/ICDAR2019_LSVT/gt_images",        # 30000
        "/home/lijun.clj/data/iceberg_labeling/episode-1/ocr_sample20210709",
        "/home/lijun.clj/data/iceberg_labeling/episode-2/td_ocr20210812",
        "/home/lijun.clj/data/iceberg_labeling/episode-3/td_ocr20210830",
        "/home/lijun.clj/data/iceberg_labeling/episode-4/td_ocr20210903",
        "/home/lijun.clj/data/iceberg_labeling/episode-5/td_ocr20210914",
    ]



    total_cnt = 0
    dataset_cnt = {}
    for p in datasets:

        cnt = 0
        try:
            cnt = get_image_num(p)
            print(p, cnt)
        except:
            print('{} not exists'.format(p))
            cnt = 0

        dataset_cnt[p] = cnt
        total_cnt += cnt

    return total_cnt, dataset_cnt

class DatasetManager(object):
    def on_get(self, req, resp):

        # implements your own func to get dataset stat
        tic = time.time()
        total_cnt, dataset_cnt = get_dataset_num([])  # ---------------- todo
        toc = time.time()
        logger.info("client ip: {} | dataset_num: {}".format(req.remote_addr, total_cnt))
        resp.media = {
            'ocr': total_cnt,
            # 'time_elapsed': round(toc-tic, 2),
            # 'profile': dataset_cnt,
        }
        resp.status = falcon.HTTP_200


app = falcon.API()
app.add_route('/ocr_dataset_stat', DatasetManager()) # ------ todo




