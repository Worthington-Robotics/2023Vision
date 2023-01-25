import sys
import pyzed.sl as sl
import cv2
import sys
import time
import numpy
from pupil_apriltags import Detector
from vision.zed_init import zed_init
from vision.zed_params import *
from vision.vision_processing import VisionProcesser
from xavier_testing import xavier_testing


def main():
    zed = zed_init()

    runtime = sl.RuntimeParameters()
    camera_pose = sl.Pose()

    camera_params = init_calibration_params(zed)

    camera_info = zed.get_camera_information()

    pose_data = sl.Transform()

    detect = Detector()

    vision_processer = VisionProcesser(detect, zed)

    #delete before competition:
    test = xavier_testing()
    
    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            tracking_state = zed.get_position(camera_pose)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:
                tx, ty, tz = vision_processer.track_position(camera_pose, zed)
                #test.print_robot_pose(tx, ty, tz)
                tag_pose = vision_processer.april_tag_tracking()
                test.print_tag_pose(tag_pose)
        


if __name__ == "__main__":
    main()

