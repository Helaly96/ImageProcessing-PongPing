import cv2
import numpy as np


def Crop_Image(event, x, y, flags, param):
    global cropping
    global end_drawing
    global current_pos

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
        points.append((x, y))
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        points.append((x, y))
        cropping = False
        cv2.rectangle(frame, points[0], points[1], (0, 255, 0), 2)
        end_drawing = True

    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        current_pos = (x, y)



def Stadium_segment(image):
    lower_stadium = np.array([100,80,90], dtype=np.uint8)
    upper_stadium = np.array([110,110,185], dtype=np.uint8)
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

        elif(abs(y-prev_point[1]) >0.4*height_of_rectangle):
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


#to hold image of rect
points=[]

cropping = False

#current mouse position
current_pos=(0,0)
end_drawing=False

#define a window
cv2.namedWindow('Original_First_Frame')
#the window the mouse events binded to that windows
cv2.setMouseCallback('Original_First_Frame',Crop_Image)

#read from video
cap = cv2.VideoCapture('Edmonton.mp4')

#read it
clone = cv2.imread("Testing_Ball_HSV/x.jpg")
#keep showing the image, so we can draw on it hehe.
while(1):
    frame = clone.copy()
    if(cropping and current_pos!=(0,0)):
        cv2.rectangle(frame, points[0], current_pos, (255, 0, 0), 2)
    k = cv2.waitKey(20) & 0xFF
    if end_drawing:
        break
    cv2.imshow('Original_First_Frame',frame)


#destroy the first frame
cv2.destroyAllWindows()




saved_frame=[]
no_of_frames_to_be_considered=700
#Capture the first selected_no frames
while(1):
    ret, frame = cap.read()
    frame = cvt_hsv(frame)
    frame= frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]
    mask = Stadium_segment(frame)
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    if len(saved_frame) < no_of_frames_to_be_considered:
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

    Right_Half = cv2.convexHull(contours[0])
    Left_Half = cv2.convexHull(contours[1])


    cv2.drawContours(image_to_be_displayed, [Right_Half],-1, (255, 255,255), 3)
    cv2.drawContours(image_to_be_displayed, [Left_Half], -1, (255, 0, 0), 3)

    #cv2.fillPoly(image_to_be_displayed, pts=[Right_Half], color=(255, 255, 255))
    #cv2.fillPoly(image_to_be_displayed, pts=[Left_Half], color=(255, 255, 255))


    pts,image_to_be_displayed = Bounding_Box_Of_Stadium(Right_Half,image_to_be_displayed)
    pts, image_to_be_displayed = Bounding_Box_Of_Stadium(Left_Half, image_to_be_displayed)

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

