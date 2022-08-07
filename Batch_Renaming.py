#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 18:44:56 2022

@author: heisenberg
"""

# Python 3 code to rename multiple
# files in a directory or folder

# importing os module
import os

# Function to rename multiple files
def main():

	folder = "/home/heisenberg/Study/Database/New_Rsearch/img/dst_imgs/Images_Research_1"
	for count, filename in enumerate(os.listdir(folder)):
		dst = "G_img_ {str(count)}.jpg"
		src ="/home/heisenberg/Study/Database/New_Rsearch/img/dst_imgs/Images_Research_1" # foldername/filename, if .py file is outside folder
		dst ="/home/heisenberg/dst/home/heisenberg/Study/Database/New_Rsearch/img/dst_imgs/Images_Research_1"
		
		# rename() function will
		# rename all the files
		os.rename(src, dst)

# Driver Code
if __name__ == '__main__':
	
	# Calling main() function
	main()
