"""
----------------------------------------------------------------------------
Authors:     FRC Team 4145
Description: This script 
----------------------------------------------------------------------------
"""
from pyzed import sl
from Apriltags import Detector
from . import Constants, Dispatcher, PoseCalculator

import cv2
import math
import numpy as np


class VisionProcessor:
    def __init__(self, zed: sl.Camera, detector: Detector, dispatcher: Dispatcher, poseCalculator: PoseCalculator, cameraPose):
        self.zed = zed
        self.detctor = detector
        self.dispatcher = dispatcher
        self.poseCalculator = poseCalculator
        self.cameraPose = cameraPose
        pass

    def initializeZed(self):
        """Initializes the Zed with params set in Constants
        """
        status = self.zed.open(Constants.ZED_INIT_PARAMS)
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            exit()
        self.zed.enable_positional_tracking(sl.PositionalTrackingParameters())

    def trackVIOPosition(self, cameraPose):
        """Tracks the position of the zed with VIO
        Args:
            cameraPose: 
        """
        pyTranslation = sl.Translation()
        tx = round(cameraPose.get_translation(pyTranslation).get()[0], 3)
        ty = round(cameraPose.get_translation(pyTranslation).get()[1], 3)
        tz = round(cameraPose.get_translation(pyTranslation).get()[2], 3)

        return np.array([tx, ty, tz])

    def getTagDetections(self):
        zedImg = sl.Mat()
        self.zed.retrieve_image(zedImg, sl.VIEW.LEFT)
        zedCVImg = zedImg.get_data()
        cv2.imshow("img", zedCVImg)
        cv2.waitKey(5)
        zedCVImg = cv2.cvtColor(zedCVImg, cv2.COLOR_BGR2GRAY)

        zedCameraParams = self.zed.get_camera_information(
        ).camera_configuration.calibration_parameters.left_cam
        cameraParams = (zedCameraParams.fx, zedCameraParams.fy,
                        zedCameraParams.cx, zedCameraParams.cy)

        tagSizeInMeters = Constants.TAG_SIZE * 0.0254

        tag_detections = Detector(searchpath=['apriltags'], families='tag16h11', nthreads=1, quad_decimate=1.0, quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25, debug=0)

        return tag_detections

    def processVision(self):
        # Zed Tracking
        vioPosition = self.trackVIOPosition(self.cameraPose)
        translatedVIO = self.poseCalculator.translateZedPose(0, vioPosition)

        # Tag Tracking
        detections = self.getTagDetections()

        theta = 0

        num_april_tags = 0
        average_tag_pose = np.zeros((1, 3))
        average_yaw = 0
        for detection in detections:
            if(detection.hamming == 0):
                t_z_a = np.array([[detection.pose_R[0,0], detection.pose_R[0,1], detection.pose_R[0,2], detection.pose_t[0][0]],
                                  [detection.pose_R[1,0], detection.pose_R[1,1], detection.pose_R[1,2], detection.pose_t[1][0]],
                                  [detection.pose_R[2,0], detection.pose_R[2,1], detection.pose_R[2,2], detection.pose_t[2][0]], 
                                  [                    0,                     0,                     0,                   1]])
                t_f_r = self.poseCalculator.getRobotTranslation(detection.tag_id, t_z_a, theta)
                if(t_f_r is not None):
                    np.add(average_tag_pose, t_f_r[0:3, 3])
                    sy = math.sqrt(t_f_r[0,0] * t_f_r[0,0] +  t_f_r[1,0] * t_f_r[1,0])
                    singular = sy < 1e-6
                    # yaw = 0
                    # if not singular :
                    yaw = math.acos(t_f_r[0, 0])
                    average_yaw += yaw
                    num_april_tags += 1
                    # print(t_f_r[0, -1] * 12)
                    print(detection.tag_id)
        if num_april_tags != 0:
            tag_pose = np.divide(average_tag_pose, num_april_tags)
            average_yaw /= num_april_tags
            average_yaw = math.degrees(average_yaw)
        else:
            tag_pose = None
            average_yaw = None
        
            
        
        # Send data to SmartDashboard
        self.dispatcher.dispatchVIOPose(translatedVIO)
        self.dispatcher.dispatchTagPose(tag_pose, average_yaw)
