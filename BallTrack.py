import numpy as np
import cv2
import math
from Algorithm.match import Match
from operator import sub, add, floordiv
from time import sleep

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


def find_length(diff_x, diff_y):
    return math.sqrt(diff_y ** 2 + diff_x ** 2)


# Color Filtering Function
def contours_center(c):
    if c is not None:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    return cX, cY


def colorSegment(frame):
    lower = np.array([80, 0, 0])
    upper = np.array([120, 100, 255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    return res


def find_nearest_contour(point, contours, trajectories):
    min = 100000
    index = 0
    correct_index = 0

    best_fit = ()
    # comparing to each contour point
    for c in contours:
        for p in c:
            x, y = p.ravel()
            diff_x = x - point[0]
            diff_y = y - point[1]
            dist = find_length(diff_x, diff_y)
            if dist < min:
                min = dist
                best_fit = (x, y)
        index += 1

    # print("THE INDEX IS "+str(correct_index)+" :D")

    if len(contours) == 0:
        return -1, -1
    else:
        diff_x = best_fit[0] - point[0]
        diff_y = best_fit[1] - point[1]
        dist = find_length(diff_x, diff_y)
        # print("the distance between the old point and the new approx is:" + str(int(dist)))
        # return best_fit
        # the point we predicted is off
        if dist > 150:
            pass
            # predict
            # last_direction = tuple(map(sub, trajectories[-1], trajectories[-2]))
            # last_direction = tuple(map(floordiv, last_direction, (2, 2)))
            # best_fit = tuple(map(add, point, last_direction))
        return best_fit


'''
#Mouse Box
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
'''
''' --------------------/ Video Processing /------------------ '''
# Points
points = [[0, 0], [0, 0]]
points[0][1] = 321
points[1][1] = 711
points[0][0] = 329
points[1][0] = 1559
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

# holds a record of previous ball positions
trajectories = []

# differences
differences = []
j = 0

'''--------------------Create Match Object-----------------------'''

boundaryFirstPlayer = [(1530 - points[0][1], 670 - points[0][0]), (950 - points[0][1], 675 - points[0][0]),
                       (954 - points[0][1], 620 - points[0][0]), (1310 - points[0][1], 620 - points[0][0])]
boundarySecondPlayer = [(919 - points[0][1], 678 - points[0][0]), (370 - points[0][1], 647 - points[0][0]),
                        (600 - points[0][1], 610 - points[0][0]), (920 - points[0][1], 620 - points[0][0])]
boundaryNet = [(921 - points[0][1], 678 - points[0][0]), (921 - points[0][1], 610 - points[0][0]),
               (954 - points[0][1], 580 - points[0][0]), (947 - points[0][1], 680 - points[0][0])]

pts0 = np.array([[1530, 670], [950, 675], [954, 620], [1310, 620]], np.int32)
pts1 = np.array([[919, 678], [370, 647], [600, 610], [920, 620]], np.int32)
pts2 = np.array([[921, 678], [921, 610], [954, 580], [947, 680]], np.int32)

pts0 = pts0.reshape((-1, 1, 2))
pts1 = pts1.reshape((-1, 1, 2))
pts2 = pts2.reshape((-1, 1, 2))

# Construct the match
m = Match()
m.defineTable(boundaryFirstPlayer, boundarySecondPlayer, boundaryNet)
m.startMatch()

while True:

    _, frame = cap.read()
    if frame is None:
        break

    cv2.polylines(frame, [pts0], True, (255, 255, 255))
    cv2.polylines(frame, [pts1], True, (255, 255, 255))
    cv2.polylines(frame, [pts2], True, (0, 255, 0))
    frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]
    # frame = colorSegment(frame)
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    differenceImage = cv2.absdiff(grayImage, previous)
    blur = cv2.GaussianBlur(differenceImage, (5, 5), cv2.BORDER_DEFAULT)
    _, thresholdImage = cv2.threshold(blur, sensitivityValue1, 255, cv2.THRESH_BINARY)

    # Blurring the Image to get rid of noise
    finalThresholdImage = cv2.GaussianBlur(thresholdImage, blurSize, cv2.BORDER_DEFAULT)
    _, finalThresholdImage = cv2.threshold(finalThresholdImage, sensitivityValue2, 255, cv2.THRESH_BINARY)
    # cv2.imshow("FFF",finalThresholdImage)

    # Opening
    structuringElementSize = (7, 7)
    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, structuringElementSize)
    finalThresholdImage = cv2.morphologyEx(thresholdImage, cv2.MORPH_OPEN, structuringElement)

    finalThresholdImage = cv2.GaussianBlur(finalThresholdImage, (5, 5), cv2.BORDER_DEFAULT)

    # cv2.imshow("Final Thresholded_image", cv2.bitwise_and(frame,frame,mask=finalThresholdImage))
    # Contour Detection
    # Contour Parameters
    perimeterMin = 50
    perimeterMax = 100
    epsilon = 0.03
    numberOfAcceptedContours = 4

    # Blank frame to draw the contour on
    blankFrame = np.zeros(frame.shape)

    # instead of getting a tree of contours (ie, each contour contain a child)
    # contours, hierarchy = cv2.findContours(finalThresholdImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # we can get only top levels contours
    contours, hierarchy = cv2.findContours(finalThresholdImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)[:numberOfAcceptedContours]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    real_cnts = []

    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        if perimeterMin < perimeter < perimeterMax:
            # if cv2.isContourConvex(approx):
            # if cv2.contourArea(cnt) < 300:
            real_cnts.append(cnt)

    # comment the following if you want the full history
    all_contours = [contours]
    contours_only = np.zeros(frame.shape)
    contoured = cv2.cvtColor(finalThresholdImage, cv2.COLOR_GRAY2RGB)

    if len(contours) >= 1:
        cv2.drawContours(frame, contours[0], -1, (0, 255, 255), thickness=5)  # yellow = 1
    if len(contours) >= 2:
        cv2.drawContours(frame, contours[1], -1, (0, 0, 255), thickness=5)     # blue = 2
    if len(contours) >= 3:
        cv2.drawContours(frame, contours[2], -1, (0, 255, 0), thickness=5)     # green = 3
    if len(contours) >= 4:
        cv2.drawContours(frame, contours[3], -1, (255, 0, 0), thickness=5)     # red = 4

    ''' --------------------/ Trajectory /------------------ '''

    ''' The ball will be lagging the actual ball but that's fixable because the point we are drawing 
     is the center of the contour, while the point we are drawing is the first point of the contour
     '''

    # the ball is detected
    if len(real_cnts) > 0:
        # get center of current contour (whetehr it's a ball or human)
        center_x, center_y = contours_center(real_cnts[0])
        trajectories.append((center_x, center_y))
        # just passing some frames
        if len(trajectories) > 15:
            diff_x = trajectories[-1][0] - trajectories[-2][0]
            diff_y = trajectories[-1][1] - trajectories[-2][1]
            # find the distance betweeen them
            dist = find_length(diff_y, diff_x)
            # print("The distance between the ball and the center of new is"+str(int(dist)))
            if dist > 150:
                # the reading we got is not correct
                trajectories.pop()
                # we need to search the remaining contours
                corrected_x, corrected_y = find_nearest_contour(trajectories[-1], contours, trajectories)
                trajectories.append((corrected_x, corrected_y))

            m.updateGame(trajectories[-1])
            cv2.line(frame, trajectories[-1], trajectories[-2], (0, 0, 255), 5)
            cv2.line(frame, trajectories[-2], trajectories[-3], (0, 255, 0), 5)
    else:
        # if there are no contours
        if len(trajectories) > 15:
            last_direction = tuple(map(sub, trajectories[-1], trajectories[-2]))
            last_direction = tuple(map(floordiv, last_direction, (2, 2)))
            best_fit = tuple(map(add, trajectories[-1], last_direction))
            trajectories.append(best_fit)

    cv2.imshow('Contour Detected on original', frame)
    # cv2.imshow('Contours only', contours_only)
    previous = grayImage.copy()

    k = cv2.waitKey(45) & 0xff
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
