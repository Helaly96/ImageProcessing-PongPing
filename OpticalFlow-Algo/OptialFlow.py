import cv2
import numpy as np

point = ()
point_selected = False
old_points = np.array([[]])

#call back for the mouse
def select_point_to_track(event,x,y,flags,params):
    global point
    global point_selected
    global old_points
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x,y)
        point_selected = True
        old_points = np.array([[x, y]], dtype=np.float32)


#LK algo params
#windows size that it will look for matching in it 
#max level of pyramids to help in faster movements (#TODO)
#?
#Minimum eigen value of the 2x2 matrix
lk_params = dict(winSize = (20, 20),
                maxLevel = 4,
                criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01),
                minEigThreshold=0.03 )




cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point_to_track)
#video = cv2.VideoCapture("OF.mp4")
video = cv2.VideoCapture("../private-record.mp4")
_,frame = video.read()
old_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)




while True:

    _,frame = video.read()

    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    if point_selected is True:
        #original ball position ( the first click)
        cv2.circle(frame, point, 5, (0, 0, 255), 2)
        
        #ball current position
        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
        old_gray = gray_frame.copy()
        old_points = new_points
        x, y = new_points.ravel()
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)


    cv2.imshow("Frame",frame)
    k = cv2.waitKey(120)
    if k==27:
        break

video.release()
cv2.destroyAllWindows()
