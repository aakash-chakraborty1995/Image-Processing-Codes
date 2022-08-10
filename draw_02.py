# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 20:47:34 2022

@author: akash
"""
# Python program to explain
# cv2.polylines() method
 
import cv2
import numpy as np
 
# path

 
# Reading an image in default
# mode
image = cv2.imread('C:/Akash/Study/datasets/New_EAST_Dataset/result/img_80.jpg')
 
# Window name in which image is
# displayed
window_name = 'Image'
 
# Polygon corner points coordinates
pts = np.array([[25, 70], [25, 160],
                [110, 200], [200, 160],
                [200, 70], [110, 20]],
               np.int32)
 
pts = pts.reshape((-1, 1, 2))
 
isClosed = True
 
# Blue color in BGR
color = (255, 0, 0)
 
# Line thickness of 2 px
thickness = 2
 
# Using cv2.polylines() method
# Draw a Blue polygon with
# thickness of 1 px
image = cv2.polylines(image, [pts],
                      isClosed, color, thickness)
 
# Displaying the image
cv2.imshow('image', image)
cv2.waitKey()   
cv2.destroyAllWindows()