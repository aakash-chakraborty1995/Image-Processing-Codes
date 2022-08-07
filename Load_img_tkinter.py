#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 21:40:22 2022

@author: heisenberg
"""


#Import the tkinter library
from tkinter import *
import numpy as np
import cv2
from PIL import Image, ImageTk

#Create an instance of tkinter frame
win = Tk()
win.geometry("700x550")
#Load the image
img = cv2.imread('/home/heisenberg/Study/Database/New_Rsearch/Data/train_img_636.jpg')

#Rearrange colors
blue,green,red = cv2.split(img)
img = cv2.merge((red,green,blue))
img = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im)

#Create a Label to display the image
Label(win, image= imgtk).pack()
win.mainloop()