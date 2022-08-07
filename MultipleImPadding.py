# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 15:20:37 2022

@author: akash
"""
import cv2
import glob
from PIL import Image
from numpy import asarray


path = "/home/heisenberg/img/src_imgs/bin_15/*.*"
img_number = 147

for file in glob.glob(path):
    print(file)
    
    img = Image.open(file)
   

    
    width, height = img.size
     
    right = int(((1280-width)/10)*3)
    left = int(((1280-width)/10)*7)
    top = int(((720-height)/10)*7)
    bottom = int(((720-height)/10)*3)
      
    width, height = img.size
      
    new_width = width + right + left
    new_height = height + top + bottom
      
    result = Image.new(img.mode, (new_width, new_height), (245, 224, 194))
      
    result.paste(img, (right, top))
    New_Result = asarray(result)
    Result_rgb = cv2.cvtColor(New_Result, cv2.COLOR_BGR2RGB)
    
    
    cv2.imwrite("/home/heisenberg/img/dst_imgs/bin_15_result/train_img_"+str(img_number)+".jpg", Result_rgb)
    img_number +=1
