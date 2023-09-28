import threading
import json
import time
import cv2
from wpimath.geometry import *
from vision import WorbotsVision, PoseCalculator
from network import WorbotsTables
from config import WorbotsConfig

def main():
    config = WorbotsConfig()
    network = WorbotsTables()
    vision = WorbotsVision()
    calc = PoseCalculator()
    print(f"Optimized used?: {cv2.useOptimized()}")
    network.sendConfig()
    # vision.calibrateCameraImages("./images")
    # vision.calibrateCamLive()

    while True:
        start = time.time()

        frame, poseDetection = vision.processFrame()
        network.sendPoseDetection(poseDetection)
        
        # cv2.imshow("out", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps = int(1 / (time.time() - start))
        network.sendFps(fps)

if __name__ == '__main__':
    main()
