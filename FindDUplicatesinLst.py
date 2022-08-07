#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:49:21 2022

@author: heisenberg
"""

l=[1, 10, 23, 7, 10, 3, 3, 90]
l_new=[]
for i in l:
    if i not in l_new:
        l_new.append(i)
    else:
        print(i,end=' ')