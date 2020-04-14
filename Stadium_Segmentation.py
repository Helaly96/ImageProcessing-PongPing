import numpy as np
import cv2
import imutils

def Stadium_segment(image):
    lower_stadium = np.array([100,80,120], dtype=np.uint8)
    upper_stadium = np.array([110,110,190], dtype=np.uint8)
    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(image, lower_stadium, upper_stadium)
    # Bitwise-AND mask and original image
    mask = cv2.bitwise_and(frame,frame, mask= mask)
    
    return mask

def draw_circles_of_points(c,image_to_be_displayed):
    for point in c:
        x,y = point.ravel()
        cv2.circle(image_to_be_displayed, (x,y), 8, (255, 255, 255), -1)
    return image_to_be_displayed


def Bounding_Box_Of_Stadium(c,image_to_be_displayed):

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,500)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    
    max_x=0
    y_max_x=0

    min_x=2000
    y_min_x=0

    max_y=0
    x_max_y=0

    min_y=2000
    x_min_y=0


    for point in c:
        x,y=point.ravel()
        if(x>max_x):
            max_x=x
            y_max_x=y
        elif(x<min_x):
            min_x=x
            y_min_x=y         
        if(y>max_y):
            max_y=y
            x_max_y=x
        elif(y<min_y):
            min_y=y
            x_min_y=x

    widht_of_rectangle=max_x-min_x
    height_of_rectangle=max_y-min_y

    #first point of hull is lower right?
    cv2.circle(image_to_be_displayed, tuple(c[0][0]), 8, (255, 255, 255), -1)
    
    cv2.putText(image_to_be_displayed,'1', 
                tuple(c[0][0]), 
                font, 
                fontScale,
                fontColor,
                lineType
                )

    prev_point=c[0][0]

    first_time_x=False
    count=1
    for point in c:
        
        if count==4:
            break
        x,y=point.ravel()
        if( (abs(x-prev_point[0])>0.85*widht_of_rectangle) and (not first_time_x)):
            count+=1
            first_time_x=True
            cv2.circle(image_to_be_displayed, (x,y), 8, (0, 255, 0), -1)
            prev_point = list((x,y))
            cv2.putText(image_to_be_displayed,str(count), 
                (x,y), 
                font, 
                fontScale,
                fontColor,
                lineType
                )
        
        elif(abs(x-prev_point[0]) >0.6*widht_of_rectangle and first_time_x):
            count+=1
            cv2.circle(image_to_be_displayed, (x,y), 8, (255, 0, 0), -1)
            prev_point = list((x,y))
            cv2.putText(image_to_be_displayed,str(count), 
                (x,y), 
                font, 
                fontScale,
                fontColor,
                lineType
                )

        elif(abs(y-prev_point[1]) >0.7*height_of_rectangle):
            count+=1
            cv2.circle(image_to_be_displayed, (x,y), 8, (0, 0, 255), -1)
            prev_point = list((x,y))
            cv2.putText(image_to_be_displayed,str(count), 
                (x,y), 
                font, 
                fontScale,
                fontColor,
                lineType
                )    
                
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c,0.04 *peri, True)
    return len(approx),image_to_be_displayed


def cvt_hsv(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    return image

def color_pick(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print("Value of clicked position is")
        print(frame[y,x])

#read from video
cap = cv2.VideoCapture('Testing-pingpong.mp4')

saved_frame=[]

no_of_frames_to_be_considered=700

#Capture the first selected_no frames 
while(1):
    ret, frame = cap.read()
    frame = cvt_hsv(frame)
    mask = Stadium_segment(frame)
    if(len(saved_frame) < no_of_frames_to_be_considered):
        saved_frame.append(mask)
    else:
        break

current_area=[]
displayed_frame=[]
no_of_corner=[]
max_area = 0

#len(saved_frame)
for i in range(len(saved_frame)):
    image_to_be_displayed=cv2.cvtColor(saved_frame[i],cv2.COLOR_HSV2BGR)
    Grayed=cv2.cvtColor(image_to_be_displayed,cv2.COLOR_BGR2GRAY)
    ret,result = cv2.threshold(Grayed,100,255,cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(result,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:4]
    hull = cv2.convexHull(contours[0])
    cv2.drawContours(image_to_be_displayed, [hull],-1, (255, 255,255), 3)     
    pts,image_to_be_displayed = Bounding_Box_Of_Stadium(hull,image_to_be_displayed)
    no_of_corner.append(pts)
    displayed_frame.append(image_to_be_displayed)
    Area=0
    for j in range(len(contours)):
        Area += cv2.contourArea(contours[j])
    current_area.append(Area)
    cv2.imshow("X",image_to_be_displayed)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('k'):
        break


current_area=np.array(current_area)
index=np.argmax(current_area)
cv2.imshow("X",saved_frame[index])
cv2.imshow("Frame with maximum area with contours drawn",displayed_frame[index])
cv2.waitKey(0)

