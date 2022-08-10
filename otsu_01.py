# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:48:46 2022

@author: akash
"""
import cv2

im = cv2.imread('C:/Akash/Study/datasets/New_EAST_Dataset/result/img_7.jpg')

im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

th, im_gray_th_otsu = cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)

print(th)
# 117.0

cv2.imwrite('C:/Akash/Study/datasets/New_EAST_Dataset/result/img_8.jpg', im_gray_th_otsu)
