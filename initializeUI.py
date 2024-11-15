# GUI 프로그램에서 위젯 초기화 부분만 모아두기

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel

def initializeUI(obj) :
    # Speed
    obj.btn_speed_40 = QPushButton("Speed 40", obj)
    obj.btn_speed_50 = QPushButton("Speed 50", obj)
    obj.btn_speed_60 = QPushButton("Speed 60", obj)
    obj.btn_speed_80 = QPushButton("Speed 80", obj)
    obj.btn_speed_100 = QPushButton("Speed 100", obj)

    # Move
    obj.btn_stop = QPushButton("Stop", obj)
    obj.btn_left = QPushButton("Left", obj)
    obj.btn_right = QPushButton("Right", obj)
    obj.btn_forward = QPushButton("Forward", obj)
    obj.btn_backward = QPushButton("Backward", obj)
    obj.btn_turn_left = QPushButton("Turn Left", obj)
    obj.btn_turn_right = QPushButton("Turn Right", obj)

    obj.widget = QWidget()
    obj.setWindowTitle(obj.title)
    obj.setCentralWidget(obj.widget)
    obj.setFixedSize(600, 700)
    obj.label = QLabel()
    obj.label.resize(600, 300)
    obj.label.setScaledContents(True)
    
    # Pressed
    obj.btn_left.pressed.connect(obj.left)
    obj.btn_right.pressed.connect(obj.right)
    obj.btn_forward.pressed.connect(obj.forward)
    obj.btn_backward.pressed.connect(obj.backward)
    obj.btn_turn_left.pressed.connect(obj.turn_left)
    obj.btn_turn_right.pressed.connect(obj.turn_right)

    # Released
    obj.btn_left.released.connect(obj.stop)
    obj.btn_right.released.connect(obj.stop)
    obj.btn_forward.released.connect(obj.stop)
    obj.btn_backward.released.connect(obj.stop)
    obj.btn_turn_left.released.connect(obj.stop)
    obj.btn_turn_right.released.connect(obj.stop)

    # Clicked
    obj.btn_speed_40.clicked.connect(obj.speed40)
    obj.btn_speed_50.clicked.connect(obj.speed50)
    obj.btn_speed_60.clicked.connect(obj.speed60)
    obj.btn_speed_80.clicked.connect(obj.speed80)
    obj.btn_speed_100.clicked.connect(obj.speed100)
    obj.btn_stop.clicked.connect(obj.stop)
    obj.btn_haar.clicked.connect(obj.toggle_haar)
    obj.btn_linetracing.clicked.connect(obj.toggle_lineTracing)

    # Layout
    video_box = QHBoxLayout()
    video_box.addWidget(obj.label)

    hbox_01 = QHBoxLayout()
    hbox_01.addWidget(obj.btn_haar)
    hbox_01.addWidget(obj.btn_linetracing)

    hbox_02 = QHBoxLayout()
    hbox_02.addWidget(obj.btn_speed_40)
    hbox_02.addWidget(obj.btn_speed_50)
    hbox_02.addWidget(obj.btn_speed_60)
    hbox_02.addWidget(obj.btn_speed_80)
    hbox_02.addWidget(obj.btn_speed_100)

    hbox_03 = QHBoxLayout()
    hbox_03.addWidget(obj.btn_stop)
    hbox_03.addWidget(obj.btn_forward)
    hbox_03.addWidget(obj.btn_backward)

    hbox_04 = QHBoxLayout()
    hbox_04.addWidget(obj.btn_turn_left)
    hbox_04.addWidget(obj.btn_turn_right)

    hbox_05 = QHBoxLayout()
    hbox_05.addWidget(obj.btn_left)
    hbox_05.addWidget(obj.btn_right)

    vbox = QVBoxLayout()
    vbox.addLayout(video_box)
    vbox.addLayout(hbox_01)
    vbox.addLayout(hbox_02)
    vbox.addLayout(hbox_03)
    vbox.addLayout(hbox_04)
    vbox.addLayout(hbox_05)

    box = QVBoxLayout(obj.widget)
    box.addLayout(vbox)