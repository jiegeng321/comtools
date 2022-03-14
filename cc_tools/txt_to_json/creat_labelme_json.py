import json
import os
import base64
import cv2
from tqdm import tqdm

def convert(img_dir, txt_path, json_path):
    with open(txt_path, "r+") as f:
        content = f.readline().strip(' ').split(' ')
        #print(len(content))
        #print(content)
        version = "4.5.6"
        flags = {}
        shapes = [
            {"label": "brow_l", "points": [[int(float(content[0])), int(float(content[1]))], [int(float(content[2])), int(float(content[3]))],
                                              [int(float(content[4])), int(float(content[5]))], [int(float(content[6])), int(float(content[7]))],
                                           [int(float(content[8])), int(float(content[9]))]],
             "group_id": "face_pts", "shape_type": "linestrip", "flags": {}},

            {"label": "brow_r", "points": [[int(float(content[10])), int(float(content[11]))], [int(float(content[12])), int(float(content[13]))],
                                              [int(float(content[14])), int(float(content[15]))], [int(float(content[16])), int(float(content[17]))],
                                            [int(float(content[18])), int(float(content[19]))]],
             "group_id": "face_pts", "shape_type": "linestrip", "flags": {}},

            {"label": "eyes_l", "points": [[int(float(content[20])), int(float(content[21]))], [int(float(content[22])), int(float(content[23]))],
                                              [int(float(content[24])), int(float(content[25]))], [int(float(content[26])), int(float(content[27]))],
                                           [int(float(content[28])), int(float(content[29]))], [int(float(content[30])), int(float(content[31]))]],
             "group_id": "face_pts", "shape_type": "polygon", "flags": {}},

            {"label": "eyes_r", "points": [[int(float(content[32])), int(float(content[33]))], [int(float(content[34])), int(float(content[35]))],
                                              [int(float(content[36])), int(float(content[37]))], [int(float(content[38])), int(float(content[39]))],
                                           [int(float(content[40])), int(float(content[41]))], [int(float(content[42])), int(float(content[43]))]],
             "group_id": "face_pts", "shape_type": "polygon", "flags": {}}
                ]

        # read image
        img_basename = os.path.basename(txt_path)
        img_name = img_basename[:-8] + ".jpg"
        #print(img_name)
        img_path = os.path.join(img_dir, img_name)
        img = cv2.imread(img_path)

        encoded = base64.b64encode(open(img_path, 'rb').read())

        anno = {"version": version, "flags": flags, "shapes": shapes, "imagePath": img_name,
                "imageData": encoded.decode(),
                "imageHeight": img.shape[0], "imageWidth": img.shape[1]}

        with open(json_path, "w+") as f:
            json.dump(anno, f, indent=4)


if __name__ == '__main__':
    base_dir = "face_pts_prelabel_2nd"

    img_dir = os.path.join(base_dir, 'face_pts_img_3rd')
    txt_dir = os.path.join(base_dir, 'face_pts_prelabel_txt_2nd')
    json_dir = os.path.join(base_dir, 'prelabel_json')

    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    txt_list = os.listdir(txt_dir)
    for file in tqdm(txt_list):

        if "txt" not in file or os.path.getsize(os.path.join(txt_dir, file)) == 0:
            continue
        #print(file)
        file_name, _ = os.path.splitext(file)
        json_path = os.path.join(json_dir, f"{file_name[:-4]}.json")

        convert(img_dir, os.path.join(txt_dir, file), json_path)
