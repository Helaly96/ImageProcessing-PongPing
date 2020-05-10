import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Algorithm.match import Match
import configparser
import cv2
from ini_api import API
import BallTrack

result = dict()


def close_program():
    sys.exit()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('pongping.ui', self)

        self.uploadbutton.clicked.connect(self.upload_video)
        self.opencamerabutton.clicked.connect(self.open_camera)
        self.restartbutton.clicked.connect(self.restart)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.actionQuit.triggered.connect(close_program)

        self.uploadbutton.setEnabled(True)
        self.opencamerabutton.setEnabled(False)
        self.show()

    def update_table(self, res):
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(res[0]))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(res[1]))


    def upload_video(self):
        filename = QFileDialog.getOpenFileName(None, 'Open File', os.getenv('HOME'))
        if filename[0]:
            print(filename[0])
            self.run(filename[0])

    def open_camera(self):
        pass

    def on_combobox_changed(self, value):
        if value == 1:
            self.uploadbutton.setEnabled(False)
            self.opencamerabutton.setEnabled(True)
        else:
            self.uploadbutton.setEnabled(True)
            self.opencamerabutton.setEnabled(False)

    def restart(self):
        clear_list = ["", "", "", ""]
        self.update_table(clear_list)

    def run(self, path):
        #Create API Object
        api = API()
        #Capture the video from the path
        cap = cv2.VideoCapture(path)
        _, frame = cap.read()

        #Get crop points from ini 
        points = api.get_crop_points()  

        # Crop the frame
        frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]

        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        previous = grayImage.copy()


        # holds a record of previous ball positions
        trajectories = []

        #Read the ini for the table and net boundaries 
        boundaryFirstPlayer, boundarySecondPlayer, boundaryNet = api.get_stadium_points()
        
        axisTranslation = [(points[0][1], points[0][0]), (points[0][1], points[0][0]), (points[0][1], points[0][0]), (points[0][1], points[0][0])]

        boundaryFirstPlayer = [ (a[0]- b[0], a[1] - b[1]) for a, b in zip(boundaryFirstPlayer, axisTranslation) ]
        boundarySecondPlayer = [ (a[0]- b[0], a[1] - b[1]) for a, b in zip(boundarySecondPlayer, axisTranslation) ]
        boundaryNet = [ (a[0]- b[0], a[1] - b[1]) for a, b in zip(boundaryNet, axisTranslation) ]
        
        # Construct the match
        m = Match()
        m.defineTable(boundaryFirstPlayer, boundarySecondPlayer, boundaryNet)
        m.startMatch()

        while True:
            # Read frame if end of file is reached break
            _, frame = cap.read()
            
            if frame is None:
                break

            #Call Ball Track pass (the frame cropped?, previous, trajectories, differnces) recieve ballCoord
            ballCoord = BallTrack.get_ball_coordinates(frame, previous, trajectories, points)
            if ballCoord == None:
                continue
            m.updateGame(ballCoord)
            

            #Draw Trajectory
            if len(trajectories) > 5:
                cv2.line(frame, trajectories[-1], trajectories[-2], (0, 0, 255), 5)
                cv2.line(frame, trajectories[-2], trajectories[-3], (0, 255, 0), 5)
            
            #Draw The Stadium

            #UpdateScore
            res = [(m.players[0]).getScore(), (m.players[1]).getScore()]
            self.update_table(res)

            #Show the frame
            cv2.imshow('Match', frame)

            #Wait Key
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        
        #Message End of Match
        cap.release()
        cv2.destroyAllWindows()





app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()



