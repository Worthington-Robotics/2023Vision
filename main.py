import sys
import pyzed.sl as sl
import cv2
import sys
import time
import numpy
from pupil_apriltags import Detector
from vision import VisionProcesser, zed_init, init_calibration_params, Dispatcher

import time



def main():
    zed = zed_init()

    dispatcher = Dispatcher()

    runtime = sl.RuntimeParameters()
    camera_pose = sl.Pose()


    camera_params = init_calibration_params(zed)

    camera_info = zed.get_camera_information()

    pose_data = sl.Transform()

    detect = Detector()

    vision_processer = VisionProcesser(detect, zed)

    #start_time = time.time()
    #frame = 0
    #able to calculate robotpose 38 times a second?
    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            tracking_state = zed.get_position(camera_pose)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:
                tx, ty, tz = vision_processer.track_position(camera_pose, zed)
                frame = frame + 1
                tag_pose = vision_processer.april_tag_tracking()
                dispatcher.dispatch_robot_pose(tx, ty, tz)
                dispatcher.dispatch_tag_pose(tag_pose)
    
    #print(frame/60)             
        


if __name__ == "__main__":
    main()

