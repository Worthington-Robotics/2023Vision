import os
import time
import numpy as np
import cv2
from cvu.detector.yolov5 import Yolov5 as Yolov5Trt

cap = cv2.VideoCapture(0)

keyPress = None
os.curdir
model = Yolov5Trt(classes=["cone, cube"],
                  backend="tensorrt",
                  weight=f"{os.curdir}/models/best.engine",
                  auto_install=False,
                  dtype='fp16')

while keyPress != ord('q'):
    ret, image = cap.read()

    if ret:
        preds = model(image)
        pass
