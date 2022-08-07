# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 13:45:39 2022

@author: akash
"""
import cv2
import numpy as np
import glob


path = "C:/Akash/Study/datasets/Satyajit Word Database/train_img_1/*.*"
img_number = 1

for file in glob.glob(path):
    print(file)
    
    img = cv2.imread(file)
    resized = cv2.resize(img, (1280, 720), interpolation = cv2.INTER_NEAREST)
   
    
    
    cv2.imwrite("C:/Akash/Study/datasets/Satyajit Word Database/train_img_2/train_img_"+str(img_number)+".jpg", resized)
    img_number +=1