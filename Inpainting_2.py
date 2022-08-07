#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 01:42:04 2022

@author: heisenberg
"""

import cv2

img = cv2.imread('/home/heisenberg/Akash_WD/Work/Satyajit/Devi/Vol-I/Completed/devi0070.jpg')
mask = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)[1][:,:,0]

#dst = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
#cv2.imshow("dst",dst)
#cv2.waitKey(0)
#cv2.destroyAllWindows()