import numpy as np
import cv2

def color_pick(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #print("Value of clicked position is ")
        cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
        #print("X is "+ str(x))
        #print("Y is "+ str(y))
        print(hsv[y,x])



def cvt_hsv(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    return image

#define a window
name_of_image = input("Enter Name of File you want to read \n")
cv2.namedWindow('pick')
#the window the mouse events binded to that windows
cv2.setMouseCallback('pick',color_pick)
image = cv2.imread(name_of_image)

while(1):
    frame = image
    hsv = cvt_hsv(frame)
    k = cv2.waitKey(20) & 0xFF
    if(k == ord('e') ):
        break
    cv2.imshow("pick",image)
    cv2.imshow("hsv",hsv)

