#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 00:14:58 2022

@author: heisenberg
"""

import cv2
  
img = cv2.imread("/home/heisenberg/Study/Database/EAST_Dataset/Cropped/test_1.jpg")
print(type(img))
  
# Shape of the image
print("Shape of the image", img.shape)
  
# [rows, columns]
crop = img[358:377, 74:106]   #57, 667,247, 668,244, 708,56, 708 h
                               #75, 360,106, 358,106, 377,74, 376 p
  
cv2.imwrite("/home/heisenberg/Study/Database/EAST_Dataset/Cropped/cropped_text_4.jpg", crop)
