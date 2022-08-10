# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 21:08:06 2022

@author: akash
"""

import cv2
import numpy as np
    
my_file = open("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/gt_img_6.txt") 
contents = my_file.read()
print(contents) 

my_file_1 =  open("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/gt_img_6.txt")
lines = len(my_file_1.readlines())
print('Total Number of lines:', lines)

my_file_2 =  open("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/gt_img_6.txt")
list1 = []
for line in my_file_2:
    strip_lines=line.strip()
    listli = strip_lines.split(",")
    print(listli)
    m = list1.append(listli)
print(list1)
list2=list(list1)
print(list2)
res = np.full((720, 1280, 3),
                        0, dtype = np.uint8)
for i in list2:
    a1 = list(i[0:2])
    a2 = list(i[2:4])
    a3 = list(i[4:6])
    a4 = list(i[6:8])
    print(a1,a2,a3,a4)
    
    
    # Reading an image in default
    # mode
    image = np.full((720, 1280, 3),
                            0, dtype = np.uint8)
     
    # Window name in which image is
    # displayed
    window_name = 'Image'
     
    # Polygon corner points coordinates
    pts = np.array([a1,a2,a3,a4],
                   np.int32)
     
    pts = pts.reshape((-1, 1, 2))
     
    isClosed = True
     
    # Blue color in BGR
    color = (0, 0, 255)
    color1 = (255,0,0)
     
    # Line thickness of 2 px
    thickness = 2
     
    # Using cv2.polylines() method
    # Draw a Blue polygon with
    # thickness of 1 px
    image = cv2.polylines(image, [pts],
                          isClosed, color, thickness)
    image = cv2.fillPoly(image, [pts], color1)
    res += image
    cv2.imwrite('C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/img_6_1.jpg', res)
    
im = cv2.imread('C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/img_6.jpg')

im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gray_1 = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

th, im_gray_th_otsu = cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)
th1, im_gray_th = cv2.threshold(im_gray_1, 128, 192, cv2.THRESH_OTSU)
print(th,th1)
# 117.0

cv2.imwrite('C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/img_6_2.jpg', im_gray_th_otsu)
cv2.imwrite('C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/img_6_3.jpg', im_gray_th)   

dest_and = cv2.bitwise_and(im_gray_th, im_gray_th_otsu, mask = None) 

cv2.imwrite('C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/img_6_mask.jpg', dest_and)
    
    
    
    

     

    
