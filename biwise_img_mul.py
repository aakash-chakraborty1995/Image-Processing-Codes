# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 15:04:32 2022

@author: akash
"""
import cv2
import numpy as np
    
# path to input images are specified and  
# images are loaded with imread command 
img1 = cv2.imread('C:/Akash/Study/datasets/New_EAST_Dataset/result/img_7.jpg') 
img2 = cv2.imread('C:/Akash/Study/datasets/New_EAST_Dataset/result/img_82.jpg')
 
# cv2.bitwise_and is applied over the
# image inputs with applied parameters
dest_and = cv2.bitwise_and(img2, img1, mask = None)
 
# the window showing output image
# with the Bitwise AND operation
# on the input images
cv2.imwrite('C:/Akash/Study/datasets/New_EAST_Dataset/result/img_8.jpg', dest_and)
  
