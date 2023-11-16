from queue import Empty
from typing import Any, Union, Optional, List
import cv2
from multiprocessing import Process, Queue
from cProfile import Profile

from config.worbotsConfig import WorbotsConfig


class WorbotsCamera:
    proc: Process
    
    def __init__(self, configPath: Optional[str], out: List[Queue]):
        self.proc = Process(target=runCameraThread, args=(configPath, out,), name="Camera Process")
        self.proc.start()

    def stop(self):
        self.proc.terminate()

def runCameraThread(configPath: Optional[str], out: List[Queue]):
    prof = Profile()
    config = WorbotsConfig(configPath)
    prof.enable()
    cam = ThreadCamera(configPath)

    queueIndex = 0
    while True:
        frame = cam.getRawFrame()
        if frame is not None:
            out[queueIndex].put(frame)
            queueIndex += 1
            if queueIndex >= len(out):
                queueIndex = 0

        if config.RUN_ONCE:
            break

    prof.disable()
    prof.dump_stats("cam_prof")
        
class ThreadCamera:
    worConfig: WorbotsConfig
    cap: cv2.VideoCapture

    def __init__(self, configPath: Optional[str]):
        self.worConfig = WorbotsConfig(configPath)
        if self.worConfig.USE_GSTREAMER:
            print("Initializing camera with GStreamer...")
            self.cap = cv2.VideoCapture(f"gst-launch-1.0 -v v4l2src device=/dev/video{self.worConfig.CAMERA_ID} ! image/jpeg, width={self.worConfig.RES_W}, height={self.worConfig.RES_H}, format=MJPG, framerate={self.worConfig.CAM_FPS}/1 ! jpegdec ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
        else:
            print("Initializing camera with default backend...")
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.worConfig.RES_H)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.worConfig.RES_W)
            # self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
            # self.cap.set(cv2.CAP_PROP_HW_ACCELERATION, 1.0)
            self.cap.set(cv2.CAP_PROP_FPS, self.worConfig.CAM_FPS)

        if self.cap.isOpened():
            print(f"Initialized camera with {self.cap.get(cv2.CAP_PROP_BACKEND)} backend")
            print(f"Camera running at {self.cap.get(cv2.CAP_PROP_FPS)} fps")
        else:
            print("Failed to initialize camera")

    def getRawFrame(self) -> Union[Any, None]:
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            return None