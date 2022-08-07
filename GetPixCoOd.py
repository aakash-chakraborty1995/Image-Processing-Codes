#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 13:39:18 2022

@author: heisenberg
"""


#Import the tkinter library


import tkinter as tk
import cv2
from PIL import Image, ImageTk

clicks = []
def button_pressed(event):
    clicks.append((event.x, event.y))
    if len(clicks) > 3:
       print(str(clicks).strip('[]').strip('()').replace('), (', ','))
       clicks.clear()
    

root = tk.Tk()
cvimg = cv2.imread('/home/heisenberg/Study/Database/New_Rsearch/Data/train_img_759.jpg')
imgtk = Image.fromarray(cvimg)
img = ImageTk.PhotoImage(image=imgtk)
img.image = img
label = tk.Label(root)
label['image'] = img
label['cursor'] = 'crosshair'
label.pack()
label.bind('<Button-1>', lambda event: button_pressed(event))
root.mainloop()

