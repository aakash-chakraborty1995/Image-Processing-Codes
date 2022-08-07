# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:58:37 2021

@author: AKASH
"""
    
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math as m
import copy
import xml.etree.ElementTree as ET
import tkinter as tk 
from tkinter import *
import tkinter.messagebox
from tkinter import tix
import random
import tkinter.filedialog
import os
from pyavrophonetic import avro
from pyhinavrophonetic import hinavro
from matplotlib.widgets import RectangleSelector
import time
import signal
import matplotlib
import ntpath
# Reading the image and binarization
#Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
global file_select_mode
file_select_mode=0


print(matplotlib.get_backend())

##### very very important to change matplotlib backend #######
plt.switch_backend('QT5Agg')
print(matplotlib.get_backend())
##############################################################


def RunFile_select(w):
    global file_select_mode

    top = tix.Frame(w, bd=1, relief=tix.RAISED)        
    box = tix.ButtonBox(w, orientation=tix.HORIZONTAL)
    box.add('new', text='New Page Annotation', underline=0, width=25,
            command=lambda w=w: new_file_select(w))
    box.add('old', text='Annotate Unfinished Document', underline=0, width=25,
            command=lambda w=w: old_file_select(w))
    box.pack(side=tix.BOTTOM, fill=tix.X)
    top.pack(side=tix.TOP, fill=tix.BOTH, expand=1)
            
def new_file_select(w):
    # tixDemo:Status "Month = %s" % demo_month.get()
    global file_select_mode
    file_select_mode=1    
    w.destroy()
            
def old_file_select(w):
    # tixDemo:Status "Month = %s" % demo_month.get()
    global file_select_mode
    file_select_mode=2    
    w.destroy()
        
if __name__ == '__main__':
    root = tix.Tk()
    RunFile_select(root)
    root.mainloop()




# Take the input image under consideration

path=tkinter.filedialog.askopenfilename(filetypes=[("Image File",'.jpg')])
path=os.path.normpath(path)
in_img = cv2.imread(path) #reading the image as original 'E://GuGaBaBa//GGBB-P019.bmp'
org_size=np.shape(in_img)
Vert=org_size[0]#900 # Fit in the screen
Horz=org_size[1]#int(float(org_size[1])/float(org_size[0])*Vert)
in_img2R=cv2.resize(in_img,(Horz,Vert))
gray_img=cv2.cvtColor(in_img2R,cv2.COLOR_BGR2GRAY) #converting image into gray scale
img_bin = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15,9)
bin_img = copy.deepcopy(img_bin)   # create for finding corrected and segmented image
cv2.imshow('Contour image', img_bin)
#----------------applying dilation operation on binary image
kernal = np.ones((1,1),np.uint8)#(np.squeeze(np.asarray([[0,1,0],[1,1,1],[0,1,0]]))).astype(int)#
bin_img=cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernal)
bin_img=cv2.dilate(bin_img,kernal,iterations =1)


LANG=['English','Bengali','Hindi']
#----------------applying contour operation on binary image
thresh, org_bin_img = cv2.threshold(bin_img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
contours, heirarchy= cv2.findContours(org_bin_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse = True)
org_bin_img=org_bin_img/255

m=len(contours)
for i in range(m-1,0,-1):
    M = cv2.contourArea(contours[i])
    if M<=12:
        contours.pop(i)
m=len(contours)   
global img_cd
img_cd=copy.deepcopy(in_img2R)

contours_all=copy.deepcopy(contours)
for c in range(len(contours)):
    rr=random.randint(1,255)
    gg=random.randint(1,255)
    bb=random.randint(1,255)
    cv2.drawContours(img_cd, contours, c, (rr,gg,bb),-1)    

cv2.imshow('contours_org',img_cd)
os.mkdir(path[0:(len(path)-4)]+"_Annotation\\")
cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\Contours.jpg",img_cd) 

# define all indispensable variables at their default value
ground_truth_img=np.zeros((Vert,Horz,3))
ground_truth_img=ground_truth_img.astype(np.uint8)
ground_truth_desc_img=np.zeros((Vert,Horz,3))
ground_truth_desc_img=ground_truth_img.astype(np.uint8)
ground_truth_line3_img=np.zeros((Vert,Horz,3))
ground_truth_line3_img=ground_truth_img.astype(np.uint8)
ground_truth_word4_img=np.zeros((Vert,Horz,3))
ground_truth_word4_img=ground_truth_img.astype(np.uint8)
label_box=np.zeros((5, 100))
desc_box=np.zeros((5, 200))
line3_box=np.zeros((5, 500))
word4_box=np.zeros((5, 1000))
label_list=[[]]*100
l_list = ['Noise','Text','Bold_Text','Striked_Text','Underlined_Text','Textbox','Hand_Sketch','Graphics','Headlines','Headers']
for i in range(0,len(l_list)):
    label_list[i]=l_list[i]
del l_list
desc_list=[[]]*200
desc_list[0] ='None'
desc_list[1]='Paragraph'
line3_list=[[]]*500
line3_list[0] = 'None'
line3_list[1]='Line'
word4_list=[[]]*1000
word4_list[0] = 'None'
word4_list[1]='Word'
word4_numberlist=[[]]*1000
contours_label = []
contours_desc=[]
contours_line3=[]
contours_word4=[]
for i in range(100):
    contours_label.append([])    
for i in range(200):
    contours_desc.append([])    
for i in range(500):
    contours_line3.append([])    
for i in range(1000):
    contours_word4.append([])

label_children=[]
for k in range(0,100):
    label_children.append([])  
desc_children=[]
for k in range(0,200):
    desc_children.append([]) 
line3_children=[]
for k in range(0,500):
    line3_children.append([])    
        
maxlayer=0
if file_select_mode==2:
    path_xml=tkinter.filedialog.askopenfilename(filetypes=[("Upload XML for Annotation",'.xml')])
    path_xml=os.path.normpath(path_xml)
    parser1 = ET.XMLParser(encoding='utf-8')
    tree = ET.parse(path_xml,parser=parser1)
    root = tree.getroot()
    indexxx=0
    for Annotations in root:
        print ("Annotations.tag")
        print ("----------")    
        for labels_elem in Annotations:
            print (labels_elem.tag)
            b_box=labels_elem.get('boundingbox')
            bb_box = b_box.split(',')
            indexx=labels_elem.get('index')
            indexxx=int(indexx)
            if indexxx>0 and maxlayer==0:
                maxlayer=1
            #print b_box
            label_box[0][indexxx]=float(bb_box[0])
            label_box[1][indexxx]=float(bb_box[1])
            label_box[2][indexxx]=float(bb_box[2])
            label_box[3][indexxx]=float(bb_box[3])
            label_list[indexxx]=(labels_elem.tag)
            del b_box, bb_box, indexx, indexxx
            for desc_elem in labels_elem:
                b_box=desc_elem.get('boundingbox')
                bb_box = b_box.split(',')
                indexx=desc_elem.get('index')
                indexxx=int(indexx)
                if indexxx>0 and maxlayer<2:
                    maxlayer=2
                desc_box[0][indexxx]=float(bb_box[0])
                desc_box[1][indexxx]=float(bb_box[1])
                desc_box[2][indexxx]=float(bb_box[2])
                desc_box[3][indexxx]=float(bb_box[3])
                desc_list[indexxx]=desc_elem.tag
                label_children[label_list.index(labels_elem.tag)].append(desc_elem.tag)                
                del b_box, bb_box, indexx, indexxx
                #print desc_elem.tag
                for line3_elem in desc_elem:
                    b_box=line3_elem.get('boundingbox')
                    bb_box = b_box.split(',')
                    indexx=line3_elem.get('index')
                    indexxx=int(indexx)
                    if indexxx>0 and maxlayer<3:
                        maxlayer=3
                    line3_box[0][indexxx]=float(bb_box[0])
                    line3_box[1][indexxx]=float(bb_box[1])
                    line3_box[2][indexxx]=float(bb_box[2])
                    line3_box[3][indexxx]=float(bb_box[3])
                    line3_list[indexxx]=line3_elem.tag
                    desc_children[desc_list.index(desc_elem.tag)].append(line3_elem.tag)
                    del b_box, bb_box, indexx, indexxx
                    #print line3_elem.tag
                    for word4_elem in line3_elem:
                        b_box=word4_elem.get('boundingbox')
                        bb_box = b_box.split(',')
                        indexx=word4_elem.get('index')
                        indexxx=int(indexx)
                        if indexxx>0 and maxlayer<4:
                            maxlayer=4
                        word4_box[0][indexxx]=float(bb_box[0])
                        word4_box[1][indexxx]=float(bb_box[1])
                        word4_box[2][indexxx]=float(bb_box[2])
                        word4_box[3][indexxx]=float(bb_box[3])
                        word4_list[indexxx]=word4_elem.get('spelling')
                        word4_numberlist[indexxx]=word4_elem.tag
                        line3_children[line3_list.index(line3_elem.tag)].append(word4_elem.tag)
                        del b_box, bb_box, indexx, indexxx
                        
#                        print word4_elem.tag , word4_elem.attrib

    
    load_gt=0
    while load_gt<maxlayer:
        print('Please Upload  '+ str(load_gt+1)+ '-Layer GT-image')
        path_xml=tkinter.filedialog.askopenfilename(filetypes=[("Upload_Layer-GT-image",'.jpg')])
        path_xml=os.path.normpath(path_xml)
        path_file=ntpath.basename(path_xml)
        try:    
            if load_gt==0 and path_file=='GT-Layer1.jpg':
                ground_truth_img = cv2.imread(path_xml)
                load_gt=1 
                gray_img=cv2.cvtColor(ground_truth_img,cv2.COLOR_BGR2GRAY)
                thresh, img_x = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY)
                img_x=img_x/255
                img_done=np.multiply(org_bin_img.astype(float),img_x)
                img_todo=np.subtract(org_bin_img,img_done)
                img_done=img_done.astype(np.uint8)
                img_todo=img_todo.astype(np.uint8)
                contours, hierarchy = cv2.findContours(img_todo,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse = True)
                m=len(contours)
                for i in range(m-1,0,-1):
                    M = cv2.contourArea(contours[i])
                    if M<=12:
                        contours.pop(i)
                if cv2.contourArea(contours[0])>0.5*Vert*Horz:
                    contours.pop(0)
                contours_label_todo=contours
                
                contours, hierarchy = cv2.findContours(img_done,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse = True)
                if cv2.contourArea(contours[0])>0.5*Vert*Horz:
                    contours.pop(0)
                m=len(contours)
                for i in range(m-1,0,-1):
                    M = cv2.contourArea(contours[i])
                    if M<=12:
                        contours.pop(i)
                img_x=gray_img
                img_x=np.pad(img_x, 1, mode='constant')
                for c in contours:
                    indx=c[1][0][1]+1
                    indy=c[1][0][0]+1
                    indexx=0
                    try:
                        for i in range(indx-1,indx+2):
                            for j in range(indy-1,indy+2):
                                indexx=max(img_x[i,j],indexx)
                    except:
                        indexx=0
                    if indexx!=0:
                        contours_label[indexx].append(c)                        
                print ('1st Layer GT image Loaded')#reading the image as original 'E://GuGaBaBa//GGBB-P019.bmp'
                del img_x,img_done,img_todo,contours,indexx,indx,indy,gray_img,thresh,hierarchy
                
            elif load_gt==1 and path_file=='GT-Layer2.jpg':
                ground_truth_desc_img = cv2.imread(path_xml)
                load_gt=2 
                gray_img=cv2.cvtColor(ground_truth_desc_img,cv2.COLOR_BGR2GRAY)
                thresh, img_x = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY)
                img_x=img_x/255
                img_done=np.multiply(org_bin_img.astype(float),img_x)
                img_todo=np.subtract(org_bin_img,img_done)
                img_done=img_done.astype(np.uint8)
                img_todo=img_todo.astype(np.uint8)
                contours, hierarchy = cv2.findContours(img_todo,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse = True)
                m=len(contours)
                for i in range(m-1,0,-1):
                    M = cv2.contourArea(contours[i])
                    if M<=12:
                        contours.pop(i)
                if cv2.contourArea(contours[0])>0.5*Vert*Horz:
                    contours.pop(0)
                contours_desc_todo=contours
                
                im2, contours, hierarchy = cv2.findContours(img_done,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse = True)
                if cv2.contourArea(contours[0])>0.5*Vert*Horz:
                    contours.pop(0)
                m=len(contours)
                for i in range(m-1,0,-1):
                    M = cv2.contourArea(contours[i])
                    if M<=12:
                        contours.pop(i)
                img_x=gray_img
                img_x=np.pad(img_x, 1, mode='constant')
                for c in contours:
                    indx=c[1][0][1]+1
                    indy=c[1][0][0]+1
                    indexx=0
                    try:
                        for i in range(indx-1,indx+2):
                            for j in range(indy-1,indy+2):
                                indexx=max(img_x[i,j],indexx)
                    except:
                        indexx=0
                    if indexx!=0:
                        contours_desc[indexx].append(c)                        
                print ('2nd Layer GT image Loaded')#reading the image as original 'E://GuGaBaBa//GGBB-P019.bmp'
                del img_x,img_done,img_todo,contours,indexx,indx,indy,gray_img,thresh,hierarchy
    
            elif load_gt==2 and path_file=='GT-Layer3.jpg':
                ground_truth_line3_img = cv2.imread(path_xml)
                load_gt=3 
                gray_img=cv2.cvtColor(ground_truth_line3_img,cv2.COLOR_BGR2GRAY)
                thresh, img_x = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY)
                img_x=img_x/255
                img_done=np.multiply(org_bin_img.astype(float),img_x)
                img_todo=np.subtract(img_x,img_done)
                img_done=img_done.astype(np.uint8)
                img_todo=img_todo.astype(np.uint8)
                contours, hierarchy = cv2.findContours(img_todo,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse = True)
                m=len(contours)
                for i in range(m-1,0,-1):
                    M = cv2.contourArea(contours[i])
                    if M<=12:
                        contours.pop(i)
                if cv2.contourArea(contours[0])>0.5*Vert*Horz:
                    contours.pop(0)
                contours_line3_todo=contours
                
                contours, hierarchy = cv2.findContours(img_done,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse = True)
                if cv2.contourArea(contours[0])>0.5*Vert*Horz:
                    contours.pop(0)
                m=len(contours)
                for i in range(m-1,0,-1):
                    M = cv2.contourArea(contours[i])
                    if M<=12:
                        contours.pop(i)
                img_x=gray_img
                img_x=np.pad(img_x, 1, mode='constant')
                for c in contours:
                    indx=c[1][0][1]+1
                    indy=c[1][0][0]+1
                    indexx=0
                    try:
                        for i in range(indx-1,indx+2):
                            for j in range(indy-1,indy+2):
                                indexx=max(img_x[i,j],indexx)
                    except:
                        indexx=0
                    if indexx!=0:
                        contours_line3[indexx].append(c)                        
                print ('3rd Layer GT image Loaded')#reading the image as original 'E://GuGaBaBa//GGBB-P019.bmp'
                del img_x,img_done,img_todo,contours,indexx,indx,indy,gray_img,thresh,hierarchy

            elif load_gt==3 and path_file=='GT-Layer4.jpg':
                ground_truth_word4_img = cv2.imread(path_xml)
                load_gt=4 
                gray_img=cv2.cvtColor(ground_truth_word4_img,cv2.COLOR_BGR2GRAY)
                thresh, img_x = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY)
                img_x=img_x/255
                img_done=np.multiply(org_bin_img.astype(float),img_x)
                img_todo=np.subtract(img_x,img_done)
                img_done=img_done.astype(np.uint8)
                img_todo=img_todo.astype(np.uint8)
                contours, hierarchy = cv2.findContours(img_todo,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse = True)
                m=len(contours)
                for i in range(m-1,0,-1):
                    M = cv2.contourArea(contours[i])
                    if M<=12:
                        contours.pop(i)
                if cv2.contourArea(contours[0])>0.5*Vert*Horz:
                    contours.pop(0)
                contours_word4_todo=contours
                
                contours, hierarchy = cv2.findContours(img_done,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse = True)
                if cv2.contourArea(contours[0])>0.5*Vert*Horz:
                    contours.pop(0)
                m=len(contours)
                for i in range(m-1,0,-1):
                    M = cv2.contourArea(contours[i])
                    if M<=12:
                        contours.pop(i)
                img_x=gray_img
                img_x=np.pad(img_x, 1, mode='constant')
                for c in contours:
                    indx=c[1][0][1]+1
                    indy=c[1][0][0]+1
                    indexx=0
                    try:
                        for i in range(indx-1,indx+2):
                            for j in range(indy-1,indy+2):
                                indexx=max(img_x[i,j],indexx)
                    except:
                        indexx=0
                    if indexx!=0:
                        contours_word4[indexx].append(c)                        
                print ('4th Layer GT image Loaded')#reading the image as original 'E://GuGaBaBa//GGBB-P019.bmp'
                del img_x,img_done,img_todo,contours,indexx,indx,indy,gray_img,thresh,hierarchy  
                
            else:
                print ('Error-1')
                
        except:
            print ('Error-2')
            

        

        
del img_bin, c,bin_img,in_img
del org_size
del kernal
del img_cd
#=======================Defining Small functions=======================================================
global r,kk
r=[0,0,0,0]
kk=0
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)
interrupted = False

def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    r[0]=x1
    r[1]=y1
    r[2]=x2-x1
    r[3]=y2-y1
    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    print(" The button you used were: %s %s" % (eclick.button, erelease.button))


def toggle_selector(event):
    print(' Key pressed.')
    global kk
    kk=0
    print (event.key)
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)
    if event.key=='enter':
        print ('LOL') 
        kk=1
    if event.key=='ctrl+c':
        global interupted
        interupted=1
    if event.key== 'C':
        "global interupted"
        interupted=1

def main1(img_cd1):
    org_size=np.shape(img_cd1)
    Vert1=org_size[0]#900 # Fit in the screen
    Horz1=org_size[1]#int(float(org_size[1])/float(org_size[0])*Vert)
    plt.close()   
    fig, current_ax = plt.subplots(1,2)                                                  # If N is large one can see 
    current_ax[0].imshow(cv2.cvtColor(in_img2R, cv2.COLOR_BGR2RGB))                                                 # If N is large one can see
    current_ax[1].imshow(cv2.cvtColor(img_cd1, cv2.COLOR_BGR2RGB))
        #r=[0,0,0,0]
    print("\n      click  -->  release")

        # drawtype is 'box' or 'line' or 'none'
    toggle_selector.RS = RectangleSelector(current_ax[1], line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
    plt.connect('key_press_event', toggle_selector)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.axis("off")
    plt.xlim(-20,Horz1+20)
    plt.ylim(Vert1+20,-20)
    plt.draw()
    plt.tight_layout()    
    time.sleep(0.5)
    try:
        while True:
            #print 'your input'
            print ('Buttonpress wanted')
            if plt.waitforbuttonpress():
                if kk==1:
                    break                
    
    except KeyboardInterrupt:
        global interupted
        interupted=1
        pass                
    
    

def main2(img_cd1,label_box,k):
    plt.close()
    global interupted
    interupted=0
    fig, current_ax = plt.subplots(1,2)                                                  # If N is large one can see 
    current_ax[0].imshow(cv2.cvtColor(in_img2R, cv2.COLOR_BGR2RGB))                                                 # If N is large one can see
    current_ax[1].imshow(cv2.cvtColor(img_cd1, cv2.COLOR_BGR2RGB),origin='upper')
        #r=[0,0,0,0]
    print("\n      click  -->  release")

        # drawtype is 'box' or 'line' or 'none'
    toggle_selector.RS = RectangleSelector(current_ax[1], line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
    plt.connect('key_press_event', toggle_selector)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.xlim(label_box[0][k]-20,label_box[2][k]+20)
    plt.ylim(label_box[3][k]+20,label_box[1][k]-20)
    plt.show()
    plt.tight_layout()    
    time.sleep(0.5)
    try:
        while True:
            #print 'your input'
            print ('Buttonpress wanted')
            if plt.waitforbuttonpress():
                if kk==1:
                    break                
    
    except KeyboardInterrupt:
        interupted=1
        pass
    


#=======================================applying contour sorting=================================================
if file_select_mode==2:
   contour_disp=copy.deepcopy(contours_label_todo)
elif file_select_mode==1:
   contour_disp=copy.deepcopy(contours_all)
#-----------------------------above codes are for Dialog Box Only------------------
#----------------------------------------------------------------------------------
cv2.destroyAllWindows()


global ok_label
ok_label=0
global save1_label
save1_label=0
global interupted
interupted=0
count=1
img_cd1=copy.deepcopy(in_img2R)
font = cv2.FONT_HERSHEY_SIMPLEX
for i in range(len(label_list)-1,0,-1):
    if label_list[i]==[]:
        label_list.pop(i)
    else:
        break
        

while (len(contour_disp) > 5 and interupted==0) :
    print ("Please Select ROI, All Labels are not Marked\n")
    #tkMessageBox.showinfo("Title", "Please Select ROI, All Labels are not Marked")
    fromCenter = False
    img_cd1=copy.deepcopy(in_img2R)
    #cv2.drawContours(img_cd1, contour_disp, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
    for c in range(len(contour_disp)):
        rr=random.randint(1,255)
        gg=random.randint(1,255)
        bb=random.randint(1,255)
        cv2.drawContours(img_cd1, contour_disp, c, (rr,gg,bb),-1)
    cv2.putText(img_cd1,"Layer-1 Annonation",(5, 12), font, 0.4, (100,55,55), 2, cv2.LINE_AA)
    #r = cv2.selectROI(img_cd1, fromCenter)

    
    r=[0,0,0,0]
    kk=0
    if __name__ == '__main__':        
        main1(img_cd1)
    #--------------------Select Label---------------------------------------------------
    print ('Enters Selected region')
    print ('r')
    def RunSample(w):
        global demo_label
        global ok_label
        global save1_label
        save1_label=0
        ok_label=0   
        top = tix.Frame(w, bd=1, relief=tix.RAISED)        
        demo_label = tix.StringVar()

        a = tix.ComboBox(top, label="Labels: ", dropdown=1,
                         command=select_month, editable=1, variable=demo_label,
                         options='listbox.height 14 label.width 12 label.anchor e')
        a.pack(side=tix.TOP, anchor=tix.W)        
        for i in label_list:
            a.insert(tix.END, i)

        a.set_silent('Please Select Label')
        
        box = tix.ButtonBox(w, orientation=tix.HORIZONTAL)
        box.add('ok', text='Ok', underline=0, width=6,
                    command=lambda w=w: ok_command(w))
        box.add('cancel', text='Cancel', underline=0, width=6,
                    command=lambda w=w: w.destroy())
        box.add('save&continue', text='Save & Continue', underline=0, width=15,
                    command=lambda w=w: sok_command(w))
        box.pack(side=tix.BOTTOM, fill=tix.X)
        top.pack(side=tix.TOP, fill=tix.BOTH, expand=1)
            
    def select_month(event=None):
        # tixDemo:Status "Month = %s" % demo_month.get()
        pass
            
    def select_year(event=None):
        # tixDemo:Status "Year = %s" % demo_year.get()
        pass
    
    def sok_command(w):
        global save1_label
        save1_label=1    
        global ok_label
        ok_label=1;
        w.destroy()
    
    def ok_command(w):
        # tixDemo:Status "Month = %s, Year= %s" % (demo_month.get(), demo_year.get())
        global ok_label
        ok_label=1;
        w.destroy()
        
    if __name__ == '__main__':
        root = tix.Tk()
        RunSample(root)
        root.mainloop()
    
    #print ("Select label LOOP crossed")
    
        
    if ok_label==1:
        lab_st=demo_label.get()    
        if lab_st not in label_list:
            label_list.append(lab_st)
        
        label=label_list.index(lab_st)
        print (label)
        print (lab_st)
#-------------------------------------------------------------------------------------------
    
        mm=len(contour_disp)
        deletelist=[]
        for i in range(mm):
            (x,y,w,h) = cv2.boundingRect(contour_disp[i])
            if (x>=r[0] and y>=r[1] and x+w<=r[0]+r[2] and y+h<=r[1]+r[3] ):            
                deletelist.insert(len(deletelist),i)
                if (lab_st!='None' and lab_st!='Please Select Label'):
                    contours_label[label].append(contour_disp[i])
            
            
        for i in reversed(range(len(deletelist))):
            contour_disp.pop(deletelist[i])
            
    if save1_label==1:
        cv2.destroyAllWindows()
        count=1
        final_img=copy.deepcopy(in_img2R)
        ground_truth_img=np.zeros((Vert,Horz))
        font = cv2.FONT_HERSHEY_SIMPLEX
        label_box=np.zeros((4, len(label_list)))

        for i in range(0,len(label_list)):
            cont_cluster=copy.deepcopy(contours_label[i])
            height, width, _ = in_img2R.shape
            min_x, min_y = width, height
            max_x = max_y = 0
    
            for c in cont_cluster:
                (x,y,w,h) = cv2.boundingRect(c)
                min_x, max_x = min(x, min_x), max(x+w, max_x)
                min_y, max_y = min(y, min_y), max(y+h, max_y) 
        
            if max_x - min_x > 0 and max_y - min_y > 0:
                cv2.rectangle(final_img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
                cv2.putText(final_img,label_list[i],(min_x+5, min_y-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
                label_box[0][i]=min_x
                label_box[1][i]=min_y
                label_box[2][i]=max_x
                label_box[3][i]=max_y
    
            print(len(cont_cluster))
            cv2.drawContours(final_img, cont_cluster, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
            cv2.drawContours(ground_truth_img, cont_cluster, -1, i,-1)   
     

        cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\Display-Layer1.jpg",final_img) 
        cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\GT-Layer1.jpg",ground_truth_img)
        root = ET.Element("Page")
        doc = ET.SubElement(root, "Annotations")

        count=0
        for i in range(len(label_list)):
            if (len(contours_label[i])>0):
                ET.SubElement(doc,label_list[i] , pattern="Layer-1", boundingbox= str(label_box[0][i])+','+str(label_box[1][i])+','+str(label_box[2][i])+','+str(label_box[3][i]), index=str(i))    
 
        tree = ET.ElementTree(root)
        tree.write(path[0:(len(path)-4)]+"_Annotation\\Annotations.xml",encoding='utf8')

            

##==============Final Image and XML writing for Layer-1 
cv2.destroyAllWindows()
count=1
final_img=copy.deepcopy(in_img2R)
ground_truth_img=np.zeros((Vert,Horz))
font = cv2.FONT_HERSHEY_SIMPLEX
label_box=np.zeros((4, len(label_list)))

for i in range(0,len(label_list)):
    cont_cluster=copy.deepcopy(contours_label[i])
    height, width, _ = in_img2R.shape
    min_x, min_y = width, height
    max_x = max_y = 0
    
    for c in cont_cluster:
        (x,y,w,h) = cv2.boundingRect(c)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y) 
        
    if max_x - min_x > 0 and max_y - min_y > 0:
        cv2.rectangle(final_img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
        cv2.putText(final_img,label_list[i],(min_x+5, min_y-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
        label_box[0][i]=min_x
        label_box[1][i]=min_y
        label_box[2][i]=max_x
        label_box[3][i]=max_y
    
    print(len(cont_cluster))
    cv2.drawContours(final_img, cont_cluster, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
    cv2.drawContours(ground_truth_img, cont_cluster, -1, i,-1)   
     

cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\Display-Layer1.jpg",final_img) 
cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\GT-Layer1.jpg",ground_truth_img)
del final_img
del ground_truth_img
#del contours

root = ET.Element("Page")
doc = ET.SubElement(root, "Annotations")

count=0
for i in range(len(label_list)):
    if (len(contours_label[i])>0):
        ET.SubElement(doc,label_list[i] , pattern="Layer-1", boundingbox= str(label_box[0][i])+','+str(label_box[1][i])+','+str(label_box[2][i])+','+str(label_box[3][i]), index=str(i))    
 
tree = ET.ElementTree(root)
tree.write(path[0:(len(path)-4)]+"_Annotation\\Annotations.xml",encoding='utf8')
#--------------------------------------------------------------------------------------------------------------------------------
#---------------------Layer 2:Description Image----------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

interupted=0
ok_label=0;
"global ok_label"
ok_label=0
"global save1_label"
save1_label=0
"global interupted"
interupted=0
count=1
img_cd1=copy.deepcopy(in_img2R)
font = cv2.FONT_HERSHEY_SIMPLEX
for i in range(len(desc_list)-1,0,-1):
    if desc_list[i]==[]:
        desc_list.pop(i)
    else:
        break




for k in range(len(label_list)):

    contour_disp=[]
    cv2.destroyAllWindows()         
    count=1
    contour_all=copy.deepcopy(contours_label[k])
    gray_img=cv2.cvtColor(ground_truth_desc_img,cv2.COLOR_BGR2GRAY)
    thresh, img_x = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY)
    img_x=img_x/255
    img_done=np.zeros((Vert,Horz))
    for c in range(len(contour_all)):
        cv2.drawContours(img_done, contour_all, c, 1,-1)
    img_todo=np.subtract(img_done,np.multiply(img_x,img_done))
    img_todo=img_todo.astype(np.uint8)
    contour_disp, hierarchy = cv2.findContours(img_todo,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contour_disp = sorted(contour_disp, key=cv2.contourArea, reverse = True)
    
    while (len(contour_disp) > 3 and interupted==0):
        print ("Please Select ROI, All Labels are not Marked\n")
        #tkMessageBox.showinfo("Title", "Please Select ROI, All Labels are not Marked")
        "global ok_label"
        ok_label=0
        fromCenter = False
        img_cd1=copy.deepcopy(in_img2R)
        cv2.rectangle(img_cd1, (int(label_box[0][k]), int(label_box[1][k]) ), (int(label_box[2][k]) , int(label_box[3][k])), (255, 0, 0), 2)
        cv2.putText(img_cd1,label_list[k],(int(label_box[0][k])+5, int(label_box[1][k])+5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
        #cv2.drawContours(img_cd1, contour_disp, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
        for c in range(len(contour_disp)):
            rr=random.randint(1,255)
            gg=random.randint(1,255)
            bb=random.randint(1,255)
            cv2.drawContours(img_cd1, contour_disp, c, (rr,gg,bb),-1)
        
        cv2.putText(img_cd1,"Layer-2 Annonation",(5, 12), font, 0.4, (100,55,55), 2, cv2.LINE_AA)
        #r = cv2.selectROI(img_cd1, fromCenter)
        r=[0,0,0,0]
        kk=0
        if __name__ == '__main__':        
            main2(img_cd1,label_box,k)
        
        
        #--------------------Select Label---------------------------------------------------
        def RunSample(w):
            global demo_desc
            global ok_label
            global save1_label
            save1_label=0
            ok_label=0   
            top = tix.Frame(w, bd=1, relief=tix.RAISED)        
            demo_desc = tix.StringVar()

            a = tix.ComboBox(top, label="Labels: ", dropdown=1,
                         command=select_month, editable=1, variable=demo_desc,
                         options='listbox.height 14 label.width 12 label.anchor e')
            a.pack(side=tix.TOP, anchor=tix.W)        
            for i in desc_list:
                a.insert(tix.END, i)

            a.set_silent('Please Select Label')
        
            box = tix.ButtonBox(w, orientation=tix.HORIZONTAL)
            box.add('ok', text='Ok', underline=0, width=6,
                    command=lambda w=w: ok_command(w))
            box.add('cancel', text='Cancel', underline=0, width=6,
                    command=lambda w=w: w.destroy())
            box.add('save&continue', text='Save & Continue', underline=0, width=15,
                    command=lambda w=w: sok_command(w))
            box.pack(side=tix.BOTTOM, fill=tix.X)
            top.pack(side=tix.TOP, fill=tix.BOTH, expand=1)
            
        def select_month(event=None):
        # tixDemo:Status "Month = %s" % demo_month.get()
            pass
            
        def select_year(event=None):
        # tixDemo:Status "Year = %s" % demo_year.get()
            pass
    
        def sok_command(w):
            global save1_label
            save1_label=1    
            global ok_label
            ok_label=1;
            w.destroy()
    
        def ok_command(w):
        # tixDemo:Status "Month = %s, Year= %s" % (demo_month.get(), demo_year.get())
            global ok_label
            ok_label=1;
            w.destroy()
        
        if __name__ == '__main__':
            root = tix.Tk()
            RunSample(root)
            root.mainloop()

    
        if ok_label==1:
            desc_st=demo_desc.get()
        
            if desc_st not in desc_list:
                desc_list.append(desc_st)
                label_children[k].append(desc_st)
               
        
            desc=desc_list.index(desc_st)
            desc_box[4][desc]=k+1
            print (desc)    
        #-------------------------------------------------------------------------------------------
            mm=len(contour_disp)
            deletelist=[]
            for i in range(mm):
                (x,y,w,h) = cv2.boundingRect(contour_disp[i])
                if (x>=r[0] and y>=r[1] and x+w<=r[0]+r[2] and y+h<=r[1]+r[3] ):
                    deletelist.insert(len(deletelist),i)
                    if (desc_st!='None' and desc_st!='Please Select Label'):
                        contours_desc[desc].append(contour_disp[i])
                        
            
            
            for i in reversed(range(len(deletelist))):
                contour_disp.pop(deletelist[i])
            
            
        if save1_label==1:
            cv2.destroyAllWindows()
            count=1
            final_desc_img=copy.deepcopy(in_img2R)
            ground_truth_desc_img=np.zeros((Vert,Horz))
            font = cv2.FONT_HERSHEY_SIMPLEX
            desc_box=np.zeros((4, len(desc_list)))

            for i in range(0,len(desc_list)):
                cont_cluster=copy.deepcopy(contours_desc[i])
                height, width, _ = in_img2R.shape
                min_x, min_y = width, height
                max_x = max_y = 0
    
                for c in cont_cluster:
                    (x,y,w,h) = cv2.boundingRect(c)
                    min_x, max_x = min(x, min_x), max(x+w, max_x)
                    min_y, max_y = min(y, min_y), max(y+h, max_y) 
        
                if max_x - min_x > 0 and max_y - min_y > 0:
                    cv2.rectangle(final_desc_img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
                    cv2.putText(final_desc_img, desc_list[i],(min_x+5, min_y-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
                    desc_box[0][i]=min_x
                    desc_box[1][i]=min_y
                    desc_box[2][i]=max_x
                    desc_box[3][i]=max_y
    
                print(len(cont_cluster))
                cv2.drawContours(final_desc_img, cont_cluster, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
                cv2.drawContours(ground_truth_desc_img, cont_cluster, -1, i,-1)   
     

            cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\Display-Layer2.jpg",final_desc_img) 
            cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\GT-Layer2.jpg",ground_truth_desc_img)
            
                    
            root = ET.Element("Page")
            doc = ET.SubElement(root, "Annotations")
            
            count=0
            for i in range(len(label_list)):
                if (len(contours_label[i])>0):
                    ET.SubElement(doc,label_list[i] , pattern="Layer-1", boundingbox= str(label_box[0][i])+','+str(label_box[1][i])+','+str(label_box[2][i])+','+str(label_box[3][i]), index=str(i))    
            
            Siblings_1=[]
            sibling_1=[]
            Siblings_1=[elem.tag for elem in doc.iter() if elem is not doc and len(label_children[label_list.index(elem.tag)])>0]
            
            for sibling_1 in Siblings_1:
                elem=doc.find(sibling_1)
                Siblings_2=[]
                Siblings_2 = label_children[label_list.index(sibling_1)]
                for sibling_2 in Siblings_2:
                    i=desc_list.index(sibling_2)
                    ET.SubElement(elem, sibling_2, pattern="Layer-2", boundingbox= str(desc_box[0][i])+','+str(desc_box[1][i])+','+str(desc_box[2][i])+','+str(desc_box[3][i]), index=str(desc_list.index(sibling_2)))
            


 
cv2.destroyAllWindows()
count=1
final_desc_img=copy.deepcopy(in_img2R)
ground_truth_desc_img=np.zeros((Vert,Horz))
font = cv2.FONT_HERSHEY_SIMPLEX


for i in range(0,len(desc_list)):
    cont_cluster=copy.deepcopy(contours_desc[i])
    height, width, _ = in_img2R.shape
    min_x, min_y = width, height
    max_x = max_y = 0

    for c in cont_cluster:
        (x,y,w,h) = cv2.boundingRect(c)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y) 
            
    if max_x - min_x > 0 and max_y - min_y > 0:
        cv2.rectangle(final_desc_img, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
        cv2.putText(final_desc_img,desc_list[i],(min_x+5, min_y-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
        desc_box[0][i]=min_x
        desc_box[1][i]=min_y
        desc_box[2][i]=max_x
        desc_box[3][i]=max_y        
        #label_children[k].append(desc_list[i])
    

    print(len(cont_cluster))
    cv2.drawContours(final_desc_img, cont_cluster, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
    cv2.drawContours(ground_truth_desc_img, cont_cluster, -1, i,-1)
        
        

     
cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\Display-Layer2.jpg",final_desc_img) 
cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\GT-Layer2.jpg",ground_truth_desc_img)

root = ET.Element("Page")
doc = ET.SubElement(root, "Annotations")
            
count=0
for i in range(len(label_list)):
    if (len(contours_label[i])>0):
        ET.SubElement(doc,label_list[i] , pattern="Layer-1", boundingbox= str(label_box[0][i])+','+str(label_box[1][i])+','+str(label_box[2][i])+','+str(label_box[3][i]), index=str(i))    
            
Siblings_1=[]
sibling_1=[]
Siblings_1=[elem.tag for elem in doc.iter() if elem is not doc and len(label_children[label_list.index(elem.tag)])>0]
            
for sibling_1 in Siblings_1:
    elem=doc.find(sibling_1)
    Siblings_2=[]
    Siblings_2 = label_children[label_list.index(sibling_1)]
    for sibling_2 in Siblings_2:
        i=desc_list.index(sibling_2)
        ET.SubElement(elem, sibling_2, pattern="Layer-2", boundingbox= str(desc_box[0][i])+','+str(desc_box[1][i])+','+str(desc_box[2][i])+','+str(desc_box[3][i]), index=str(desc_list.index(sibling_2)))


tree = ET.ElementTree(root)
tree.write(path[0:(len(path)-4)]+"_Annotation\\Annotations.xml",encoding='utf8')
del cont_cluster
del final_desc_img
#del contours_label



#--------------------------------------------------------------------------------------------------------------------------------
#---------------------Layer 3:Line3 Image----------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

interupted=0
ok_label=0;
"global ok_label"
ok_label=0
"global save1_label"
save1_label=0
"global interupted"
interupted=0
count=1
img_cd1=copy.deepcopy(in_img2R)
font = cv2.FONT_HERSHEY_SIMPLEX
for i in range(len(line3_list)-1,0,-1):
    if line3_list[i]==[]:
        line3_list.pop(i)
    else:
        break



#for l in range(len(label_list)):
for k in range(len(desc_list)):


    contour_disp=[]
    cv2.destroyAllWindows()         
    count=1
    contour_all=copy.deepcopy(contours_desc[k])
    gray_img=cv2.cvtColor(ground_truth_line3_img,cv2.COLOR_BGR2GRAY)
    thresh, img_x = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY)
    img_x=img_x/255
    img_done=np.zeros((Vert,Horz))
    img_done=img_done.astype(np.uint8)
    for c in range(len(contour_all)):
        cv2.drawContours(img_done, contour_all, c, 1,-1)
    img_todo=np.subtract(img_done,np.multiply(img_x,img_done))
    img_todo=img_todo.astype(np.uint8)
    contour_disp, hierarchy = cv2.findContours(img_todo,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contour_disp = sorted(contour_disp, key=cv2.contourArea, reverse = True)

    
    while (len(contour_disp) > 1 and interupted==0):
        print ("Please Select ROI, All Labels are not Marked\n")
        #tkMessageBox.showinfo("Title", "Please Select ROI, All Labels are not Marked")
        fromCenter = False
        img_cd1=np.zeros((Vert,Horz))
        img_cd1=copy.deepcopy(in_img2R)
        cv2.rectangle(img_cd1, (int(desc_box[0][k]), int(desc_box[1][k]) ), (int(desc_box[2][k]) , int(desc_box[3][k])), (255, 0, 0), 2)
        cv2.putText(img_cd1,desc_list[k],(int(desc_box[0][k])+5, int(desc_box[1][k])-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
        #cv2.drawContours(img_cd1, contour_disp, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
        for c in range(len(contour_disp)):
            rr=random.randint(1,255)
            gg=random.randint(1,255)
            bb=random.randint(1,255)
            cv2.drawContours(img_cd1, contour_disp, c, (rr,gg,bb),-1)
            
        cv2.putText(img_cd1,"Layer-3 Annonation",(5, 12), font, 0.4, (100,55,55), 2, cv2.LINE_AA)
        #r = cv2.selectROI(img_cd1, fromCenter)
        r=[0,0,0,0]
        kk=0
        if __name__ == '__main__':        
            main2(img_cd1,desc_box,k)

        
        #--------------------Select Label---------------------------------------------------
        def RunSample(w):
            global demo_line3
            global ok_label
            global save1_label
            save1_label=0
            ok_label=0   
            top = tix.Frame(w, bd=1, relief=tix.RAISED)        
            demo_line3 = tix.StringVar()

            a = tix.ComboBox(top, label="Labels: ", dropdown=1,
                         command=select_month, editable=1, variable=demo_line3,
                         options='listbox.height 14 label.width 12 label.anchor e')
            a.pack(side=tix.TOP, anchor=tix.W)        
            for i in line3_list:
                a.insert(tix.END, i)

            a.set_silent('Please Select Label')
        
            box = tix.ButtonBox(w, orientation=tix.HORIZONTAL)
            box.add('ok', text='Ok', underline=0, width=6,
                    command=lambda w=w: ok_command(w))
            box.add('cancel', text='Cancel', underline=0, width=6,
                    command=lambda w=w: w.destroy())
            box.add('save&continue', text='Save & Continue', underline=0, width=15,
                    command=lambda w=w: sok_command(w))
            box.pack(side=tix.BOTTOM, fill=tix.X)
            top.pack(side=tix.TOP, fill=tix.BOTH, expand=1)
            
        def select_month(event=None):
        # tixDemo:Status "Month = %s" % demo_month.get()
            pass
            
        def select_year(event=None):
        # tixDemo:Status "Year = %s" % demo_year.get()
            pass
    
        def sok_command(w):
            global save1_label
            save1_label=1    
            global ok_label
            ok_label=1;
            w.destroy()
    
        def ok_command(w):
        # tixDemo:Status "Month = %s, Year= %s" % (demo_month.get(), demo_year.get())
            global ok_label
            ok_label=1;
            w.destroy()

                
        if __name__ == '__main__':
            root = tix.Tk()
            RunSample(root)
            root.mainloop()
                
        if ok_label==1:
            line3_st=demo_line3.get()
    
            if line3_st not in line3_list:
                line3_list.append(line3_st)
                desc_children[k].append(line3_st)
                
            line3=line3_list.index(line3_st)
            line3_box[4][desc]=k
            #print line3    
            #-------------------------------------------------------------------------------------------
            mm=len(contour_disp)
            deletelist=[]
            for i in range(mm):
                (x,y,w,h) = cv2.boundingRect(contour_disp[i])
                if (x>=r[0] and y>=r[1] and x+w<=r[0]+r[2] and y+h<=r[1]+r[3] ):
                    deletelist.insert(len(deletelist),i)
                    if (line3_st!='None' and line3_st!='Please Select Label'):
                        contours_line3[line3].append(contour_disp[i])
                    
                    
                    
            for i in reversed(range(len(deletelist))):
                contour_disp.pop(deletelist[i])
                
                
        if save1_label==1:
            cv2.destroyAllWindows()
            count=1
            final_line3_img=copy.deepcopy(in_img2R)
            ground_truth_desc_img=np.zeros((Vert,Horz))
            font = cv2.FONT_HERSHEY_SIMPLEX
            desc_box=np.zeros((4, len(desc_list)))

            for i in range(0,len(line3_list)):
                cont_cluster=copy.deepcopy(contours_line3[i])
                height, width, _ = in_img2R.shape
                min_x, min_y = width, height
                max_x = max_y = 0
    
                for c in cont_cluster:
                    (x,y,w,h) = cv2.boundingRect(c)
                    min_x, max_x = min(x, min_x), max(x+w, max_x)
                    min_y, max_y = min(y, min_y), max(y+h, max_y) 
        
                if max_x - min_x > 0 and max_y - min_y > 0:
                    cv2.rectangle(final_line3_img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
                    cv2.putText(final_line3_img, line3_list[i],(min_x+5, min_y-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
                    line3_box[0][i]=min_x
                    line3_box[1][i]=min_y
                    line3_box[2][i]=max_x
                    line3_box[3][i]=max_y
    
                print(len(cont_cluster))
                cv2.drawContours(final_line3_img, cont_cluster, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
                cv2.drawContours(ground_truth_line3_img, cont_cluster, -1, i,-1)   
     

            cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\Display-Layer3.jpg",final_line3_img) 
            cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\GT-Layer3.jpg",ground_truth_line3_img)
            
                    
            root = ET.Element("Page")
            doc = ET.SubElement(root, "Annotations")
            
            count=0
            for i in range(len(label_list)):
                if (len(contours_label[i])>0):
                    ET.SubElement(doc,label_list[i] , pattern="Layer-1", boundingbox= str(label_box[0][i])+','+str(label_box[1][i])+','+str(label_box[2][i])+','+str(label_box[3][i]), index=str(i))    
            
            Siblings_1=[]
            sibling_1=[]
            Siblings_1=[elem.tag for elem in doc.iter() if elem is not doc and len(label_children[label_list.index(elem.tag)])>0]
            
            for sibling_1 in Siblings_1:
                elem=doc.find(sibling_1)
                Siblings_2=[]
                Siblings_2 = label_children[label_list.index(sibling_1)]
                for sibling_2 in Siblings_2:
                    i=desc_list.index(sibling_2)
                    ET.SubElement(elem, sibling_2, pattern="Layer-2", boundingbox= str(desc_box[0][i])+','+str(desc_box[1][i])+','+str(desc_box[2][i])+','+str(desc_box[3][i]), index=str(desc_list.index(sibling_2)))
                    if len(desc_children[desc_list.index(sibling_2)])>0:
                        elem_2=elem.find(sibling_2)
                        Siblings_3=[]
                        Siblings_3 = desc_children[desc_list.index(sibling_2)]
                        for sibling_3 in Siblings_3:
                            j=line3_list.index(sibling_3)
                            ET.SubElement(elem_2, sibling_3, pattern="Layer-3", boundingbox= str(line3_box[0][j])+','+str(line3_box[1][j])+','+str(line3_box[2][j])+','+str(line3_box[3][j]), index=str(line3_list.index(sibling_3)))
        
            tree = ET.ElementTree(root)
            tree.write(path[0:(len(path)-4)]+"_Annotation\\Annotations.xml",encoding='utf8')
            #count=count+1
            #if count>20:
            #    break

 

cv2.destroyAllWindows()
count=1
final_line3_img=copy.deepcopy(in_img2R)
ground_truth_line3_img=np.zeros((Vert,Horz))
font = cv2.FONT_HERSHEY_SIMPLEX




for i in range(0,len(line3_list)):
    cont_cluster=copy.deepcopy(contours_line3[i])
    height, width, _ = in_img2R.shape
    min_x, min_y = width, height
    max_x = max_y = 0
            
    for c in cont_cluster:
        (x,y,w,h) = cv2.boundingRect(c)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y) 
                
    if max_x - min_x > 0 and max_y - min_y > 0:
        cv2.rectangle(final_line3_img, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
        cv2.putText(final_line3_img,line3_list[i],(min_x+5, min_y-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
        line3_box[0][i]=min_x
        line3_box[1][i]=min_y
        line3_box[2][i]=max_x
        line3_box[3][i]=max_y
                #line3_box[4][i]=k
                #desc_children[k].append(line3_list[i])
                
            #print(len(cont_cluster))
    cv2.drawContours(final_line3_img, cont_cluster, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
    cv2.drawContours(ground_truth_line3_img, cont_cluster, -1, i,-1)   

     
cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\Display-Layer3.jpg",final_line3_img) 
cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\GT-Layer3.jpg",ground_truth_line3_img)

root = ET.Element("Page")
doc = ET.SubElement(root, "Annotations")

count=0
for i in range(len(label_list)):
    if (len(contours_label[i])>0):
        ET.SubElement(doc,label_list[i] , pattern="Layer-1", boundingbox= str(label_box[0][i])+','+str(label_box[1][i])+','+str(label_box[2][i])+','+str(label_box[3][i]), index=str(i))    

Siblings_1=[]
sibling_1=[]
Siblings_1=[elem.tag for elem in doc.iter() if elem is not doc and len(label_children[label_list.index(elem.tag)])>0]

for sibling_1 in Siblings_1:
    elem=doc.find(sibling_1)
    Siblings_2=[]
    Siblings_2 = label_children[label_list.index(sibling_1)]
    for sibling_2 in Siblings_2:
        i=desc_list.index(sibling_2)
        ET.SubElement(elem, sibling_2, pattern="Layer-2", boundingbox= str(desc_box[0][i])+','+str(desc_box[1][i])+','+str(desc_box[2][i])+','+str(desc_box[3][i]), index=str(desc_list.index(sibling_2)))
        if len(desc_children[desc_list.index(sibling_2)])>0:
            elem_2=elem.find(sibling_2)
            Siblings_3=[]
            Siblings_3 = desc_children[desc_list.index(sibling_2)]
            for sibling_3 in Siblings_3:
                j=line3_list.index(sibling_3)
                ET.SubElement(elem_2, sibling_3, pattern="Layer-3", boundingbox= str(line3_box[0][j])+','+str(line3_box[1][j])+','+str(line3_box[2][j])+','+str(line3_box[3][j]), index=str(line3_list.index(sibling_3)))


tree = ET.ElementTree(root)
tree.write(path[0:(len(path)-4)]+"_Annotation\\Annotations.xml",encoding='utf8')
del final_line3_img
del ground_truth_line3_img
#del contours_desc
#--------------------------------------------------------------------------------------------------------------------------------
#---------------------Layer 4:word4 Image----------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

LANG=['English','Bengali','Hindi']
global lang
lang='English'
interupted=0
ok_label=0;
"global ok_label"
ok_label=0
"global save1_label"
save1_label=0
"global interupted"
interupted=0
count=1
img_cd1=copy.deepcopy(in_img2R)
font = cv2.FONT_HERSHEY_SIMPLEX
for i in range(len(word4_list)-1,0,-1):
    if word4_list[i]==[] or word4_list[i]=='None':
        word4_list.pop(i)
        word4_numberlist.pop(i)
    else:
        break



for k in range(len(line3_list)):

    contour_disp=[]
    cv2.destroyAllWindows()         
    count=1
    contour_all=copy.deepcopy(contours_line3[k])
    gray_img=cv2.cvtColor(ground_truth_word4_img,cv2.COLOR_BGR2GRAY)
    thresh, img_x = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY)
    img_x=img_x/255
    img_done=np.zeros((Vert,Horz))
    for c in range(len(contour_all)):
        cv2.drawContours(img_done, contour_all, c, 1,-1)
    img_todo=np.subtract(img_done,np.multiply(img_x,img_done))
    img_todo=img_todo.astype(np.uint8)
    contour_disp, hierarchy = cv2.findContours(img_todo,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contour_disp = sorted(contour_disp, key=cv2.contourArea, reverse = True)

            
    while (len(contour_disp) > 0 and interupted==0):
        print ("Please Select ROI, All Labels are not Marked\n")
                #tkMessageBox.showinfo("Title", "Please Select ROI, All Labels are not Marked")
        fromCenter = False
        img_cd1=np.zeros((Vert,Horz))
        img_cd1=copy.deepcopy(in_img2R)
        cv2.rectangle(img_cd1, (int(line3_box[0][k]), int(line3_box[1][k]) ), (int(line3_box[2][k]) , int(line3_box[3][k])), (255, 0, 0), 2)
        cv2.putText(img_cd1,line3_list[k],(int(line3_box[0][k])+5, int(line3_box[1][k])-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
                #cv2.drawContours(img_cd1, contour_disp, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
        for c in range(len(contour_disp)):
            rr=random.randint(1,255)
            gg=random.randint(1,255)
            bb=random.randint(1,255)
            cv2.drawContours(img_cd1, contour_disp, c, (rr,gg,bb),-1)

                
        cv2.putText(img_cd1,"Layer-4 Annonation",(5, 12), font, 1, (100,55,55), 2, cv2.LINE_AA)
                #r = cv2.selectROI(img_cd1, fromCenter)
        r=[0,0,0,0]
        kk=0
        if __name__ == '__main__':        
            main2(img_cd1,line3_box,k)
        
        
                #--------------------Select Label---------------------------------------------------
        def RunSample(w):
            global demo_word4 
            global demo_langdisp4
            global demo_lang4
            global demo_word4_number
            global ok_label
            ok_label=0;    
            top = tix.Frame(w, bd=1, relief=tix.RAISED)
                    
            demo_word4 = tix.StringVar()
            demo_word4_number = tix.StringVar()
            demo_lang4 = tix.StringVar()
                    

            c = tix.ComboBox(top, label="Word Number: ", dropdown=1,
                             command=select_month, editable=1, variable=demo_word4_number,
                             options='listbox.height 14 label.width 18 label.anchor e')
            c.pack(side=tix.TOP, anchor=tix.W)        
            for i in word4_numberlist:
                c.insert(tix.END, i)  
                    
            c.set_silent('word-' + str(len(word4_numberlist)))
                    
            a = tix.ComboBox(top, label="Word Descripton: ", dropdown=1,
                             command=select_month, editable=1, variable=demo_word4,
                             options='listbox.height 14 label.width 18 label.anchor e')
            a.pack(side=tix.TOP, anchor=tix.W)        
            for i in word4_list:
                a.insert(tix.END, i)
                    
            a.set_silent('Please write word')
                    
            b = tix.ComboBox(top, label="Language: ", dropdown=1,
                        command=select_month, editable=0, variable=demo_lang4,
                        options='listbox.height 3 label.width 18 label.anchor e')
            b.pack(side=tix.TOP, anchor=tix.W)        
            for i in LANG:
                b.insert(tix.END, i)
            b.set_silent(lang)
                    #demo_langdisp4 =  avro.parse(demo_word4.get())
            box = tix.ButtonBox(w, orientation=tix.HORIZONTAL)
            box.add('b_display', text='বাংলা হরফ', underline=0, width=15,
                    command=lambda w=w: select_month2(w))
            box.add('h_display', text='हिन्दी हरफ', underline=0, width=15,
                    command=lambda w=w: select_month3(w))
            box.add('ok', text='Ok', underline=0, width=6,
                    command=lambda w=w: ok_command(w))
            box.add('cancel', text='Cancel', underline=0, width=6,
                    command=lambda w=w: w.destroy())
            box.add('save&continue', text='Save & Continue', underline=0, width=15,
                    command=lambda w=w: sok_command(w))

            box.pack(side=tix.BOTTOM, fill=tix.X)
            top.pack(side=tix.TOP, fill=tix.BOTH, expand=1)
                    
        def select_month2(w):
                # tixDemo:Status "Month = %s" % demo_month.get()
            beng_disp=avro.parse(demo_word4.get())
            label_2=tix.Label(w)
            label_2["text"]=beng_disp
            label_2.pack(side=tix.TOP, anchor=tix.W) 
                    
        def select_month3(w):
                # tixDemo:Status "Month = %s" % demo_month.get()
            beng_disp=hinavro.parse(demo_word4.get())
            label_2=tix.Label(w)
            label_2["text"]=beng_disp
            label_2.pack(side=tix.TOP, anchor=tix.W) 
                        
        def select_year(event=None):
                # tixDemo:Status "Year = %s" % demo_year.get()
            pass
                
        def ok_command(w):
        # tixDemo:Status "Month = %s, Year= %s" % (demo_month.get(), demo_year.get())
            global ok_label
            ok_label=1
            w.destroy()
        
        def sok_command(w):
            global save1_label
            save1_label=1    
            global ok_label
            ok_label=1;
            w.destroy()

                    
        if __name__ == '__main__':
            root = tix.Tk()
            RunSample(root)
            root.mainloop()
                    
        print (ok_label)
        if ok_label==1:
            lang=demo_lang4.get()
            if (lang == "Bengali"):
                word4_st=avro.parse(demo_word4.get())
            elif (lang == "Hindi"):
                word4_st=hinavro.parse(demo_word4.get())
            else:
                word4_st=demo_word4.get()

                    
            wordnum4_st=demo_word4_number.get()
            if wordnum4_st not in word4_numberlist:
                word4_numberlist.append(wordnum4_st)
                word4_list.append(word4_st)
                line3_children[k].append(wordnum4_st)
                    
            try:
                word4=word4_numberlist.index(wordnum4_st)
                print (word4)
                word4_box[4][word4]=k
            except:
                print ("Error is there")
                
#-------------------------------------------------------------------------------------------
            mm=len(contour_disp)
            deletelist=[]
            for i in range(mm):
                (x,y,w,h) = cv2.boundingRect(contour_disp[i])
                if (x>=r[0] and y>=r[1] and x+w<=r[0]+r[2] and y+h<=r[1]+r[3] ):                        
                    deletelist.insert(len(deletelist),i)
                    if (word4_st!='None' and word4_st!='Please write word' and word4_st!='word-0'):
                        contours_word4[word4].append(contour_disp[i])
                        
                    
                    
            for i in reversed(range(len(deletelist))):
                contour_disp.pop(deletelist[i])
                
        if save1_label==1:
            final_word4_img=copy.deepcopy(in_img2R)
            ground_truth_word4_img=np.zeros((Vert,Horz))
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            for i in range(0,1000):
                cont_cluster=copy.deepcopy(contours_word4[i])
                height, width, _ = in_img2R.shape
                min_x, min_y = width, height
                max_x = max_y = 0
                            
                for c in cont_cluster:
                    (x,y,w,h) = cv2.boundingRect(c)
                    min_x, max_x = min(x, min_x), max(x+w, max_x)
                    min_y, max_y = min(y, min_y), max(y+h, max_y) 
                                
                if max_x - min_x > 0 and max_y - min_y > 0:
                    cv2.rectangle(final_word4_img, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
                                #cv2.putText(final_word4_img,word4_list[i],(min_x+5, min_y-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
                    word4_box[0][i]=min_x
                    word4_box[1][i]=min_y
                    word4_box[2][i]=max_x
                    word4_box[3][i]=max_y
                    #word4_box[4][i]=k
                    line3_children[k].append(word4_numberlist[i])
                                
                        #print(len(cont_cluster))
                cv2.drawContours(final_word4_img, cont_cluster, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
                cv2.drawContours(ground_truth_word4_img, cont_cluster, -1, i,-1)   
                            
                            
            cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\Display-Layer4.jpg",final_word4_img) 
            cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\GT-Layer4.jpg",ground_truth_word4_img) 
            
            
            
            
            #=============================================NEW TREE=================================================================================================
            
            root = ET.Element("Page")
            doc = ET.SubElement(root, "Annotations")
            
            count=0
            for i in range(len(label_list)):
                if (len(contours_label[i])>0):
                    ET.SubElement(doc,label_list[i] , pattern="Layer-1", boundingbox= str(label_box[0][i])+','+str(label_box[1][i])+','+str(label_box[2][i])+','+str(label_box[3][i]), index=str(i))    
            
            Siblings_1=[]
            sibling_1=[]
            Siblings_1=[elem.tag for elem in doc.iter() if elem is not doc and len(label_children[label_list.index(elem.tag)])>0]
            
            for sibling_1 in Siblings_1:
                elem=doc.find(sibling_1)
                Siblings_2=[]
                Siblings_2 = label_children[label_list.index(sibling_1)]
                for sibling_2 in Siblings_2:
                    i=desc_list.index(sibling_2)
                    ET.SubElement(elem, sibling_2, pattern="Layer-2", boundingbox= str(desc_box[0][i])+','+str(desc_box[1][i])+','+str(desc_box[2][i])+','+str(desc_box[3][i]), index=str(desc_list.index(sibling_2)))
                    if len(desc_children[desc_list.index(sibling_2)])>0:
                        elem_2=elem.find(sibling_2)
                        Siblings_3=[]
                        Siblings_3 = desc_children[desc_list.index(sibling_2)]
                        for sibling_3 in Siblings_3:
                            j=line3_list.index(sibling_3)
                            ET.SubElement(elem_2, sibling_3, pattern="Layer-3", boundingbox= str(line3_box[0][j])+','+str(line3_box[1][j])+','+str(line3_box[2][j])+','+str(line3_box[3][j]), index=str(line3_list.index(sibling_3)))
                            if len(line3_children[line3_list.index(sibling_3)])>0:
                                elem_3=elem_2.find(sibling_3)
                                Siblings_4=[]
                                Siblings_4 = line3_children[line3_list.index(sibling_3)]
                                for sibling_4 in Siblings_4:
                                    k=word4_numberlist.index(sibling_4)
                                    ET.SubElement(elem_3,sibling_4, spelling=word4_list[word4_numberlist.index(sibling_4)], pattern="Layer-4", boundingbox= str(word4_box[0][k])+','+str(word4_box[1][k])+','+str(word4_box[2][k])+','+str(word4_box[3][k]), index=str(word4_numberlist.index(sibling_4)))
            
                
            tree = ET.ElementTree(root)
            tree.write(path[0:(len(path)-4)]+"_Annotation\\Annotations.xml",encoding='utf8')
                    
                    
                    #count=count+1
                    #if count>20:
                    #    break

 

cv2.destroyAllWindows()
count=1
final_word4_img=copy.deepcopy(in_img2R)
ground_truth_word4_img=np.zeros((Vert,Horz))
font = cv2.FONT_HERSHEY_SIMPLEX

for i in range(0,1000):
    cont_cluster=copy.deepcopy(contours_word4[i])
    height, width, _ = in_img2R.shape
    min_x, min_y = width, height
    max_x = max_y = 0
                
    for c in cont_cluster:
        (x,y,w,h) = cv2.boundingRect(c)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y) 
                    
    if max_x - min_x > 0 and max_y - min_y > 0:
        cv2.rectangle(final_word4_img, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
                    #cv2.putText(final_word4_img,word4_list[i],(min_x+5, min_y-5), font, 0.5, (100,55,55), 2, cv2.LINE_AA)
        word4_box[0][i]=min_x
        word4_box[1][i]=min_y
        word4_box[2][i]=max_x
        word4_box[3][i]=max_y
        #word4_box[4][i]=k
        #line3_children[k].append(word4_numberlist[i])
                    
            #print(len(cont_cluster))
    cv2.drawContours(final_word4_img, cont_cluster, -1, (random.randint(1,10)*25,random.randint(1,10)*25,random.randint(1,10)*25),-1)
    cv2.drawContours(ground_truth_word4_img, cont_cluster, -1, i,-1)   
                
                
cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\Display-Layer4.jpg",final_word4_img) 
cv2.imwrite(path[0:(len(path)-4)]+"_Annotation\\GT-Layer4.jpg",ground_truth_word4_img) 




#=============================================NEW TREE=================================================================================================

root = ET.Element("Page")
doc = ET.SubElement(root, "Annotations")

count=0
for i in range(len(label_list)):
    if (len(contours_label[i])>0):
        ET.SubElement(doc,label_list[i] , pattern="Layer-1", boundingbox= str(label_box[0][i])+','+str(label_box[1][i])+','+str(label_box[2][i])+','+str(label_box[3][i]), index=str(i))    

Siblings_1=[]
sibling_1=[]
Siblings_1=[elem.tag for elem in doc.iter() if elem is not doc and len(label_children[label_list.index(elem.tag)])>0]

for sibling_1 in Siblings_1:
    elem=doc.find(sibling_1)
    Siblings_2=[]
    Siblings_2 = label_children[label_list.index(sibling_1)]
    for sibling_2 in Siblings_2:
        i=desc_list.index(sibling_2)
        ET.SubElement(elem, sibling_2, pattern="Layer-2", boundingbox= str(desc_box[0][i])+','+str(desc_box[1][i])+','+str(desc_box[2][i])+','+str(desc_box[3][i]), index=str(desc_list.index(sibling_2)))
        if len(desc_children[desc_list.index(sibling_2)])>0:
            elem_2=elem.find(sibling_2)
            Siblings_3=[]
            Siblings_3 = desc_children[desc_list.index(sibling_2)]
            for sibling_3 in Siblings_3:
                j=line3_list.index(sibling_3)
                ET.SubElement(elem_2, sibling_3, pattern="Layer-3", boundingbox= str(line3_box[0][j])+','+str(line3_box[1][j])+','+str(line3_box[2][j])+','+str(line3_box[3][j]), index=str(line3_list.index(sibling_3)))
                if len(line3_children[line3_list.index(sibling_3)])>0:
                    elem_3=elem_2.find(sibling_3)
                    Siblings_4=[]
                    Siblings_4 = line3_children[line3_list.index(sibling_3)]
                    for sibling_4 in Siblings_4:
                        k=word4_numberlist.index(sibling_4)
                        ET.SubElement(elem_3,sibling_4, spelling=word4_list[word4_numberlist.index(sibling_4)], pattern="Layer-4", boundingbox= str(word4_box[0][k])+','+str(word4_box[1][k])+','+str(word4_box[2][k])+','+str(word4_box[3][k]), index=str(word4_numberlist.index(sibling_4)))

    
tree = ET.formstring(root)
tree.write(path[0:(len(path)-4)]+"_Annotation\\Annotations.xml",encoding='utf8')# -*- coding: utf-8 -*-