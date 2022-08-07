#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 23:36:09 2022

@author: heisenberg
"""

import cv2
import numpy as np

# load the image
image_path = "/home/heisenberg/Study/Database/EAST_Dataset/train_img_new/train_img_34.jpg"
image = cv2.imread(image_path)

# create a mask with white pixels
mask = np.ones(image.shape, dtype=np.uint8)
mask.fill(255)

# points to be cropped
roi_corners = np.array([[(561, 136), (604 , 139), (607 , 165), (559 , 162)]], dtype=np.int32)
# fill the ROI into the mask
cv2.fillPoly(mask, roi_corners, 0)

# The mask image
cv2.imwrite("/home/heisenberg/Study/Database/EAST_Dataset/image_masked.png", mask)

# applying th mask to original image
masked_image = cv2.bitwise_or(image, mask)

# The resultant image
cv2.imwrite("/home/heisenberg/Study/Database/EAST_Dataset/new_masked_image.jpg", masked_image)