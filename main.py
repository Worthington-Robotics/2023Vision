import cProfile
from queue import Empty
import sys
from multiprocessing import Process, Queue, Event
import time
from typing import Any, List, Optional
import cv2
from wpimath.geometry import *
from cscore import CameraServer
from utils import MovingAverage
from vision import WorbotsVision
from network import WorbotsTables
from config import WorbotsConfig
from vision.worbotsCamera import WorbotsCamera
from worbotsDetection import PoseDetection
from argparse import ArgumentParser

def main(configPath: Optional[str]):
    prof = cProfile.Profile()
    prof.enable()

    config = WorbotsConfig(configPath)
    camera = WorbotsCamera(configPath)
    output = Output(configPath)
    
    procCount = config.PROC_COUNT

    outQueue: Queue = Queue()
    processors: List[Processor] = []
    try:
        for i in range(procCount):
            processors.append(Processor(i, configPath, outQueue))
        
        # Used so that the printed FPS is only updated every couple of frames so it doesnt look
        # so jittery
        i = 0
        processorIndex = 0
        timeWhenLastFrameDone = time.time()
        averageFps = MovingAverage(80)
        while True:
            # Send frames from the camera to one of the processors
            frame = camera.getFrame()
            if frame is not None:
                processors[processorIndex].sendCameraFrame(frame)
                processorIndex += 1
                if processorIndex > procCount - 1:
                    processorIndex = 0

            # Get any processed frames from the processors
            try:
                frameData: FrameData = outQueue.get(timeout=0.001)
            except Empty:
                frameData = None
            if frameData is not None:
                output.sendPoseDetection(DetectionData(frameData.poseData, frameData.timestamp))

                if frameData.frame is not None:
                    output.sendFrame(frameData.frame)
                    

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
    prof.dump_stats("prof")

    print("Stopping!")
    camera.stop()
    output.stop()
    for proc in processors:
        proc.stop()

class FrameData:
    frame: Any
    poseData: Optional[PoseDetection]
    timestamp: float
    fps: float
    averageFps: Optional[float]

    def __init__(self, frame, poseData, timestamp, fps, averageFps):
        self.frame = frame
        self.poseData = poseData
        self.timestamp = timestamp
        self.fps = fps
        self.averageFps = averageFps

class Processor:
    proc: Process
    index: int
    inQueue = Queue()
    terminate = Event()

    def __init__(self, index: int, configPath: Optional[str], outQueue: Queue):
        self.index = index
        self.proc = Process(target=runProcessor, args=(index, configPath, self.inQueue, outQueue, self.terminate,), name="Vision Processor")
        self.proc.start()

    def sendCameraFrame(self, frame: Optional[Any]):
        if frame is not None:
            self.inQueue.put(frame)

    def stop(self):
        self.terminate.set()
        self.proc.terminate()

def runProcessor(index: int, configPath: Optional[str], inQueue: Queue, outQueue: Queue, terminate: Event):
    if index == 0:
        prof = cProfile.Profile()
        prof.enable()
    else:
        prof = None

    vision = WorbotsVision(hasCamera=False, configPath=configPath)
    config = WorbotsConfig(configPath)
    
    # vision.calibrateCameraImages("./images")
    # vision.calibrateCamLive()

    try:
        while not terminate.is_set():
            start = time.time()

            try:
                frame = inQueue.get(timeout=0.001)
            except Empty:
                frame = None
            poseDetection = None

            if frame is None:
                continue
            else:
                if config.PROCESS_VIDEO:
                    frame, poseDetection = vision.processFrame(frame)

            frameData = FrameData(frame, poseDetection, start, 0.0, 0.0)
            outQueue.put(frameData)

            if config.RUN_ONCE:
                break
    except Exception as e:
        print(e)
    
    if prof is not None:
        prof.disable()
        prof.dump_stats("proc_prof")

class DetectionData:
    poseData: Optional[PoseDetection]
    timestamp: float

    def __init__(self, poseData, timestamp):
        self.poseData = poseData
        self.timestamp = timestamp

class Output:
    proc: Process
    detectionQueue = Queue()
    fpsQueue = Queue()
    frameQueue = Queue()

    def __init__(self, configPath: Optional[str]):
        self.proc = Process(target=runOutput, args=(configPath, self.detectionQueue, self.fpsQueue, self.frameQueue,), name="Vision Output")
        self.proc.start()

    def sendPoseDetection(self, detection: Optional[DetectionData]):
        if detection is not None:
            self.detectionQueue.put(detection)

    def sendFrame(self, frame: Optional[Any]):
        if frame is not None:
            self.frameQueue.put(frame)

    def sendFps(self, fps: float):
        self.fpsQueue.put(fps)

    def stop(self):
        self.proc.terminate()

def runOutput(configPath: Optional[str], detectionQueue: Queue, fpsQueue: Queue, frameQueue: Queue):
    config = WorbotsConfig(configPath)
    network = WorbotsTables(configPath)
    CameraServer.enableLogging()
    output = CameraServer.putVideo("Module"+str(config.MODULE_ID), config.RES_W, config.RES_H)
    print(f"Optimized used?: {cv2.useOptimized()}")
    network.sendConfig()
    
    while True:
        # Pose detection
        try:
            detection: DetectionData = detectionQueue.get_nowait()
        except Empty:
            detection = None

        if config.SEND_POSE_DATA and detection is not None:
            network.sendPoseDetection(detection.poseData, detection.timestamp)

        # Camera frames
        try:
            frame: Any = frameQueue.get_nowait()
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
            fps: float = fpsQueue.get_nowait()
            network.sendFps(fps)
        except Empty:
            pass

        if config.RUN_ONCE:
            break

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--config-path", default="config.json", help="Path to the config file. Defaults to ./config.json")
    args = parser.parse_args()
    print(f"Config path: {args.config_path}")
        
    main(args.config_path)
