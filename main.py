import sys
import pyzed.sl as sl
import cv2
import sys
import time
import numpy
from pupil_apriltags import Detector
from vision.zed_init import zed_init
from vision.zed_params import *
from vision.vision_processing import VisionProcessing


def main():
    zed = zed_init()

    runtime = sl.RuntimeParameters()
    camera_pose = sl.Pose()

    camera_params = init_calibration_params(zed)

    camera_info = zed.get_camera_information()

    pose_data = sl.Transform()

    detect = Detector(camera_pose)

    while True:
        VisionProcessing.track_position()


if __name__ == "__main__":
    main()

