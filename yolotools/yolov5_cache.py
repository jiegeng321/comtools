
import numpy as np
import torch
import warnings
warnings.filterwarnings("ignore")
from PIL import Image
import os.path as osp
from pathlib import Path
import sys
sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")
from mmdet.datasets.builder import DATASETS
from mmdet.datasets.custom import CustomDataset
from mmdet.datasets.dataset_wrappers import MultiImageMixDataset
from tqdm import tqdm

img_formats = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.dng']  # acceptable image suffixes


@DATASETS.register_module()
class Yolov5Dataset(CustomDataset):
    """XML dataset for detection.

        Args:
            min_size (int | float, optional): The minimum size of bounding
                boxes in the images. If the size of a bounding box is less than
                ``min_size``, it would be add to ignored field.
            img_subdir (str): Subdir where images are stored. Default: JPEGImages.
            ann_subdir (str): Subdir where annotations are. Default: Annotations.
        """


    def __init__(self,
                 min_size=32,
                 img_subdir="",
                 anno_subdir="",
                 cache = None,
                 **kwargs):

        assert self.CLASSES or kwargs.get(
            'classes', None), 'CLASSES in `Yolov5Dataset` can not be None.'

        self.img_subdir = img_subdir
        self.anno_subdir = anno_subdir
        self.min_size = min_size
        self.cache = cache
        super(Yolov5Dataset, self).__init__(**kwargs)
        self.cat2label = {cat: i for i, cat in enumerate(self.CLASSES)}

        if self.cache == "disk":
            print("disk cache")
            print(len(self.data_infos))
            print(len(self.valid_ids))
            print(self.data_infos[0])
        elif self.cache == "ram":
            self.DATA_RAM = []
            print("ram caching")
            for idx in tqdm(range(len(self.data_infos))):#len(self.data_infos)
                if self.test_mode:
                    self.DATA_RAM.append(self.prepare_test_img(idx))
                else:
                    while True:
                        data = self.prepare_train_img(idx)
                        if data is None:
                            idx = self._rand_another(idx)
                            continue
                        self.DATA_RAM.append(data)
                        break

        else:
            print("do not cache")


    def get_ann_info(self, idx):
        img_id = self.data_infos[idx]['id']
        txt_path = osp.join(self.ann_file, img_id + '.txt')
        target = np.loadtxt(txt_path).reshape(-1, 5)
        target = np.maximum(target, 0)
        bboxes_ignore = np.zeros((0, 4))
        labels_ignore = np.zeros((0,))
        if target.shape[0]!=0:
            x1 = (target[:, 1] - target[:, 3]/2)[:, np.newaxis]
            y1 = (target[:, 2] - target[:, 4]/2)[:, np.newaxis]
            x2 = (target[:, 1] + target[:, 3]/2)[:, np.newaxis]
            y2 = (target[:, 2] + target[:, 4]/2)[:, np.newaxis]
            bboxes = np.concatenate((x1, y1, x2, y2), 1).tolist()
            labels = target[:, 0].tolist()
        else:
            bboxes = np.zeros((0, 4))
            labels = np.zeros((0,))
        bboxes = np.array(bboxes, ndmin=2)
        labels = np.array(labels)
        ann = dict(
            bboxes=bboxes.astype(np.float32),
            labels=labels.astype(np.int64),
            bboxes_ignore=bboxes_ignore.astype(np.float32),
            labels_ignore=labels_ignore.astype(np.int64))
        return ann

    def get_cat_ids(self, idx):
        img_id = self.data_infos[idx]['id']
        txt_path = osp.join(self.ann_file, img_id + '.txt')
        target = np.loadtxt(txt_path).reshape(-1, 5)
        return target[:, 0].tolist()

    def load_annotations(self, ann_file):
        data_infos = []
        self.valid_ids = []
        img_files = [i for i in Path(self.img_prefix).rglob('*.*') if i.suffix.lower() in img_formats and i.is_file()]
        ignore_sum = 0
        for index, img_path in enumerate(img_files):
            if img_path.is_dir():
                continue
            filename = str(img_path)
            img_stem = img_path.stem
            txt_path = osp.join(self.ann_file, img_stem+'.txt')
            if not osp.exists(txt_path):
                ignore_sum += 1
                continue
            try:
                img = Image.open(img_path)
                img.verify()
                if img.format == 'GIF':
                    ignore_sum += 1
                    continue
                width, height = img.size
            except:
                if img is None:
                    continue
                ignore_sum += 1
                print(f"{str(img_path)} open error!")
                continue
            target = np.loadtxt(txt_path).reshape(-1, 5)
            data_infos.append(
                dict(id=img_stem, filename=filename, width=width, height=height))
            if min(width, height) < self.min_size:
                continue
            if self.filter_empty_gt:
                if target.shape[0]==0:
                    continue
            self.valid_ids.append(index - ignore_sum)

        return data_infos

    def __getitem__(self, idx):
        if self.cache:
            return self.DATA_RAM[idx]
        else:
            if self.test_mode:
                return self.prepare_test_img(idx)
            while True:
                data = self.prepare_train_img(idx)
                if data is None:
                    idx = self._rand_another(idx)
                    continue
                return data
    def _filter_imgs(self, min_size=32):
        return self.valid_ids


