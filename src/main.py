import cProfile
from queue import Empty
import queue
from threading import Thread, Event
import sys
import time
from typing import Any, Optional
import cv2
from wpimath.geometry import *
from cscore import CameraServer
from utils import MovingAverage
from vision import WorbotsVision
from network import WorbotsTables
from config import ConfigPaths, WorbotsConfig
from vision.camera import WorbotsCamera
from detection import PoseDetection
from argparse import ArgumentParser

def main(configPaths: ConfigPaths):
    prof = cProfile.Profile()
    prof.enable()

    camera = None
    output = None

    try:
        config = WorbotsConfig(configPaths)
        output = Output(configPaths)
        vision = WorbotsVision(configPaths)

        camera = WorbotsCamera(configPaths)
        
        # Used so that the printed FPS is only updated every couple of frames so it doesnt look
        # so jittery
        i = 0
        timeWhenLastFrameDone = time.time()
        averageFps = MovingAverage(80)
        while True:
            start = time.time()
            # Try to get a frame from the camera
            frame = camera.getFrame()

            # Process the frame
            poseDetection = None

            if frame is None:
                continue
            if config.PROCESS_VIDEO:
                frame, poseDetection = vision.processFrame(frame)

            # Send processed data to the output
            if poseDetection is not None:
                output.sendPoseDetection(DetectionData(poseDetection, start))

            if frame is not None:
                output.sendFrame(frame) 

            elapsed = time.time() - timeWhenLastFrameDone
            if elapsed != 0.0:
                fps = 1 / elapsed
                averageFps.add(fps)

            timeWhenLastFrameDone = time.time()

            if config.PRINT_FPS:
                if i % 10000 == 0:
                    sys.stdout.write(f"\rFPS: {averageFps.average()}")
                    sys.stdout.flush()

            output.sendFps(averageFps.average())

            if config.RUN_ONCE:
                break
    except Exception as e:
        print(e)

    prof.disable()
    prof.dump_stats("prof/prof")

    print("Stopping!")
    if camera is not None:
        camera.stop()
    if output is not None:
        output.stop()

class DetectionData:
    poseData: Optional[PoseDetection]
    timestamp: float

    def __init__(self, poseData, timestamp):
        self.poseData = poseData
        self.timestamp = timestamp

class Output:
    thread: Thread
    detectionQueue = queue.Queue()
    fpsQueue = queue.Queue()
    frameQueue = queue.Queue()
    stop: Event

    def __init__(self, configPaths: ConfigPaths):
        self.stop = Event()
        self.thread = Thread(target=runOutput, args=(self.stop, configPaths, self.detectionQueue, self.fpsQueue, self.frameQueue,), name="Vision Output", daemon=True)
        self.thread.start()

    def sendPoseDetection(self, detection: Optional[DetectionData]):
        if detection is not None:
            self.detectionQueue.put(detection)

    def sendFrame(self, frame: Optional[Any]):
        if frame is not None:
            self.frameQueue.put(frame)

    def sendFps(self, fps: float):
        self.fpsQueue.put(fps)

    def stop(self):
        self.stop.set()
        self.thread.join()

def runOutput(stop: Event, configPaths: ConfigPaths, detectionQueue: queue.Queue, fpsQueue: queue.Queue, frameQueue: queue.Queue):
    config = WorbotsConfig(configPaths)
    network = WorbotsTables(configPaths)
    CameraServer.enableLogging()
    output = CameraServer.putVideo("Module"+str(config.MODULE_ID), config.RES_W, config.RES_H)
    print(f"Optimized used?: {cv2.useOptimized()}")
    network.sendConfig()
    
    while not stop.is_set():
        # Pose detection
        try:
            detection: DetectionData = detectionQueue.get(timeout=0.001)
        except Empty:
            detection = None

        if config.SEND_POSE_DATA and detection is not None:
            network.sendPoseDetection(detection.poseData, detection.timestamp)

        # Camera frames
        try:
            frame: Any = frameQueue.get(timeout=0.001)
        except Empty:
            frame = None

        if frame is not None:
            output.putFrame(frame)
            if config.SHOW_IMAGE:
                cv2.imshow('image', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # FPS
        try:
            fps: float = fpsQueue.get(timeout=0.001)
            network.sendFps(fps)
        except Empty:
            pass

        if config.RUN_ONCE:
            break

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--config-path", default="config.json", help="Path to the config file. Defaults to ./config.json")
    parser.add_argument("-C", "--calibration-path", default="calibration.json", help="Path to the camera calibration file. Defaults to ./calibration.json")
    args = parser.parse_args()
    print(f"Config path: {args.config_path} Calibration path: {args.calibration_path}")
    print(f"CUDA: {cv2.cuda.getCudaEnabledDeviceCount()}")
    paths = ConfigPaths(args.config_path, args.calibration_path)
    main(paths)
