import numpy as np
import cv2



#-----------------/ The Bounding Box /--------------------



#to hold image of rect
points=[]

cropping = False

#current mouse position
current_pos=(0,0)
end_drawing=False

#the mouse call back event , i binded it to the very first frame
#basically i want the user to click 4 points, that will be the 
#ROI of interest
#THIS IS JUST FOR TESTING, THE ROI will be the table of pingpong

def Crop_Image(event,x,y,flags,param):
    global cropping
    global end_drawing
    global current_pos

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frame,(x,y),10,(255,0,0),-1)
        points.append( (x,y) )
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        points.append((x,y))
        cropping = False
        cv2.rectangle(frame, points[0], points[1], (0, 255, 0), 2)
        end_drawing=True

    elif event == cv2.EVENT_MOUSEMOVE and cropping :
        current_pos=(x,y)
		

		# draw a rectangle around the region of interest

#Color Filtering Function

def colorSegment(frame):
    lower = np.array([80,0,0])
    upper = np.array([124,120,255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame,frame, mask = mask)
    return res



#define a window
cv2.namedWindow('Original_First_Frame')
#the window the mouse events binded to that windows
cv2.setMouseCallback('Original_First_Frame',Crop_Image)

#read from video
cap = cv2.VideoCapture('Testing-pingpong.mp4')

#read first frame of video
ret,frame = cap.read()

#write the first frame
cv2.imwrite("x.jpg",frame)

#read it
clone = cv2.imread("x.jpg")

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
cap.release()



#--------------------/ Video Processing /------------------



#Parameters for the difference
sensitivityValue1 = 50
sensitivityValue2 = 80
blurSize = (9,9)

#read from video
cap = cv2.VideoCapture('Testing-pingpong.mp4')
_, frame = cap.read()
frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]
#frame = colorSegment(frame)
grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
previous = grayImage.copy()

while(1):
    _, frame = cap.read()
    frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]
    #frame = colorSegment(frame)
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    differenceImage = cv2.absdiff(grayImage, previous)
    _, thresholdImage = cv2.threshold(differenceImage, sensitivityValue1, 255, cv2.THRESH_BINARY)
	
    #Blurring the Image to get rid of noise
    finalThresholdImage = cv2.blur(thresholdImage, blurSize)
    _, finalThresholdImage = cv2.threshold(finalThresholdImage, sensitivityValue2, 255, cv2.THRESH_BINARY)
    

    #Contour Detection
    #Contour Parameters
    perimeterMin = 10
    perimeterMax = 40
    epsilon = 0.03
    numberOfAcceptedContours = 4

    #Blank frame to draw the contour on
    blankFrame = np.zeros(frame.shape)

    contours, hierarchy = cv2.findContours(finalThresholdImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:numberOfAcceptedContours]
    real_cnts=[]

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, epsilon * cv2.arcLength(cnt, True), True)
        perimeter = cv2.arcLength(cnt, True)
        if(len(approx) > 3 and perimeter > perimeterMin and perimeter < perimeterMax):
            k = cv2.isContourConvex(approx)
            if(k):
                real_cnts.append((cnt))
    
    cv2.drawContours(frame, real_cnts, -1, (0, 255, 0), 2)

    '''
    #Apply Hough Circle
    #Hough Circle Parameters
    #dp: This parameter is the inverse ratio of the accumulator resolution to the image resolution (see Yuen et al. for more details). Essentially, the larger the dp gets, the smaller the accumulator array gets.
    dp = 1.2
    #minDist: Minimum distance between the center (x, y) coordinates of detected circles. If the minDist is too small, multiple circles in the same neighborhood as the original may be (falsely) detected. If the minDist is too large, then some circles may not be detected at all.
    minDist = 0
    if len(real_cnts) > 5 :
        circles = cv2.HoughCircles(blankFrame, cv2.HOUGH_GRADIENT, dp, minDist)

        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 3)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    '''

    #Window Showing

    cv2.imshow('Difference Image',differenceImage)
    cv2.imshow('Threshold Image',thresholdImage)
    cv2.imshow('Final Threshold Image', finalThresholdImage)
    cv2.imshow('Contour Detected', frame)


    previous = grayImage.copy() 

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k==ord('h'):
        h_lower=int(input("Enter Lower Hue's Value \n"))
        h_higher=int(input("Enter Upper Hue's Value \n"))
    elif k==ord('v'):
        v_lower=int(input("Enter Lower Value's Value \n"))
        v_higher=int(input("Enter Lower Value's Value \n"))
    elif k==ord('s'):
        s_lower=int(input("Enter Lower Saturation's Value \n"))
        s_higher=int(input("Enter Lower Saturation's Value \n"))
    elif k==ord('p'):
        x=input()

cap.release()
cv2.destroyAllWindows()