if __name__=="__main__":
    from functools import partial
    from mmcv.parallel import collate
    dataset_type = 'Yolov5Dataset'
    data_root = '/data02/xu.fx/dataset/PATTERN_DATASET/comb_data/yolodataset_pattern_18bs_25ks_0613/'
    img_norm_cfg = dict(mean=[0, 0, 0], std=[255., 255., 255.], to_rgb=True)

    #
    meta_keys = ['img_info', 'ann_info', 'img_prefix', 'seg_prefix', 'proposal_file', 'bbox_fields', 'mask_fields', 'seg_fields',
     'filename', 'ori_filename', 'img_shape', 'ori_shape', 'img_fields',  'gt_bboxes_ignore',
     'pad_shape', 'scale_factor']

    train_pipeline = [
        dict(type='LoadImageFromFile', to_float32=True),
        dict(type='LoadAnnotations', with_bbox=True, with_label=True, poly2mask=False, denorm_bbox=True),
        # dict(type='RandomFlip', flip_ratio=0.5),
        # dict(
        #     type='MinIoURandomCrop',
        #     min_ious=(0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
        #     min_crop_size=0.3),
        # dict(type='Mosaic', random_ratio=0.4, backend="pillow"),
        # dict(type='Resize', img_scale=[(320, 320), (608, 608)], keep_ratio=True),
        # dict(type='RandomFlip', flip_ratio=0.5),
        # dict(type='PhotoMetricDistortion'),
        dict(type='Normalize', **img_norm_cfg),
        # dict(type='Pad', size_divisor=32),
        # dict(type='DefaultFormatBundle'),

    ]

    train_pipeline2 = [
        dict(type='Mosaic', min_bbox_size=10),
        dict(type='MixUp', ),
        dict(type='Resize', img_scale=[(640, 640)], keep_ratio=False),
        dict(type='DefaultFormatBundle'),
        dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'], meta_keys=meta_keys)
        # dict(type='Collect', keys=['img'], meta_keys=meta_keys)
    ]



    class_ = ['gucci-h-1', 'michaelkors-h-1', 'coach-h-1', 'adidas-h-1', 'gucci-4', 'gucci-5', 'lv-h-1', 'fendi-h-1', 'lv-h-2', 'nike-4', 'lv-h-3', 'gucci-h-2', 'lv-h-4', 'versace-h-1', 'christian dior-h-1', 'goyard-h-1', 'burberry-h-1', 'Issey miyake-h-1', 'christian dior-h-2', 'celine-h-1', 'MCM-h-1', 'Reebok-h-4','bottega veneta-h-1', 'hermes-h-1', 'van cleef arpels-h-1']
    data = Yolov5Dataset(data_root=data_root, pipeline=train_pipeline, ann_file="JPEGImages/train/labels", img_prefix="./JPEGImages", img_subdir="./train/images", classes=class_, filter_empty_gt=False,cache="ram")

    # data = Yolov5Dataset(data_root, train_pipeline, 640, 8)

    dataset_mosaic = MultiImageMixDataset(data, train_pipeline2)
    #data = dataset_mosaic
    print(type(data))
    rest = data[1]
    print(rest)
    print(rest.keys())
    img = rest['img']
    print("gt_labels:", rest['gt_labels'])
    print("gt_bboxes:", rest['gt_bboxes'])
    print(type(img))
    print(img.shape)
    print("struct!!!")
    import cv2
    #img = img.data
    #print(type(img))
    print(np.mean(img))
    # temp = cv2.imread("/data01/erwei.wang/images_8.jpeg")
    # print(temp.shape)
    # img = torch.permute(img, (1, 2, 0)).numpy()
    # print(img.shape)
    # print(type(img[0][0][0]))
    # img = np.uint8(img)
    # # print(type(img[0][0][0]))
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #
    # for box in rest['gt_bboxes'].data:
    #     box = box.numpy()
    #     print(box)
    #     cv2.rectangle(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), [0, 255, 0], 1)
    # print(img.shape)
    # cv2.imwrite("tmp.jpg", img)
    # print("exit")


    # # dataloader test
    # from mmdet.datasets.samplers import GroupSampler
    # from mmcv.parallel import collate
    # sampler = GroupSampler(dataset_mosaic, 1)
    #
    # data_loader = DataLoader(
    #     dataset_mosaic,
    #     batch_size=2,
    #     num_workers=0,
    #     pin_memory=False,
    #     sampler=sampler,
    #     collate_fn=partial(collate, samples_per_gpu=2))
    #
    # # import pdb
    # # pdb.set_trace()
    # for i, res in enumerate(data_loader):
    #     print(f"第{i}次迭代")
    #     print(res.keys())
    #     print(res['img'].shape)
    #     print(res["img_metas"].data)
    #
    #
    #
    #     # print(f'图片shape为{res["imgs"].shape}')
    #     # print(f"target shape为{res['targets'].shape}")
    #     exit()






