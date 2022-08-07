#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 01:20:10 2022

@author: heisenberg
"""

import os
# Function to rename multiple files
def main():
   i = 652
   path="/home/heisenberg/Study/Database/New_Rsearch/img/dst_imgs/Images_Research_1/"
   for filename in os.listdir(path):
      my_dest ="train_img_" + str(i+1) + ".jpg"
      my_source =path + filename
      my_dest =path + my_dest
      # rename() function will
      # rename all the files
      os.rename(my_source, my_dest)
      i += 1
# Driver Code
if __name__ == '__main__':
   # Calling main() function
   main()