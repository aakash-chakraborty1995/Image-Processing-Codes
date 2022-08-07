# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 17:26:20 2022

@author: akash
"""
from PIL import Image
  
image = Image.open("C:\Akash\Study\datasets\Satyajit Word Database\Aranyer0008\Aranyer0008_img_3.jpg")

width, height = image.size
 
right = int((1280-width)/2)
left = right
top = int((720-height)/2)
bottom = top
  
width, height = image.size
  
new_width = width + right + left
new_height = height + top + bottom
  
result = Image.new(image.mode, (new_width, new_height), (251, 232, 200))
  
result.paste(image, (right, top))
  
result.save('C:\Akash\Study\datasets\Satyajit Word Database\Aranyer0008\output_3.jpg')