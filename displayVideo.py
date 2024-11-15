import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

# Aduino Video
def displayVideo(obj) :
    obj.buffer += obj.stream.read(4096)
    obj.head = obj.buffer.find(b'\xff\xd8')
    obj.end = obj.buffer.find(b'\xff\xd9')
    
    if obj.head > -1 and obj.end > -1 :
        jpg = obj.buffer[obj.head : obj.end + 2]
        obj.buffer = obj.buffer[obj.end + 2 :]
        obj.img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        
        # Haar ON/OFF
        if obj.is_haar :
            obj.haar()

        # LineTracing ON/OFF
        if obj.is_linetracing :
            obj.lineTracing()

        h, w, c = obj.img.shape
        obj.qimg = QImage(obj.img.data, w, h, w * c, QImage.Format_BGR888)
        obj.label.setPixmap(QPixmap.fromImage(obj.qimg))