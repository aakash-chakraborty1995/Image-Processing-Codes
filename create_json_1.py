# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 16:14:45 2022

@author: akash
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 16:38:57 2022

@author: akash
"""
import json

def write_json(new_data, filename = 'C:/Akash/Study/datasets/EAST_Dataset/new_1.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["images"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)
        
        
num = 1
# num_ = 1


for i in range(1, 801):
    path_1 = f"C:/Akash/Study/datasets/EAST_Dataset/train_gt/gt_img_{num}.txt"
    my_file =  open(path_1)
    # list1 = []
    
    # for line in my_file:
    #     strip_lines=line.strip()
    #     listli = strip_lines.split(",")
    #     # listlj = [int(min(listli[0],listli[6])),int(min(listli[1],listli[3])),int(max(listli[2],listli[4]))-int(min(listli[0],listli[6])),int(max(listli[5],listli[7]))-int(min(listli[1],listli[3]))]
    #     # L = listli
        
       
    list1 = {"date_captured":"2022","file_name":f"image/train/img_{num}.jpg", "height":720,  "id":num, "license":1,"url":"", "width": 1200}

    jsonString = json.dumps(list1, indent=4)
    jsonString = json.loads(jsonString)
    print(jsonString)
    write_json(jsonString)
    # num_ += 1
        
    num += 1
    # num_ += 1 
