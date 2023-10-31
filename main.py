import time
import cv2
import math
from wpimath.geometry import *
from cscore import CameraServer
from vision import WorbotsVision, PoseCalculator
from network import WorbotsTables
from config import WorbotsConfig

def main():
    config = WorbotsConfig()
    network = WorbotsTables()
    vision = WorbotsVision()
    CameraServer.enableLogging()
    output = CameraServer.putVideo("Module"+str(config.MODULE_ID), config.RES_W, config.RES_H)
    print(f"Optimized used?: {cv2.useOptimized()}")
    network.sendConfig()
    # vision.calibrateCameraImages("./images")
    # vision.calibrateCamLive()

    while True:
        start = time.time()

        frame, poseDetection = vision.processFrame()
        network.sendPoseDetection(poseDetection, math.floor(start * 1000000))
        
        output.putFrame(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps = int(1 / (time.time() - start))
        network.sendFps(fps)

if __name__ == '__main__':
    main()
