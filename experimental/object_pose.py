#this script will hopefully be able to determine the distance of the ball and how much the turret will need to turn in order to be able to pick up the ball

#planning out program:

#1 set up stereo camera system
#2?

import cv2
import numpy as np
import pyzed.sl as sl

class ObjectPose:
    def ObjectPose(self):
        zed = sl.Camera()
        init_params = sl.InitParams()
        init_params.camera_resoultion = sl.RESOLUTION.HD720
        init_params.camera_fps = 30
        init_params.depth_mode = sl.DEPTH_MODE.ULTRA #what does this line of code do?
        err = zed.open(init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            print("error occured")
            exit()


    