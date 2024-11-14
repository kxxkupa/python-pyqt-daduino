import sys
import cv2
import random
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from urllib.request import urlopen

class App(QMainWindow) :
    def __init__(self) :
        super().__init__()

        # info
        self.title = "DADUINO AI CAR"        
        self.ip = "192.168.137.70"
        self.stream = urlopen("http://" + self.ip + ":81/stream")
        self.buffer = b''
        self.url = "http://" + self.ip + "/action?go="
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.is_haar = False
        self.is_linetracing = False

        # timer
        self.timer = QTimer(self)
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.video)
        self.timer.start()

        # Haar, LineTracing
        self.btn_haar = QPushButton("Haar", self)
        self.btn_linetracing = QPushButton("LineTracing", self)

        # Speed
        self.btn_speed_40 = QPushButton("Speed 40", self)        
        self.btn_speed_50 = QPushButton("Speed 50", self)
        self.btn_speed_60 = QPushButton("Speed 60", self)
        self.btn_speed_80 = QPushButton("Speed 80", self)
        self.btn_speed_100 = QPushButton("Speed 100", self)

        # Move        
        self.btn_stop = QPushButton("Stop", self)
        self.btn_left = QPushButton("Left", self)
        self.btn_right = QPushButton("Right", self)
        self.btn_forward = QPushButton("Forward", self)
        self.btn_backward = QPushButton("Backward", self)
        self.btn_turn_left = QPushButton("Turn Left", self)
        self.btn_turn_right = QPushButton("Turn Right", self)

        # UI
        self.initUI()

    # Aduino Video
    def video(self) :
        self.buffer += self.stream.read(4096)
        self.head = self.buffer.find(b'\xff\xd8')
        self.end = self.buffer.find(b'\xff\xd9')
        
        if self.head > -1 and self.end > -1 :
            jpg = self.buffer[self.head : self.end + 2]
            self.buffer = self.buffer[self.end + 2 :]
            self.img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Haar ON/OFF
            if self.is_haar :
                self.haar()

            # LineTracing ON/OFF
            if self.is_linetracing :
                self.lineTracing()

            h, w, c = self.img.shape
            self.qimg = QImage(self.img.data, w, h, w * c, QImage.Format_BGR888)
            self.label.setPixmap(QPixmap.fromImage(self.qimg))

    # Haar Face
    def haar(self) :
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 2)
        
        for (x, y, w, h) in faces:
            b, g, r = random.sample(range(256), 3)
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (b, g, r), 2)
            cv2.putText(self.img, "Face", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1.5, (b, g, r), 2)

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

        if center_offset > -100 :
            urlopen(self.url + "right")
        elif center_offset < 100 :
            urlopen(self.url + "left")
        else :
            urlopen(self.url + "forward")

    # (PyQt) LineTracing ON/OFF
    def toggle_lineTracing(self) :
        if self.is_linetracing :
            self.is_linetracing = False
            urlopen(self.url + "stop")
        else :
            self.is_linetracing = True

    # UI
    def initUI(self) :        
        self.widget = QWidget()
        self.setWindowTitle(self.title)
        self.setCentralWidget(self.widget)
        self.setFixedSize(600, 700)
        self.label = QLabel()
        self.label.resize(600, 300)
        self.label.setScaledContents(True)
        
        # Pressed
        self.btn_left.pressed.connect(self.left)
        self.btn_right.pressed.connect(self.right)
        self.btn_forward.pressed.connect(self.forward)
        self.btn_backward.pressed.connect(self.backward)
        self.btn_turn_left.pressed.connect(self.turn_left)
        self.btn_turn_right.pressed.connect(self.turn_right)

        # Released
        self.btn_left.released.connect(self.stop)
        self.btn_right.released.connect(self.stop)
        self.btn_forward.released.connect(self.stop)
        self.btn_backward.released.connect(self.stop)
        self.btn_turn_left.released.connect(self.stop)
        self.btn_turn_right.released.connect(self.stop)

        # Clicked
        self.btn_speed_40.clicked.connect(self.speed40)
        self.btn_speed_50.clicked.connect(self.speed50)
        self.btn_speed_60.clicked.connect(self.speed60)
        self.btn_speed_80.clicked.connect(self.speed80)
        self.btn_speed_100.clicked.connect(self.speed100)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_haar.clicked.connect(self.toggle_haar)
        self.btn_linetracing.clicked.connect(self.toggle_lineTracing)
        
        # Layout
        video_box = QHBoxLayout()
        video_box.addWidget(self.label)

        hbox_01 = QHBoxLayout()
        hbox_01.addWidget(self.btn_haar)
        hbox_01.addWidget(self.btn_linetracing)

        hbox_02 = QHBoxLayout()
        hbox_02.addWidget(self.btn_speed_40)
        hbox_02.addWidget(self.btn_speed_50)
        hbox_02.addWidget(self.btn_speed_60)
        hbox_02.addWidget(self.btn_speed_80)
        hbox_02.addWidget(self.btn_speed_100)

        hbox_03 = QHBoxLayout()
        hbox_03.addWidget(self.btn_stop)
        hbox_03.addWidget(self.btn_forward)
        hbox_03.addWidget(self.btn_backward)

        hbox_04 = QHBoxLayout()
        hbox_04.addWidget(self.btn_turn_left)
        hbox_04.addWidget(self.btn_turn_right)

        hbox_05 = QHBoxLayout()
        hbox_05.addWidget(self.btn_left)
        hbox_05.addWidget(self.btn_right)        

        vbox = QVBoxLayout()
        vbox.addLayout(video_box)
        vbox.addLayout(hbox_01)
        vbox.addLayout(hbox_02)
        vbox.addLayout(hbox_03)
        vbox.addLayout(hbox_04)
        vbox.addLayout(hbox_05)

        box = QVBoxLayout(self.widget)
        box.addLayout(vbox)
    
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
