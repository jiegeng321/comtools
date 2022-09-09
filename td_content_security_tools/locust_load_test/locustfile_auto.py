from locust import HttpUser, task, between
from locust import LoadTestShape
from pathlib import Path
import random
def is_img(img_name):
    if str(img_name).split(".")[-1].lower() in ["jpg","png","jpeg"]:
        return True
    else:
        return False
image_list = [p for p in Path('./fordeal_test_image_4k').rglob('*.jpg')]
#image_list = [p for p in Path('./dh_val_image').rglob('*.*') if is_img(p)]
#image_list1 = [p for p in Path("/data01/xu.fx/dataset/LOGO_DATASET/fordeal_test_data_total/brand_total_raw_data").rglob('*.*') if is_img(p)]
#image_list2 = [p for p in Path("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_data_for_logo_test").rglob('*.*') if is_img(p)]
#image_list3 = [p for p in Path("/data01/xu.fx/dataset/LOGO_DATASET/white_data/").rglob('*.*') if is_img(p)]
#image_list = [p for p in Path("/data01/xu.fx/dataset/PATTERN_DATASET/fordeal_test_data/fordeal_0930_raw_data").rglob('*.*') if is_img(p)]
#image_list = image_list1 + image_list2 + image_list3 + image_list4
print(f'There are {len(image_list)} images for load testing.')


class UserBehavior(HttpUser):
    wait_time = between(0.001, 0.002)

    def on_start(self):
        pass

    # the @task takes an optional weight argument.
    @ task(1)
    def logo_recognize(self):
        image_idx = random.randint(0, len(image_list)-1)
        image_path = image_list[image_idx]

        with open(image_path, 'rb') as imageFile:
            data = imageFile.read()
        data = {'img': data, 'imageId': 'xxxxx'}
        r = self.client.post('/v2/cartoon_rec', files=data)


class StageShape(LoadTestShape):
    # time_limit = 600
    stages = [
        {"duration": 120, "user": 20, "spawn_rate": 10},
        {"duration": 240, "user": 40, "spawn_rate": 10},
        {"duration": 360, "user": 80, "spawn_rate": 10},
        {"duration": 480, "user": 120, "spawn_rate": 10},
        {"duration": 600, "user": 160, "spawn_rate": 10},
        {"duration": 800, "user": 200, "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()%800
        for stage in self.stages:
            if run_time < stage['duration']:
                tick_data = (stage['user'], stage['spawn_rate'])
                return tick_data

        return None
