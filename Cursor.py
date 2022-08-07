#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 12:52:50 2022

@author: heisenberg
"""


from tkinter import *
import cv2
from PIL import Image, ImageTk


root = Tk()
root.config(cursor="star")
root.geometry("1290x730")


clicks = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
       clicks.append((x,y))
       if len(clicks) > 3:
          print(str(clicks).strip('[]').strip('()').replace('), (', ','))
          clicks.clear()  
        
        
        
if __name__=="__main__":
    root.mainloop()
    img = cv2.imread("/home/heisenberg/Study/Database/New_Rsearch/Data/train_img_608.jpg")
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    
    
