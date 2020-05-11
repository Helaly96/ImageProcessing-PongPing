import cv2
import numpy as np
import math


def find_length(diff_x, diff_y):
    return math.sqrt(diff_y ** 2 + diff_x ** 2)

#helper function to let the user choose the are of interest
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

#apply color mask to the incoming frame to detect the stadium
def Stadium_segment(image):
    lower_stadium = np.array([99, 40, 30], dtype=np.uint8)
    upper_stadium = np.array([120, 255, 255], dtype=np.uint8)
    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(image, lower_stadium, upper_stadium)
    # Bitwise-AND mask and original image
    mask = cv2.bitwise_and(frame, frame, mask=mask)

    return mask

#helper function that draws circle on a selected point
def draw_circles_of_points(c, image_to_be_displayed):
    for point in c:
        x, y = point.ravel()
        cv2.circle(image_to_be_displayed, (x, y), 8, (255, 255, 255), -1)
    return image_to_be_displayed

#TODO to be completed
#approximates the curve c to a 
def approx_to_points(c):
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    return approx

#return the vertices of the bounding boxes of a contour -half of the stadium- and draw a number for each one of them on the image
def Bounding_Box_Of_Stadium(c, image_to_be_displayed):
    points = []

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2

    approximated_cnt = approx_to_points(c)

    for i, p in enumerate(approximated_cnt):
        x, y = p.ravel()
        points.append((x, y))
        cv2.putText(image_to_be_displayed, str(i),
                    (x, y),
                    font,
                    fontScale,
                    fontColor,
                    lineType
                    )
        cv2.circle(image_to_be_displayed, (x, y), 8, (255, 255, 255), -1)

    return points, image_to_be_displayed


def cvt_hsv(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return image

#helper function to detect the color of a selected point on the image
def color_pick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print("Value of clicked position is")
        print(frame[y, x])


def sorting_factor(x):
    return x[2]

#find the top vertices of the net
def get_net(pts1, pts2):
    min_dist = 100000

    good_pair = []
    current_best = 0
    distances = []

    for p1 in pts1:
        for p2 in pts2:
            diff_x = abs(p1[0] - p2[0])
            diff_y = abs(p1[1] - p2[1])
            dist = find_length(diff_x, diff_y)
            if dist < min_dist:
                current_best = p2
                min_dist = dist

        good_pair.append((p1, current_best, min_dist))
        min_dist = 100000

    good_pair = sorted(good_pair, key=sorting_factor, reverse=False)[:2]
    print(good_pair)
    return good_pair


# to hold image of rect
points = []

cropping = False

# current mouse position
current_pos = (0, 0)
end_drawing = False

# define a window
cv2.namedWindow('Original_First_Frame')
# the window the mouse events binded to that windows
cv2.setMouseCallback('Original_First_Frame', Crop_Image)

# read from video
cap = cv2.VideoCapture('Edmonton.mp4')

# read it
clone = cv2.imread("Stadium_Picture.jpg")
# keep showing the image, so we can select the area of interest by drawing a rectangle on it.
while 1:
    frame = clone.copy()
    if cropping and current_pos != (0, 0):
        cv2.rectangle(frame, points[0], current_pos, (255, 0, 0), 2)
    k = cv2.waitKey(20) & 0xFF
    if end_drawing:
        break
    cv2.imshow('Original_First_Frame', frame)

# destroy the first frame
cv2.destroyAllWindows()

saved_frame = [] #array contains the frames that we'll extract the stadium contours from
no_of_frames_to_be_considered = 700 #number of frames to append in previous array

# Capture the first selected_no frames
while 1:
    ret, frame = cap.read()
    frame = cvt_hsv(frame) #convert the frame to hsv
    frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]] #selects the area of interest from the frame
    mask = Stadium_segment(frame) #apply the color mask to detect the stadium
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) #use morphological closing to decrease the noise
    if len(saved_frame) < no_of_frames_to_be_considered:
        saved_frame.append(mask) #append the frame after applying the mask and morph close to the saved_frames list 
    else:
        break

current_area = [] #array holds the total area of contours in each frame of saved_frames
displayed_frame = [] #array holds the frame after drawing the contours of the stadium

#loop through the saved frames and selects the best contours for the stadium from them
for i in range(len(saved_frame)):
    image_to_be_displayed = cv2.cvtColor(saved_frame[i], cv2.COLOR_HSV2BGR)
    Grayed = cv2.cvtColor(image_to_be_displayed, cv2.COLOR_BGR2GRAY)
    ret, result = cv2.threshold(Grayed, 100, 255, cv2.THRESH_BINARY)
    #find the contours in the frame
    contours, _ = cv2.findContours(result,
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #sort the contours by their area descendingly
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]

    Right_Half = cv2.convexHull(contours[0]) #right half of the stadium contour
    Left_Half = cv2.convexHull(contours[1]) #left half of the stadium contour

    #draw contours on he image
    cv2.drawContours(image_to_be_displayed, [Right_Half], -1, (255, 255, 255), 3)
    cv2.drawContours(image_to_be_displayed, [Left_Half], -1, (255, 0, 0), 3)

    #get the coordinates of the vertices of the bounding box
    pts, image_to_be_displayed = Bounding_Box_Of_Stadium(Right_Half, image_to_be_displayed)
    pts, image_to_be_displayed = Bounding_Box_Of_Stadium(Left_Half, image_to_be_displayed)

    #append the frame after drawing the box and corners numbers on it
    displayed_frame.append(image_to_be_displayed)

    #calculate and append the area of the bounding box in the current frame
    Area = 0
    for j in range(len(contours)):
        Area += cv2.contourArea(contours[j])
    current_area.append(Area)
    cv2.imshow("X", image_to_be_displayed)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('k'):
        break

current_area = np.array(current_area)
index = np.argmax(current_area) #find the index of the frame which has the best bounding box
cv2.imshow("X", saved_frame[index])

#these steps are to select the corner points from the frame with the most accurate contours
image_to_be_displayed = cv2.cvtColor(saved_frame[index], cv2.COLOR_HSV2BGR)
Grayed = cv2.cvtColor(image_to_be_displayed, cv2.COLOR_BGR2GRAY)
ret, result = cv2.threshold(Grayed, 100, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]
Right_Half = cv2.convexHull(contours[0])
Left_Half = cv2.convexHull(contours[1])

pts1, image_to_be_displayed = Bounding_Box_Of_Stadium(Right_Half, image_to_be_displayed)
pts2, image_to_be_displayed = Bounding_Box_Of_Stadium(Left_Half, image_to_be_displayed)

print(pts1)
print(pts2)
#pass the corner points of the two halves of the stadium to get_net function to detect the corners of the net
nets = get_net(pts1, pts2)

frame_good = displayed_frame[index]
#draw circles on the corners of the net
for pair in nets:
    point1, point2, _ = pair
    cv2.circle(frame_good, point1, 10, (0, 0, 255), -1)
    cv2.circle(frame_good, point2, 10, (0, 0, 255), -1)

cv2.imshow("Frame with maximum area with contours drawn", displayed_frame[index])
cv2.imshow("Net", frame_good)
cv2.waitKey(0)
