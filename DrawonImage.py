# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
img=cv2.imread('/home/heisenberg/Study/Database/words/a01/a01-000u/a01-000u-00-00.png')
height=img.shape[0]
width=img.shape[1]
cv2.line(img,(0,0),(27,51),(255,0,0),3,lineType=cv2.LINE_8,shift=None)
cv2.imshow("Image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
