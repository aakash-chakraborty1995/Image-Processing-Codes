# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 16:38:57 2022

@author: akash
"""
import json

def write_json(new_data, filename = 'C:/Akash/Study/datasets/EAST_Dataset/train.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["annotations"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)
        
        
num = 1
num_ = 1


for i in range(1, 801):
    path_1 = f"C:/Akash/Study/datasets/EAST_Dataset/Experiment/train_gt/img_{num}.txt"
    my_file =  open(path_1)
    list1 = []
    
    for line in my_file:
        strip_lines=line.strip()
        listli = strip_lines.split(",")
        listlj = [int(min(listli[0],listli[6])),int(min(listli[1],listli[3])),int(max(listli[2],listli[4]))-int(min(listli[0],listli[6])),int(max(listli[5],listli[7]))-int(min(listli[1],listli[3]))]
        L = listli
        
        list1 = {"area":listlj[2]*listlj[3],"bbox":[listlj], "category_id":1, "id":num_, "image_id":num, "iscrowd":0, "segmentation":[[int(L[0]),int(L[1]),int(L[2]),int(L[3]),int(L[4]),int(L[5]),int(L[6]),int(L[7])]]}

        jsonString = json.dumps(list1, indent=4)
        jsonString = json.loads(jsonString)
        print(jsonString)
        write_json(jsonString)
        num_ += 1
        
    num += 1
    num_ += 1 
