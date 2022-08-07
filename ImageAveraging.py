# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 18:07:15 2022

@author: akash
"""
import numpy as np
import cv2 as cv
img = cv.imread('C:\Akash\Study\datasets\Satyajit Word Database\Aranyer0008\Aranyer0008_img_2.jpg')
kernel = np.ones((5,5),np.float32)/25
dst = cv.filter2D(img,-1,kernel)
cv.imwrite('C:\Akash\Study\datasets\Satyajit Word Database\Aranyer0008\Output_1.jpg', dst)