from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import  numpy as np
IMAGE_WIDTH=800
IMAGE_HEIGHT=600
WAITING_TIME_BETWEEN_FRAMES_IN_MS=30


def nothing(x):
    pass





class Ui_MainWindow(object):

    h_lower = 0
    h_higher = 180

    s_lower = 0
    s_higher = 255

    v_lower = 120
    v_higher = 255

    def Ball_Segmentation(self,frame):
        fgbg = cv2.createBackgroundSubtractorMOG2()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_white = np.array([self.h_lower, self.s_lower, self.v_lower], dtype=np.uint8)
        upper_white = np.array([self.h_higher, self.s_higher, self.v_higher], dtype=np.uint8)
        # Opening Process
        structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # Threshold the HSV image to get only white colors
        mask = cv2.inRange(frame, lower_white, upper_white)

        # Bitwise-AND mask and original image
        frame2 = cv2.bitwise_and(frame, frame, mask=mask)

        # apply motion tracking
        fgbg.setDetectShadows(False)
        fgbg.setVarMin(500)
        fgbg.setVarMax(2500)
        fgmask = fgbg.apply(frame2)
        openedFrame = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, structuringElement)
        xframe = cv2.bitwise_and(frame2,frame2,mask=openedFrame)
        xframe=cv2.cvtColor(xframe,cv2.COLOR_HSV2RGB)
        return xframe



    def setupUi(self, MainWindow):
        #Name Of the Window and size
        MainWindow.setObjectName("PythonGUI")
        MainWindow.resize(1024, 768)
        #Centeral widget where all the actions takes place
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #video stream
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, IMAGE_WIDTH, IMAGE_HEIGHT))
        self.label.setText("")
        self.label.setObjectName("label")

        #Start/Pause
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 700, 75, 23))
        self.pushButton.setObjectName("pushButton")


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.play)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))


    def play(self):

        # create trackbars for color change


        cv2.namedWindow('image')

        cv2.createTrackbar('H_min', 'image', 0, 255, nothing)
        cv2.createTrackbar('S_min', 'image', 0, 255, nothing)
        cv2.createTrackbar('V_min', 'image', 0, 255, nothing)

        cv2.createTrackbar('H_max', 'image', 0, 255, nothing)
        cv2.createTrackbar('S_max', 'image', 0, 255, nothing)
        cv2.createTrackbar('V_max', 'image', 0, 255, nothing)

        cv2.setTrackbarPos("H_min","image",self.h_lower)
        cv2.setTrackbarPos("S_min", "image", self.s_lower)
        cv2.setTrackbarPos("V_min", "image", self.v_lower)

        cv2.setTrackbarPos("H_max", "image", self.h_higher)
        cv2.setTrackbarPos("S_max", "image", self.s_higher)
        cv2.setTrackbarPos("V_max", "image", self.v_higher)


        # create switch for ON/OFF functionality

        x = np.zeros((300, 512, 3), np.uint8)




        cap = cv2.VideoCapture('../Testing-pingpong.mp4')
        while True:


            self.h_lower = cv2.getTrackbarPos('H_min', 'image')
            self.s_lower = cv2.getTrackbarPos('S_min', 'image')
            self.v_lower = cv2.getTrackbarPos('V_min', 'image')

            self.h_higher = cv2.getTrackbarPos('H_max', 'image')
            self.s_higher = cv2.getTrackbarPos('S_max', 'image')
            self.v_higher = cv2.getTrackbarPos('V_max', 'image')


            ret, show = cap.read()
            key = cv2.waitKey(WAITING_TIME_BETWEEN_FRAMES_IN_MS) & 0xFF

            if ret:
                img=self.Ball_Segmentation(show)
                #img = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)

                image = QImage(img.data, show.shape[1], show.shape[0], show.strides[0], QImage.Format_RGB888)
                l = self.label.setPixmap(QPixmap.fromImage(image).scaled(IMAGE_WIDTH, IMAGE_HEIGHT, Qt.KeepAspectRatio))
            if key == ord('p'):
                cv2.waitKey(0)

            elif key == ord('q'):
                break



class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())