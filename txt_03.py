# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 21:08:06 2022

@author: akash
"""

import cv2
import numpy as np
import glob


path = "C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/gt/*.txt"
path_1 = "C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/test/*.jpg"
img_num = 1
img_num_bz = 1

for file in glob.glob(path):
    my_file =  open(file)
    list1 = []
    for line in my_file:
        strip_lines=line.strip()
        listli = strip_lines.split(",")
        m = list1.append(listli)
    #print(list1)
    list2=list(list1)
    #print(list2)
    res = np.full((720, 1280, 3),
                            0, dtype = np.uint8)
    for i in list2:
        a1 = list(i[0:2])
        a2 = list(i[2:4])
        a3 = list(i[4:6])
        a4 = list(i[6:8])
        #print(a1,a2,a3,a4)
        image = np.full((720, 1280, 3),
                                0, dtype = np.uint8)
        window_name = 'Image'
        pts = np.array([a1,a2,a3,a4],
                        np.int32)
        pts = pts.reshape((-1, 1, 2))
         
        isClosed = True
        color = (0, 0, 255)
        color1 = (255,0,0)
        thickness = 2
        image = cv2.polylines(image, [pts],
                              isClosed, color, thickness)
        image = cv2.fillPoly(image, [pts], color1)
        res += image
    cv2.imwrite("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bb/img_bb_"+str(img_num)+".jpg", res)
    img_num += 1

for file in glob.glob(path_1):    
    im = cv2.imread(file) 
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    th, im_gray_th_otsu = cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)
    cv2.imwrite("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bz/img_bz_"+str(img_num_bz)+".jpg", im_gray_th_otsu)
    img_num_bz += 1
    
path_2 = "C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bb/*.jpg"
img_num_bbz = 1 
for file in glob.glob(path_2):    
    im = cv2.imread(file) 
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    th, im_gray_th_otsu = cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)
    cv2.imwrite("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bbz/img_bbz_"+str(img_num_bbz)+".jpg", im_gray_th_otsu)
    img_num_bbz += 1 


path_3 = "C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bbz/*.jpg"
path_4 = "C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bz/*.jpg"
num = 1


for (i,j) in zip(glob.glob(path_3),glob.glob(path_4)):
    print(i,j)
    im1=cv2.imread(i)
    im2=cv2.imread(j)
    dest = cv2.bitwise_and(im1, im2, mask = None)
    cv2.imwrite("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/new_mask/img_mask_"+str(num)+".jpg", dest)
    num += 1
        




    
    
    

     

    
