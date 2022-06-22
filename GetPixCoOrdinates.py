import cv2

clicks = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
       clicks.append((x,y))
       if len(clicks) > 3:
          print(str(clicks).strip('[]').strip('()').replace('), (', ','))
          clicks.clear()  
        
        
        
if __name__=="__main__":
    img = cv2.imread("/home/heisenberg/Study/Database/EAST_Dataset/train_img_new/train_img_38.jpg")
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
