#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""
import os
import pickle
import random

import numpy as np
from abc import ABCMeta, abstractmethod

class Evaluation(metaclass=ABCMeta):

    def __init__(self, class_name, det_boxes, root="./tmp"):
        """
        all_boxes = {"class_name":{"image_name": np.array of shape #dets x 5 }}
        val_boxes = {"image_name": np.array of shape #dets x 5}
        :param class_name:
        :param det_boxes:
        :param val_boxes:
        :param root:
        """
        self.root = root
        self.class_name = class_name
        self.det_boxes = det_boxes
        self.get_valboxes()

    def voc_ap(self, rec, prec, use_07_metric=False):
        """Compute VOC AP given precision and recall. If use_07_metric is true, uses
        the VOC 07 11-point method (default:False).
        """
        if use_07_metric:
            # 11 point metric
            ap = 0.
            for t in np.arange(0., 1.1, 0.1):
                if np.sum(rec >= t) == 0:
                    p = 0
                else:
                    p = np.max(prec[rec >= t])
                ap = ap + p / 11.
        else:
            # correct AP calculation
            # first append sentinel values at the end
            mrec = np.concatenate(([0.], rec, [1.]))
            mpre = np.concatenate(([0.], prec, [0.]))

            # compute the precision envelope
            for i in range(mpre.size - 1, 0, -1):
                mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

            # to calculate area under PR curve, look for points
            # where X axis (recall) changes value
            i = np.where(mrec[1:] != mrec[:-1])[0]

            # and sum (\Delta recall) * prec
            ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
        return ap

    def voc_eval(self, detpath,
                 classname,
                 cachedir,
                 ovthresh=0.5,
                 use_07_metric=False):
        """rec, prec, ap = voc_eval(detpath,
                                    annopath,
                                    imagesetfile,
                                    classname,
                                    [ovthresh],
                                    [use_07_metric])
        Top level function that does the PASCAL VOC evaluation.
        detpath: Path to detections
            detpath.format(classname) should produce the detection results file.
        annopath: Path to annotations
            annopath.format(imagename) should be the xml annotations file.
        imagesetfile: Text file containing the list of images, one image per line.
        classname: Category name (duh)
        cachedir: Directory for caching the annotations
        [ovthresh]: Overlap threshold (default = 0.5)
        [use_07_metric]: Whether to use VOC07's 11 point AP computation
            (default False)
        """
        # assumes detections are in detpath.format(classname)
        # assumes annotations are in annopath.format(imagename)
        # assumes imagesetfile is a text file with each line an image name
        # cachedir caches the annotations in a pickle file

        # extract gt objects for this class
        sml = [0, 0, 0]
        class_recs = {}
        npos = 0
        for imagename in self.image_names:
            R = [obj for obj in self.val_boxes[imagename] if obj['name'] == classname]
            bbox = np.array([x['bbox'] for x in R])
            # area = np.array([(x['bbox'][3]-x['bbox'][1])*(x['bbox'][2]-x['bbox'][0]) for x in R])
            # if area.shape[0]!=0:
            #     print(area)
            #     print(np.array(area<=32*32))
            #     sml[0] += sum(area<=32*32)
            #     # print(np.array(area>32*32 and area<=96*96))
            #     sml[1] += sum(area>32*32 and area<=96*96)
            #     sml[2] += sum(area>96*96)
            difficult = np.array([x['difficult'] for x in R]).astype(np.bool)
            det = [False] * len(R)
            npos = npos + sum(~difficult)
            class_recs[imagename] = {'bbox': bbox,
                                     'difficult': difficult,
                                     'det': det}
        # print(sml)
        # read dets
        detfile = detpath.format(classname)
        with open(detfile, 'r') as f:
            lines = f.readlines()

        splitlines = [x.strip().split('\t') for x in lines]
        image_ids = [x[0] for x in splitlines]
        confidence = np.array([float(x[1]) for x in splitlines])
        BB = np.array([[float(z) for z in x[2:]] for x in splitlines])

        # sort by confidence
        sorted_ind = np.argsort(-confidence)
        BB = BB[sorted_ind, :]
        image_ids = [image_ids[x] for x in sorted_ind]

        # go down dets and mark TPs and FPs
        nd = len(image_ids)
        tp = np.zeros(nd)
        fp = np.zeros(nd)
        for d in range(nd):
            R = class_recs[image_ids[d]]
            bb = BB[d, :].astype(float)
            ovmax = -np.inf
            BBGT = R['bbox'].astype(float)
            if BBGT.size > 0:
                # compute overlaps
                # intersection
                ixmin = np.maximum(BBGT[:, 0], bb[0])
                iymin = np.maximum(BBGT[:, 1], bb[1])
                ixmax = np.minimum(BBGT[:, 2], bb[2])
                iymax = np.minimum(BBGT[:, 3], bb[3])
                iw = np.maximum(ixmax - ixmin + 1., 0.)
                ih = np.maximum(iymax - iymin + 1., 0.)
                inters = iw * ih

                # union
                uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
                       (BBGT[:, 2] - BBGT[:, 0] + 1.) *
                       (BBGT[:, 3] - BBGT[:, 1] + 1.) - inters)

                overlaps = inters / uni
                ovmax = np.max(overlaps)
                jmax = np.argmax(overlaps)

            if ovmax > ovthresh:
                if not R['difficult'][jmax]:
                    if not R['det'][jmax]:
                        tp[d] = 1.
                        R['det'][jmax] = 1
                    else:
                        fp[d] = 1.
            else:
                fp[d] = 1.

        # compute precision recall
        fps = sum(fp)
        tps = sum(tp)
        fp = np.cumsum(fp)
        tp = np.cumsum(tp)
        rec = tp / float(npos)
        recs = tps / float(npos)
        # avoid divide by zero in case the first detection matches a difficult
        # ground truth
        prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)
        precs = tps / (tps + fps)
        ap = self.voc_ap(rec, prec, use_07_metric)
        return recs, precs, ap

    def evaluate_detections(self, output_dir=None):
        """
        all_boxes is a list of length number-of-classes.
        Each list element is a list of length number-of-images.
        Each of those list elements is either an empty list []
        or a numpy array of detection.
        all_boxes = {"class_name":{"image_name": np.array of shape #dets x 5 }}
        """
        self._write_voc_results_file()
        self._do_python_eval(output_dir)

    def _get_voc_results_file_template(self):
        filename = 'comp3_det_test' + '_{:s}.txt'
        filedir = os.path.join(self.root, 'results')
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        path = os.path.join(filedir, filename)
        return path

    @abstractmethod
    def get_valboxes(self):
        """
        self.val_boxes = {"image_name": [{"bbox":[xmin, ymin,xmax, ymax], "name":LOGO, "diffict":0}, {...}]}
        :return:
        """
        self.val_boxes = {}
        pass

    def _write_voc_results_file(self):
        for cls_ind, cls in enumerate(self.class_name):
            if cls == '__background__':
                continue
            print('Writing {} VOC results file'.format(cls))
            filename = self._get_voc_results_file_template().format(cls)
            with open(filename, 'wt') as f:
                for img_dex, value in self.det_boxes.items():
                    if value.shape[0]==0:
                        continue
                    for k in range(value.shape[0]):
                        if self.class_name[int(value[k, -1])] == cls and random.random()>=0:
                            f.write(
                            '{:s}\t{:.3f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\n'.format(
                                img_dex, value[k, -2], value[k, 0]+(random.random()*0),
                                                    value[k, 1]+(random.random()*0), value[k, 2]+(random.random()*0),
                                                    value[k, 3]+(random.random()*0)))

    def _do_python_eval(self, output_dir='output'):
        # rootpath = os.path.join(self.root, 'VOC' + self._year)
        # name = self.image_set[0][1]
        # annopath = os.path.join(rootpath, 'Annotations', '{:s}.xml')
        # imagesetfile = os.path.join(rootpath, 'ImageSets', 'Main',
        #                             name + '.txt')
        # cachedir = os.path.join(self.root, 'annotations_cache')
        aps = []
        # # The PASCAL VOC metric changed in 2010
        use_07_metric = False
        # print('VOC07 metric? ' + ('Yes' if use_07_metric else 'No'))
        # if output_dir is not None and not os.path.isdir(output_dir):
        #     os.mkdir(output_dir)

        print('Results:')
        print("| {} | {:<5} | {:<5} | {:<6} |".format("classname", "recall", 'precision','ap'))
        print('|' + '-----------|' + '--------|'+'-----------|' +'--------|')
        for i, cls in enumerate(self.class_name):
            if cls == '__background__':
                continue

            filename = self._get_voc_results_file_template().format(cls)
            rec, prec, ap = self.voc_eval(
                filename,
                cls,
                None,
                ovthresh=0.5,
                use_07_metric=use_07_metric)
            aps += [ap]
            print("| {:9} | {:<5} | {:<9} | {:<6} |".format(cls,round(rec,4), round(prec, 4), round(ap, 4)))
            if output_dir is not None:
                with open(os.path.join(output_dir, cls + '_pr.pkl'),
                          'wb') as f:
                    pickle.dump({'rec': rec, 'prec': prec, 'ap': ap}, f)
        print('Mean AP = {:.4f}'.format(np.mean(aps)))

        print('')
        print('--------------------------------------------------------------')
        print('Results computed with the **unofficial** Python eval code.')
        print('Results should be very close to the official MATLAB eval code.')
        print('Recompute with `./tools/reval.py --matlab ...` for your paper.')
        print('-- Thanks, The Management')
        print('--------------------------------------------------------------')

 # ['998209.jpeg', '0.685', '1.0', '47.0', '41.0', '232.0'], ['998209.jpeg', '1.000', '1.0', '86.0', '349.0', '200.0']['998209.jpeg', '0.982', '1.0', '581.0', '377.0', '690.0']