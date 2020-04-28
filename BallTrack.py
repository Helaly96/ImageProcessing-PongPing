import numpy as np
import cv2
import math
''' -----------------/ The Bounding Box /--------------------'''


# to hold image of rect
points = []

cropping = False

# current mouse position
current_pos = (0, 0)
end_drawing = False


# the mouse call back event , i binded it to the very first frame
# basically i want the user to click 4 points, that will be the
# ROI of interest
# THIS IS JUST FOR TESTING, THE ROI will be the table of pingpong

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

    # draw a rectangle around the region of interest


def find_length(pt1,pt2):
    return int(math.sqrt( (pt1[1]-pt2[1])**2 + (pt1[0]-pt2[0])**2 ))

# Color Filtering Function
def contours_center(c):
    if c is not None:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    return cX,cY

def colorSegment(frame):
    lower = np.array([80, 0, 0])
    upper = np.array([120, 100, 255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    return res

# define a window
cv2.namedWindow('Original_First_Frame')
# the window the mouse events binded to that windows
cv2.setMouseCallback('Original_First_Frame', Crop_Image)

# read from video
cap = cv2.VideoCapture('Edmonton.mp4')

# read first frame of video
ret, frame = cap.read()

# write the first frame
cv2.imwrite("Testing_Ball_HSV/x.jpg", frame)

# read it
clone = cv2.imread("Testing_Ball_HSV/x.jpg")

all_contours = []

# keep showing the image, so we can draw on it hehe.
while True:
    frame = clone.copy()
    if cropping and current_pos != (0, 0):
        cv2.rectangle(frame, points[0], current_pos, (255, 0, 0), 2)
    k = cv2.waitKey(20) & 0xFF
    if end_drawing:
        break
    cv2.imshow('Original_First_Frame', frame)

# destroy the first frame
cv2.destroyAllWindows()
cap.release()

''' --------------------/ Video Processing /------------------ '''

# Parameters for the difference
sensitivityValue1 = 60
sensitivityValue2 = 75
blurSize = (15, 15)

# read from video
cap = cv2.VideoCapture('Edmonton.mp4')
_, frame = cap.read()
frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]
# frame = colorSegment(frame)
grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
previous = grayImage.copy()


#holds a record of previous ball positions
trajectories=[]

#differences
differences=[]

while True:
    _, frame = cap.read()
    if frame is None:
        break

    frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]
    # frame = colorSegment(frame)
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    differenceImage = cv2.absdiff(grayImage, previous)
    blur = cv2.GaussianBlur(differenceImage, (5, 5), cv2.BORDER_DEFAULT)
    _, thresholdImage = cv2.threshold(blur, sensitivityValue1, 255, cv2.THRESH_BINARY)

    # Blurring the Image to get rid of noise
    finalThresholdImage = cv2.GaussianBlur(thresholdImage, blurSize, cv2.BORDER_DEFAULT)
    _, finalThresholdImage = cv2.threshold(finalThresholdImage, sensitivityValue2, 255, cv2.THRESH_BINARY)
    cv2.imshow("FFF",finalThresholdImage)

    # Opening
    structuringElementSize = (7,7)
    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, structuringElementSize)
    finalThresholdImage = cv2.morphologyEx(thresholdImage, cv2.MORPH_OPEN, structuringElement)

    finalThresholdImage = cv2.GaussianBlur(finalThresholdImage, (5, 5), cv2.BORDER_DEFAULT)

    cv2.imshow("Final Thresholded_image", cv2.bitwise_and(frame,frame,mask=finalThresholdImage))
    # Contour Detection
    # Contour Parameters
    perimeterMin = 50
    perimeterMax = 800
    epsilon = 0.03
    numberOfAcceptedContours = 4

    # Blank frame to draw the contour on
    blankFrame = np.zeros(frame.shape)


    #instead of getting a tree of contours (ie, each contour contain a child)
    #contours, hierarchy = cv2.findContours(finalThresholdImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #we can get only top levels contours
    contours, hierarchy = cv2.findContours(finalThresholdImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:numberOfAcceptedContours]
    real_cnts = []

    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        if perimeterMin < perimeter < perimeterMax:
            #if cv2.isContourConvex(approx):
            if cv2.contourArea(cnt) < 300:
                real_cnts.append(cnt)


    #comment the following if you want the full history
    all_contours=[]
    all_contours.append(contours)
    contours_only = np.zeros(frame.shape)
    contoured = cv2.cvtColor(finalThresholdImage, cv2.COLOR_GRAY2RGB)


    #getting the center


    #testing the filtered contour vs the unfiltered
    z=frame.copy()
    for x in real_cnts:
        cv2.drawContours(z, x, 0, (0, 255, 0), thickness=10)
    #cv2.imshow("mini",z)


    #for c in all_contours:
        #hull = cv2.convexHull(c)
        #cv2.drawContours(contoured, c, 0, (0, 0, 255), thickness=cv2.FILLED)
        #cv2.drawContours(contours_only, c, 0, (0, 255, 0), thickness=cv2.FILLED)
        #cv2.drawContours(frame,c, 0, (0, 0, 255), thickness=cv2.FILLED)

    ''' --------------------/ Trajectory /------------------ '''

    ''' The ball will be lagging the actual ball but that's fixable because the point we are drawing 
     is the center of the contour, while the point we are drawing is the first point of the contour
     '''
    #the ball is detected
    if len(contours)>0:

        #get center of current contour (whetehr it's a ball or human)
        center_x,center_y = contours_center(contours[0])
        trajectories.append((center_x,center_y))

        #just passing some frames
        if len(trajectories)>30:

            #draw the current (predicted) position
            cv2.circle(frame, (trajectories[-1][0], trajectories[-1][1]), 10, (255, 0, 0), -1)
            #draw the last correct position
            cv2.circle(frame, (trajectories[-2][0], trajectories[-2][1]), 10, (0, 0, 255), -1)

            #find the distance betweeen them
            dist = find_length( (trajectories[-1][1],trajectories[-1][0]), (trajectories[-2][1],trajectories[-2][0]) )

            #print
            print("the distance is "+str(dist))

            #threshold
            if dist>330:
                trajectories.pop()
            cv2.drawContours(frame,all_contours[0], 0, (0, 0, 255), thickness=cv2.FILLED)

    #ball_only = cv2.bitwise_and(frame, contours_only)
    # Window Showing

    #cv2.imshow('Difference Image', differenceImage)
    #cv2.imshow('Threshold Image', thresholdImage)
    #cv2.imshow('Final Threshold Image', finalThresholdImage)
    #cv2.imshow('Contour only', contours_only)
    #cv2.imshow('Contours', contoured)
    cv2.imshow('Contour Detected on original', frame)
    #cv2.imshow('Contours only', contours_only )
    previous = grayImage.copy()

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('h'):
        h_lower = int(input("Enter Lower Hue's Value \n"))
        h_higher = int(input("Enter Upper Hue's Value \n"))
    elif k == ord('v'):
        v_lower = int(input("Enter Lower Value's Value \n"))
        v_higher = int(input("Enter Lower Value's Value \n"))
    elif k == ord('s'):
        s_lower = int(input("Enter Lower Saturation's Value \n"))
        s_higher = int(input("Enter Lower Saturation's Value \n"))
    elif k == ord('p'):
        x = input()

cap.release()
cv2.destroyAllWindows()
