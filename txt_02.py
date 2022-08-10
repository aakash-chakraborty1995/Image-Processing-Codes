# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 15:09:07 2022

@author: akash
"""
# 		strip_lines=line.strip()
# 		listli=strip_lines.split(",")
# 		print(listli)
# 		m=listl.append(listli)
# 	print(listl)

import cv2
import numpy as np
    
my_file = open("C:/Akash/Study/datasets/New_EAST_Dataset/test_gt/gt_img_6.txt") 
contents = my_file.read()
print(contents) 

my_file_1 =  open("C:/Akash/Study/datasets/New_EAST_Dataset/test_gt/gt_img_6.txt")
lines = len(my_file_1.readlines())
print('Total Number of lines:', lines)

my_file_2 =  open("C:/Akash/Study/datasets/New_EAST_Dataset/test_gt/gt_img_6.txt")
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
    image = cv2.imread('C:/Akash/Study/datasets/New_EAST_Dataset/result/img_80.jpg')
     
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
    cv2.imwrite('C:/Akash/Study/datasets/New_EAST_Dataset/result/img_81.jpg', res)