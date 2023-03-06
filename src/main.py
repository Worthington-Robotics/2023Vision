#!/usr/bin/env python3

"""
-----------------------------------------------------------------------------
Authors:     FRC Team 4145

Description: This script uses duckie-town apriltags and the zed sdk to
             process input from the Zed 2i Camera and publish certain values
             to SmartDashboard. This script designed to be used on the 
             Jetson Xavier.

Comments:    This script should be uploaded to the Jetson xavier via Secure
             Shell(ssh) by using the default IP address for the USB device
             server. Upon doing this, one must then use Secure Copy Protocol
             to move the files from a computer to the Jetson.
-----------------------------------------------------------------------------
"""

from pyzed import sl
from dt_apriltags import Detector
from vision import VisionProcessor, Dispatcher, Constants, PoseCalculator
import time


def main():
    zed = sl.Camera()
    cameraPose = sl.Pose()  
    runtime = sl.RuntimeParameters()

    detector = Detector(searchpath=['apriltags'],
                       families=Constants.TAG_FAMILY,
                       nthreads=5,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

    dispatcher = Dispatcher(4145)

    poseCalculator = PoseCalculator()

    visionProcessor = VisionProcessor(
        detector=detector, zed=zed, dispatcher=dispatcher, poseCalculator=poseCalculator, cameraPose=cameraPose)
        
    visionProcessor.initializeZed()
    # translation_left_to_center = zed.get_camera_information().calibration_parameters.T[0]

    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            tracking_state = zed.get_position(cameraPose)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:
                visionProcessor.processVision()

if __name__ == "__main__":
    main()
