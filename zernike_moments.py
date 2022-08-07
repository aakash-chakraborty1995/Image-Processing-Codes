# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import mahotas
import numpy as np
import matplotlib.pyplot as plt

img_before = mahotas.imread("/home/heisenberg/Study/Database/EAST_Dataset/Cropped/cropped_text_4.jpg")
plt.imshow(img_before)

img_after=img_before.max(2)
plt.imshow(img_after)


radius = 1

value = mahotas.features.zernike_moments(img_after, radius)
value =list(value)

print(value)

count = 0
for i in value:
    count = count+i
    
avg = count/len(value)
  
print("sum = ", count)
print("average = ", avg)    
