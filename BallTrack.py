import numpy as np
import cv2
import math
from Algorithm.match import Match
from operator import sub, add, floordiv
from time import sleep

''' -----------------/ The Bounding Box /--------------------'''

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


def find_nearest_contour(point, contours, trajectories):
    min = 100000
    index = 0
    correct_index = 0

    best_fit = ()
    # comparing to each contour point
    i = 0
    for c in contours:
        for p in c:
            x, y = p.ravel()
            diff_x = x - point[0]
            diff_y = y - point[1]
            dist = find_length(diff_x, diff_y)
            if dist < min:
                i = index
                min = dist
                best_fit = (x, y)
        index += 1

    diff_x = best_fit[0] - point[0]
    diff_y = best_fit[1] - point[1]
    dist = find_length(diff_x, diff_y)
    # print("the distance between the old point and the new approx is:" + str(int(dist)))
    # return best_fit
    # the point we predicted is off
    if dist > 400:
        print("wrong")
        return point, contours[i]
        # predict
        # last_direction = tuple(map(sub, trajectories[-1], trajectories[-2]))
        # last_direction = tuple(map(floordiv, last_direction, (2, 2)))
        # best_fit = tuple(map(add, point, last_direction))
    return best_fit, contours[i]


''' --------------------/ Video Processing /------------------ '''
# Points to crop
points = [[0, 0], [0, 0]]
points[0][1] = 321
points[1][1] = 711
points[0][0] = 329
points[1][0] = 1559

# Parameters for the difference
sensitivityValue = 60
blurSize = (15, 15)

# read from video
cap = cv2.VideoCapture('Edmonton.mp4')
_, frame = cap.read()

# Crop the frame
frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]

grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
previous = grayImage.copy()

# holds a record of previous ball positions
trajectories = []

# differences
differences = []
j = 0

'''--------------------Create Match Object-----------------------'''

# Boundary of the first player's table relative to the cropped image
boundaryFirstPlayer = [(1530 - points[0][1], 670 - points[0][0]), (950 - points[0][1], 675 - points[0][0]),
                       (954 - points[0][1], 620 - points[0][0]), (1310 - points[0][1], 620 - points[0][0])]

# Boundary of the second player's table relative to the cropped image
boundarySecondPlayer = [(919 - points[0][1], 678 - points[0][0]), (370 - points[0][1], 647 - points[0][0]),
                        (600 - points[0][1], 610 - points[0][0]), (920 - points[0][1], 620 - points[0][0])]

# Boundary of the net relative to the cropped image
boundaryNet = [(921 - points[0][1], 678 - points[0][0]), (921 - points[0][1], 610 - points[0][0]),
               (954 - points[0][1], 580 - points[0][0]), (947 - points[0][1], 680 - points[0][0])]


# Points of the table and net
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
    # Read frame
    _, frame = cap.read()
    if frame is None:
        break

    # Draw boundaries
    cv2.polylines(frame, [pts0], True, (255, 255, 255))
    cv2.polylines(frame, [pts1], True, (255, 255, 255))
    cv2.polylines(frame, [pts2], True, (0, 255, 0))

    # Crop frame
    frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]

    # Convert to grayscale
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calcuate the difference between current and last frame
    differenceImage = cv2.subtract(grayImage, previous)

    # Blur the difference to remove noise
    blur = cv2.GaussianBlur(differenceImage, (5, 5), cv2.BORDER_DEFAULT)

    # Threshold the blured frame
    _, thresholdImage = cv2.threshold(
        blur, sensitivityValue1, 255, cv2.THRESH_BINARY)

    # Openning on the frame
    structuringElementSize = (7, 7)
    structuringElement = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, structuringElementSize)
    finalThresholdImage = cv2.morphologyEx(
        thresholdImage, cv2.MORPH_OPEN, structuringElement)

    # Blur the opened frame
    finalThresholdImage = cv2.GaussianBlur(
        finalThresholdImage, (5, 5), cv2.BORDER_DEFAULT)

    # Contour Detection
    # Contour Parameters
    perimeterMin = 25
    perimeterMax = 125
    epsilon = 0.03

    # instead of getting a tree of contours (ie, each contour contain a child)
    # contours, hierarchy = cv2.findContours(finalThresholdImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # we can get only top levels contours
    contours, hierarchy = cv2.findContours(
        finalThresholdImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours with area
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Select contours with specific arc length
    real_cnts = []

    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        if perimeterMin < perimeter < perimeterMax:
            real_cnts.append(cnt)

    contours_only = np.zeros(frame.shape)
    contoured = cv2.cvtColor(finalThresholdImage, cv2.COLOR_GRAY2RGB)

    # Draw first 4 contours with different colors
    if len(contours) >= 1:
        cv2.drawContours(
            contours_only, contours[0], -1, (0, 255, 255), thickness=5)  # yellow = 1
    if len(contours) >= 2:
        cv2.drawContours(
            contours_only, contours[1], -1, (0, 0, 255), thickness=5)     # blue = 2
    if len(contours) >= 3:
        cv2.drawContours(
            contours_only, contours[2], -1, (0, 255, 0), thickness=5)     # green = 3
    if len(contours) >= 4:
        cv2.drawContours(
            contours_only, contours[3], -1, (255, 0, 0), thickness=5)     # red = 4

    ''' --------------------/ Trajectory /------------------ '''

    # The ball is detected
    if len(real_cnts) > 0:
        # Get center of first contour
        center_x, center_y = contours_center(real_cnts[0])

        # Append it to the trajectories
        trajectories.append((center_x, center_y))

        # Skip first 15 frames
        if len(trajectories) > 15:
            # Calculate the distance between current point and last point
            diff_x = trajectories[-1][0] - trajectories[-2][0]
            diff_y = trajectories[-1][1] - trajectories[-2][1]
            dist = find_length(diff_y, diff_x)

            # The current point is very far
            if dist > 60:
                # Remove it from the trajectories
                trajectories.pop()

                # Get the nearest contour
                corrected_point, best_contour = find_nearest_contour(
                    trajectories[-1], real_cnts, trajectories)

                # Append the correct contour to the trajectories
                trajectories.append(corrected_point)

            # Update the game and draw trajectories
            m.updateGame(trajectories[-1])
            cv2.line(frame, trajectories[-1], trajectories[-2], (0, 0, 255), 5)
            cv2.line(frame, trajectories[-2], trajectories[-3], (0, 255, 0), 5)

    # No contours are found in the current frame
    else:
        if len(trajectories) > 15:
            # Get the last direction of the ball
            last_direction = tuple(
                map(sub, trajectories[-1], trajectories[-2]))

            # Add the last direction to the last point to continue in the same direction
            best_fit = tuple(map(add, trajectories[-1], last_direction))

            # Append the new point to the trajectories
            trajectories.append(best_fit)

    # Show the frame with the trajectory on it
    cv2.imshow('Contour Detected on original', frame)
    # cv2.imshow('Contours only', contours_only)
    # cv2.imshow("Final Thresholded_image", cv2.bitwise_and(frame, frame, mask=finalThresholdImage))
    # cv2.imshow('th', differenceImage)
    previous = grayImage.copy()

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
