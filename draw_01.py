# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 20:42:32 2022

@author: akash
"""
import cv2
import numpy as np
  
# creating an array using np.full 
# 255 is code for white color
img = np.full((720, 1280, 3),
                        255, dtype = np.uint8)
  
# displaying the image
cv2.imwrite('C:/Akash/Study/datasets/New_EAST_Dataset/result/img_82.jpg', img)
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
 