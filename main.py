import sys
import cv2
import random
import numpy as np
import torch
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from urllib.request import urlopen

# Module
from initializeUI import *
from displayVideo import *

class App(QMainWindow) :
    def __init__(self) :
        super().__init__()

        # info
        self.title = "DADUINO AI CAR"
        self.ip = "192.168.137.73"
        self.stream = urlopen("http://" + self.ip + ":81/stream")
        self.buffer = b''
        self.url = "http://" + self.ip + "/action?go="
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.is_haar = False
        self.is_linetracing = False

        # timer
        self.timer = QTimer(self)
        self.timer.setInterval(1)
        self.timer.timeout.connect(lambda : displayVideo(self))
        self.timer.start()

        # Haar, LineTracing
        self.btn_haar = QPushButton("Haar", self)
        self.btn_linetracing = QPushButton("LineTracing", self)

        # yolo
        self.model = torch.hub.load("ultralytics/yolov5", "custom", path = "./best.pt")

        initializeUI(self)

    # Haar Face
    def haar(self) :
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 2)
        
        for (x, y, w, h) in faces:
            b, g, r = random.sample(range(256), 3)
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (b, g, r), 2)
            cv2.putText(self.img, "Face", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (b, g, r), 2)

    # (PyQt) Haar Face ON/OFF
    def toggle_haar(self) :
        if self.is_haar :
            self.is_haar = False
        else :
            self.is_haar = True

    # LineTracing
    def lineTracing(self) :
        height, width, _ = self.img.shape
        self.img = self.img[height // 4:, :]
        
        lower_bound = np.array([0, 0, 0])
        upper_bound = np.array([255, 255, 80])
        mask = cv2.inRange(self.img, lower_bound, upper_bound)

        M = cv2.moments(mask)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        center_offset = width // 2 - cX

        cv2.circle(self.img, (cX, cY), 10, (0, 255, 0), -1)

        if center_offset > 10 :
            self.yoloMove("right")
        elif center_offset < -10 :
            self.yoloMove("left")
        else :
            urlopen(self.url + "forward")

    # YOLO Move
    def yoloMove(self, move) :
        results = self.model(self.img)
        detections = results.pandas().xyxy[0]
        
        if not detections.empty :
            for _, detection in detections.iterrows() :
                x1, y1, x2, y2 = detection[["xmin", "ymin", "xmax", "ymax"]].astype(int).values
                self.yolo_label = detection["name"]
                self.yolo_conf = detection["confidence"]

                if "slow" in self.yolo_label and self.yolo_conf > 0.5 :
                    urlopen(self.url + "stop")
                elif "speed50" in self.yolo_label and self.yolo_conf > 0.5 :
                    urlopen(self.url + move)

                yolo_color = [int(c) for c in random.choices(range(256), k=3)]
                cv2.rectangle(self.img, (x1, y1), (x2, y2), yolo_color, 2)
                cv2.putText(self.img, f"{self.yolo_label} {self.yolo_conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, yolo_color, 2)
        else :
            urlopen(self.url + move)

    # (PyQt) LineTracing ON/OFF
    def toggle_lineTracing(self) :
        if self.is_linetracing :
            self.is_linetracing = False
            urlopen(self.url + "stop")
        else :
            self.is_linetracing = True

    # Keyboard Press
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_R:
            self.stop()
        elif key == Qt.Key_W:
            self.forward()
        elif key == Qt.Key_S:
            self.backward()
        elif key == Qt.Key_A:
            self.left()
        elif key == Qt.Key_D:
            self.right()
        elif key == Qt.Key_Q:
            self.turn_left()
        elif key == Qt.Key_E:
            self.turn_right()
        elif key == Qt.Key_1:
            self.speed40()
        elif key == Qt.Key_2:
            self.speed50()
        elif key == Qt.Key_3:
            self.speed60()
        elif key == Qt.Key_4:
            self.speed80()
        elif key == Qt.Key_5:
            self.speed100()

        # (Keyboard) Haar Face ON/OFF
        if key == Qt.Key_H :
            if self.is_haar :
                self.is_haar = False
            else :
                self.is_haar = True
        
        # (Keyboard) LineTracing ON/OFF
        if key == Qt.Key_L :
            if self.is_linetracing :
                self.is_linetracing = False
                urlopen(self.url + "stop")
            else :
                self.is_linetracing = True

    # Keyboard Release
    def keyReleaseEvent(self, event):
        self.stop()

    # Speed Function
    def speed40(self) :
        urlopen(self.url + "speed40")
    
    def speed50(self) :
        urlopen(self.url + "speed50")
    
    def speed60(self) :
        urlopen(self.url + "speed60")
    
    def speed80(self) :
        urlopen(self.url + "speed80")
    
    def speed100(self) :
        urlopen(self.url + "speed100")

    # Move Function
    def forward(self) :
        urlopen(self.url + "forward")
    
    def backward(self) :
        urlopen(self.url + "backward")

    def turn_left(self) :
        urlopen(self.url + "turn_left")

    def turn_right(self) :
        urlopen(self.url + "turn_right")
        
    def left(self) :
        urlopen(self.url + "left")

    def right(self) :
        urlopen(self.url + "right")

    def stop(self) :
        urlopen(self.url + "stop")

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    view = App()
    view.show()
    sys.exit(app.exec_())
