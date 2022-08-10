# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 21:08:06 2022

@author: akash
"""

import cv2
import numpy as np


num = 1

for i in range(1,102):
    path_1 = f"C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/gt/gt_img_{num}.txt"
    my_file =  open(path_1)
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
    cv2.imwrite("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bb/img_bb_"+str(num)+".jpg", res)
    num += 1


num_ = 1

for i in range(1,102):
    path_2 = f"C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/test/img_{num_}.jpg"
    im = cv2.imread(path_2) 
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    th, im_gray_th_otsu = cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)
    cv2.imwrite("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bz/img_bz_"+str(num_)+".jpg", im_gray_th_otsu)
    num_ += 1
    
   
    

nu_m = 1 

for i in range(1, 102): 
    path_3 = f"C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bb/img_bb_{nu_m}.jpg"
    im = cv2.imread(path_3) 
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    th, im_gray_th_otsu = cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)
    cv2.imwrite("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bbz/img_bbz_"+str(nu_m)+".jpg", im_gray_th_otsu)
    nu_m += 1 

n_um = 1

for i in range(1, 102):
    path_4 = f"C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bbz/img_bbz_{n_um}.jpg"
    path_5 = f"C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/bz/img_bz_{n_um}.jpg"
    im1 = cv2.imread(path_4)
    im2 = cv2.imread(path_5)
    dest = cv2.bitwise_and(im1, im2, mask = None)
    cv2.imwrite("C:/Akash/Study/datasets/New_EAST_Dataset/result/mask/new_mask/mask_img_"+str(n_um)+".jpg", dest)
    n_um += 1








    
    
    

     

    
