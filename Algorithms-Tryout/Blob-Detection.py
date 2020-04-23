import numpy as np
import cv2

# to hold image of rect
points = []

cropping = False

# current mouse position
current_pos = (0, 0)
end_drawing = False

eye_dropper_bool = False

def BlobDetectorInit():
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    #params.filterByColor=True
    #params.filterByColor=(255,255,255)
    # Change thresholds
    params.minThreshold = 70;
    params.maxThreshold = 200;

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 0
    params.maxArea = 200

    # Filter by Circularity
    #params.filterByCircularity = True
    params.minCircularity = 0.4

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.4

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.5

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3:
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)
    return  detector

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


circles_to_be_drawn = []


def eye_dropper(event, x, y, flags, param):
    global eye_dropper
    if event == cv2.EVENT_LBUTTONDOWN:
        circles_to_be_drawn.append((x, y))
        print("Value of clicked position is")
        print(frame[x, y])
        eye_dropper_bool = False


def Optical_flow(frame):
    return 1


# define a window
cv2.namedWindow('Original_First_Frame')
# the window the mouse events binded to that windows
cv2.setMouseCallback('Original_First_Frame', Crop_Image)

# read from video
cap = cv2.VideoCapture('../Testing-pingpong.mp4')

# moving subtract Filter
fgbg = cv2.createBackgroundSubtractorMOG2()
KNN = cv2.createBackgroundSubtractorKNN()

# read first frame of video
ret, frame = cap.read()

# write the first frame
cv2.imwrite("x.jpg", frame)

# read it
clone = cv2.imread("x.jpg")

# keep showing the image, so we can draw on it hehe.
while (1):
    frame = clone.copy()
    if (cropping and current_pos != (0, 0)):
        cv2.rectangle(frame, points[0], current_pos, (255, 0, 0), 2)
    k = cv2.waitKey(20) & 0xFF
    if end_drawing:
        break
    cv2.imshow('Original_First_Frame', frame)

# destroy the first frame
cv2.destroyAllWindows()
cap.release()

# read from video
cap = cv2.VideoCapture('../Testing-pingpong.mp4')

h_lower = 80
h_higher = 124

s_lower = 0
s_higher = 120

v_lower = 0
v_higher = 255

# define a window
cv2.namedWindow('Original_HSV')
# the window the mouse events binded to that windows
cv2.setMouseCallback('Original_HSV', eye_dropper)

# while loop to go through the video obviously
while (1):
    # read video frame
    ret, frame = cap.read()

    # crop the selected frame
    yframe = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]

    # rpg to hsv wow
    yframe = cv2.cvtColor(yframe, cv2.COLOR_BGR2HSV)

    for i in range(len(circles_to_be_drawn)):
        cv2.circle(frame, circles_to_be_drawn[i], 10, (255, 0, 0), -1)

    # TODO
    # Segmenation Ball
    # white thresholds
    lower_white = np.array([h_lower,s_lower,v_lower], dtype=np.uint8)
    upper_white = np.array([h_higher,s_higher,v_higher], dtype=np.uint8)

    # Opening Process
    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(yframe, lower_white, upper_white)

    # Bitwise-AND mask and original image
    xframe = cv2.bitwise_and(yframe,yframe, mask= mask)


    white_filtered=xframe

    cv2.imshow("SS",white_filtered)
    # apply motion tracking
    fgbg.setDetectShadows(False)
    fgbg.setVarMin(40)
    fgbg.setVarMax(5000)
    fgmask = fgbg.apply(xframe)

    # opened Frame
    openedFrame = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, structuringElement)


    # TODO
    # needs better HSV values for white
    # cv2.imshow('Result of white masking!',mask)

    # Result of HSV + Motion Detection + MOG2
    # cv2.imshow('Result_of_HSV_Motion_Detection MOG2',fgmask)

    # original_HSV
    # cv2.imshow("Original_HSV",frame)

    # rpg to hsv wow
    yframe = cv2.cvtColor(yframe, cv2.COLOR_HSV2BGR)
    # opened Frame
    xframe = cv2.bitwise_and(yframe, yframe, mask=openedFrame)

    detector = BlobDetectorInit()

    #xframe = cv2.dilate(xframe, (20, 20))
    xframe= cv2.cvtColor(xframe, cv2.COLOR_BGR2GRAY)

    xframe = cv2.medianBlur(xframe,5)

    key_points = detector.detect((xframe))

    ret, thresh = cv2.threshold(xframe, 50, 255, 0)


    w,h,_ = yframe.shape

    result = np.zeros((w, h, 1), np.uint8)
    result2 = np.zeros((w, h, 1), np.uint8)

    #cv2.imshow("S", thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    real_cnts=[]

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, .03 * cv2.arcLength(cnt, True), True)
        perimeter = cv2.arcLength(cnt, True)
        if(len(approx)>4 and perimeter>10):
            k = cv2.isContourConvex(approx)
            if(k):
                real_cnts.append((cnt))

    #contours = sorted(contours, key=cv2.contourArea, reverse=True)[0:2]
    cv2.drawContours(result, real_cnts, -1, (255, 255, 0), 3)

    if(len(real_cnts)>0):
        circles = cv2.HoughCircles(xframe, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=50, param2=30, minRadius=0)
        if(circles is not None):
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(result2, (i[0], i[1]), i[2], (255, 255, 255), 2)
                # draw the center of the circle
                cv2.circle(result2, (i[0], i[1]), 2, (255, 255, 255), 3)

    cv2.imshow("Opened", xframe)
    cv2.imshow("Opened2", result)
    cv2.imshow("Opened3", result2)
    #im_with_keypoints = cv2.drawKeypoints(xframe, key_points, np.array([]), (255, 255 , 0),
                                          #cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    k = cv2.waitKey(70) & 0xff
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