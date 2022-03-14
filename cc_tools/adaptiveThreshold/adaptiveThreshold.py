# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test2.jpg', 0)  # 0是第二个参数，将其转为灰度图

#img = cv2.medianBlur(img, 1)
ret, th1 = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

# 11 为 邻域大小,   2为C值，常数
th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                            cv2.THRESH_BINARY, 7, 5)
th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                            cv2.THRESH_BINARY, 7, 5)

titles = ['Original Image', 'Global Thresholding (v = 200)',
          'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]
for i in range(4):
    plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])

plt.show()
