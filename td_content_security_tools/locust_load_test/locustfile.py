from locust import HttpUser, task, between
from locust import LoadTestShape
from pathlib import Path
import random

image_list = [p for p in Path('./test_image').rglob('*.jpg')]
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
        r = self.client.post('/upload', files=data)


