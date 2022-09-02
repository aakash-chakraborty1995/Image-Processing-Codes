# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 18:39:46 2022

@author: akash
"""
import json

#L =open('C:/Akash/Study/Code Library/CORE-Text-main/ICDAR2017_train.json')
file_name = 'C:/Akash/Study/Code Library/CORE-Text-main/ICDAR2017_train.json'

with open(file_name, 'r', encoding='utf-8') as f:
    my_data = json.loads(f.read())
    for i in my_data["annotations"]:
        print(i["id"])
        
 
#for i in L_Dict["annotations"]:
 #        print(i['id'])