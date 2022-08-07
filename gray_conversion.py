# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:50:23 2019

@author: AKASH_95
"""


import cv2


img = cv2.imread("G:\Data\\pic_3.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
cv2.imshow('Original image',img)
cv2.imshow('Gray image', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("G:/data_a/pic_3_gray.jpg",gray)    
