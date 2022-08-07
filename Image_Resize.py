# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 15:48:53 2022

@author: akash
"""
import cv2
 
img = cv2.imread('C:\Akash\Database\Satyajit\devi0008.jpg', cv2.IMREAD_UNCHANGED)
 
print('Original Dimensions : ', img.shape)
 
scale_percent_1 = 24.25
scale_percent_0 = 16 # percent of original size
width = int(img.shape[1] * scale_percent_1 / 100)
height = int(img.shape[0] * scale_percent_0 / 100)
dim = (width, height)
  
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
 
print('Resized Dimensions : ',resized.shape)
 
cv2.imwrite('C:\Akash\Database\Satyajit\Resized_image.jpg', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()