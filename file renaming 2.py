# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 17:31:53 2022

@author: akash
"""
import cv2
import glob

num = 1
# path = f"C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/test/img_{num}.jpg"



for i in range(1,102):
    path = f"C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/test/img_{num}.jpg"
    im = cv2.imread(path)
    cv2.imwrite("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/abc/new_img_"+str(num)+".jpg", im)
    num += 1

