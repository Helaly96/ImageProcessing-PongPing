import os
import sys
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Algorithm.match import Match
import configparser
import cv2
from ini_api import API
import BallTrack
import numpy as np

IMAGE_WIDTH = 1230
IMAGE_HEIGHT = 390
WAITING_TIME_BETWEEN_FRAMES_IN_MS=30


def close_program():
    sys.exit()


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        self.timer_count = 0
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
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(res[0])))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(res[1])))

    def append_event(self, value):
        rowcount = self.tableWidget_2.rowCount()
        if value:
            self.tableWidget_2.insertRow(rowcount)
            self.tableWidget_2.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(value))
            self.tableWidget_2.setItem(rowcount, 1, QtWidgets.QTableWidgetItem(
                str(int(self.timer_count / WAITING_TIME_BETWEEN_FRAMES_IN_MS))))

    def upload_video(self):
        self.restart()
        filename = QFileDialog.getOpenFileName(None, 'Open File', os.getenv('HOME'))
        if filename[0]:
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
        self.tableWidget_2.setRowCount(0)

    def run(self, path):
        self.timer_count = 0

        # Create API Object
        api = API()
        # Capture the video from the path
        cap = cv2.VideoCapture(path)
        _, frame = cap.read()

        # Get crop points from ini
        points = api.get_crop_points()

        # Crop the frame
        frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]

        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        previous = grayImage.copy()

        # holds a record of previous ball positions
        trajectories = []

        # Read the ini for the table and net boundaries
        boundaryFirstPlayer, boundarySecondPlayer, boundaryNet = api.get_stadium_points()

        axisTranslation = [(points[0][1], points[0][0]), (points[0][1], points[0][0]), (points[0][1], points[0][0]),
                           (points[0][1], points[0][0])]

        boundaryFirstPlayer = [(a[0] - b[0], a[1] - b[1]) for a, b in zip(boundaryFirstPlayer, axisTranslation)]
        boundarySecondPlayer = [(a[0] - b[0], a[1] - b[1]) for a, b in zip(boundarySecondPlayer, axisTranslation)]
        boundaryNet = [(a[0] - b[0], a[1] - b[1]) for a, b in zip(boundaryNet, axisTranslation)]
        
        # Construct the match
        m = Match()
        m.defineTable(boundaryFirstPlayer, boundarySecondPlayer, boundaryNet)
        m.startMatch()

        while True:
            self.timer_count += 1
            # Read frame if end of file is reached break
            _, frame = cap.read()

            if frame is None:
                break

            # Crop frame
            frame = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]

            # Call Ball Track pass (the frame cropped, previous cropped, trajectories, points) recieve ballCoord
            ballCoord, previous = BallTrack.get_ball_coordinates(frame, previous, trajectories, points)

            if ballCoord is not None:
                m.updateGame(ballCoord)

            # Draw Trajectory
            if len(trajectories) > 5:
                cv2.line(frame, trajectories[-1], trajectories[-2], (0, 0, 255), 5)
                cv2.line(frame, trajectories[-2], trajectories[-3], (0, 255, 0), 5)

            # Draw The Stadium
            Contour = np.array(boundaryFirstPlayer)
            cv2.drawContours(frame, [Contour], 0, (0,255,255), 2)
            Contour = np.array(boundarySecondPlayer)
            cv2.drawContours(frame, [Contour], 0, (0,255,255), 2)
            Contour = np.array(boundaryNet)
            cv2.drawContours(frame, [Contour], 0, (255,255,255), 2)

            # UpdateScore
            res = [(m.players[0]).getScore(), (m.players[1]).getScore()]

            self.update_table(res)
            self.append_event(m.printInfo())

            # Show the frame
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)

            self.label_4.setPixmap(QPixmap.fromImage(qImg).scaled(IMAGE_WIDTH, IMAGE_HEIGHT, Qt.KeepAspectRatio))
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            QApplication.processEvents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
