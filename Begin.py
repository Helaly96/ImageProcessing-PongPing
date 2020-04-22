import numpy as np
import cv2

#to hold image of rect
points=[]

cropping = False

#current mouse position
current_pos=(0,0)
end_drawing=False

eye_dropper_bool=False
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

circles_to_be_drawn=[]

def eye_dropper(event,x,y,flags,param):
    global eye_dropper
    if event == cv2.EVENT_LBUTTONDOWN:
        circles_to_be_drawn.append((x,y))
        print("Value of clicked position is")
        print(frame[x,y])
        eye_dropper_bool = False

def Optical_flow(frame):
    return 1

#define a window
cv2.namedWindow('Original_First_Frame')
#the window the mouse events binded to that windows
cv2.setMouseCallback('Original_First_Frame',Crop_Image)

#read from video
cap = cv2.VideoCapture('Testing-pingpong.mp4')

#moving subtract Filter
fgbg = cv2.createBackgroundSubtractorMOG2()
KNN = cv2.createBackgroundSubtractorKNN()

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



#read from video
cap = cv2.VideoCapture('Testing-pingpong.mp4')

h_lower=100
h_higher=180

s_lower=0
s_higher=100

v_lower=120
v_higher=255

#define a window
cv2.namedWindow('Original_HSV')
#the window the mouse events binded to that windows
cv2.setMouseCallback('Original_HSV',eye_dropper)



#while loop to go through the video obviously
while(1):
    #read video frame
        ret, frame = cap.read()
        
        #crop the selected frame
        yframe = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]

        #rpg to hsv wow
        yframe = cv2.cvtColor(yframe, cv2.COLOR_BGR2HSV)

        for i in range(len(circles_to_be_drawn)):
            cv2.circle(frame,circles_to_be_drawn[i],10,(255,0,0),-1)


        #TODO
        #Segmenation Ball
        #white thresholds
        #lower_white = np.array([h_lower,s_lower,v_lower], dtype=np.uint8)
        #upper_white = np.array([h_higher,s_higher,v_higher], dtype=np.uint8)

        #Opening Process
        #structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        # Threshold the HSV image to get only white colors
        #mask = cv2.inRange(yframe, lower_white, upper_white)

        # Bitwise-AND mask and original image
        #xframe = cv2.bitwise_and(yframe,yframe, mask= mask)

        #apply motion tracking
        fgbg.setDetectShadows(False)
        fgbg.setVarMin(500)
        fgbg.setVarMax(2500)
        fgmask = fgbg.apply(yframe)

        #opened Frame
        #openedFrame = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, structuringElement)

        #TODO
        #needs better HSV values for white
        #cv2.imshow('Result of white masking!',mask)

        #Result of HSV + Motion Detection + MOG2
        #cv2.imshow('Result_of_HSV_Motion_Detection MOG2',fgmask)

        #original_HSV
        #cv2.imshow("Original_HSV",frame)

        #opened Frame
        xframe = cv2.cvtColor(cv2.bitwise_and(yframe,yframe, mask= fgmask),cv2.COLOR_HSV2BGR)
        cv2.imshow("Opened",xframe)


         



        k = cv2.waitKey(50) & 0xff
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