import sys
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

    # Set to true to have the pipeline only run once
    runOnce = False
    # Set to false to disable processing and pose detection
    processVideo = True
    # Set to false to disable sending pose data to nt
    sendPoseData = True
    # Set to true to show the frame when running locally
    showImage = False
    # Set to true to print the fps to the console
    printFps = False

    # Used so that the printed FPS is only updated every couple of frames so it doesnt look
    # so jittery
    i = 0
    fpses = []
    while True:
        start = time.time()

        frame = None
        if processVideo:
            frame = vision.getRawFrame()
            frame, poseDetection = vision.processFrame(frame)
            if sendPoseData:
                network.sendPoseDetection(poseDetection, math.floor(start * 1000000))
        else:
            frame = vision.getRawFrame()
        
        output.putFrame(frame)
        if showImage:
            cv2.imshow('image', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps = int(1 / (time.time() - start))
        network.sendFps(fps)

        if printFps:
            fpses.append(fps)
            average = sum(fpses) / len(fpses)
            if i % 10 == 0:
                sys.stdout.write(f"\rFPS: {fps}   Average: {average}   ")
                sys.stdout.flush()

        if runOnce:
            break

        i += 1

if __name__ == '__main__':
    main()
