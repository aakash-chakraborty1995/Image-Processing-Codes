 import cv2
 import glob

 image_list_1 = []
 image_list_2 = []

 path1='path of the folder where the images are'
 path2='path of the folder where the images are'

 num_1 = 1

 for file1 in glob.glob(path1 + '/*.jpg'): 
     im1=cv2.imread(file1)
     image_list_1.append(im1)

 for file2 in glob.glob(path2 + '/*.jpg'): 
     im2=cv2.imread(file2)
     image_list_2.append(im2)    

 for i in range(0,len(image_list_1)):
     im1 = image_list_1[i]
     im2 = image_list_2[i]
     dest_and = cv2.bitwise_and(im2, im1, mask = None)

     cv2.imwrite('path where the output images will be saved/image_'+str(num_1)+'.jpg', dest_and)
     num_1 += 1
