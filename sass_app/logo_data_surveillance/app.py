#import falcon
from pathlib import Path
import os

#aim_dir = "{}/JPEGImages/train/images"
comb_data_dir = "/data01/xu.fx/dataset/dataset_stat.txt"
def get_dataset_num():
    with open(comb_data_dir, 'r') as fr:
        lines = fr.readlines()
    return lines

class DatasetManager(object):
    def on_get(self, req, resp):

        # implements your own func to get dataset stat
        lines = get_dataset_num()
        media = {}
        for line in lines:
            brandTortNum = int(len(os.listdir(line.split(" ")[-1].strip()))/2*0.8)
            media[line.split(" ")[0]] = brandTortNum
        #adsLogoNum = len(os.listdir(aim_dir.format(dirs[1])))
        media_ = media
        print(media_)
        #resp.status = falcon.HTTP_200

a=DatasetManager()
a.on_get(1,2)
#app = falcon.API()
#app.add_route('/brand_tm_dataset_stat', DatasetManager())
