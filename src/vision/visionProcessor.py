"""
----------------------------------------------------------------------------
Authors:     FRC Team 4145
Description: This script 
----------------------------------------------------------------------------
"""
from pyzed import sl
from pupil_apriltags import Detector
from . import Constants, Dispatcher, PoseCalculator

import cv2
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
        zedCVImg = cv2.cvtColor(zedCVImg, cv2.COLOR_BGR2GRAY)

        zedCameraParams = self.zed.get_camera_information(
        ).camera_configuration.calibration_parameters.left_cam
        cameraParams = (zedCameraParams.fx, zedCameraParams.fy,
                        zedCameraParams.cx, zedCameraParams.cy)

        tagSizeInMeters = Constants.TAG_SIZE * 0.0254

        detections = self.detctor.detect(
            img=zedCVImg, estimate_tag_pose=True, camera_params=cameraParams, tag_size=tagSizeInMeters)

        return detections

    def processVision(self):
        # Zed Tracking
        vioPosition = self.trackVIOPosition(self.cameraPose)
        translatedVIO = self.poseCalculator.translateZedPose(0, vioPosition)

        # Tag Tracking
        detections = self.getTagDetections()

        # Send data to SmartDashboard
        self.dispatcher.dispatchVIOPose(translatedVIO)
        self.dispatcher.dispatchTagPose(detections)
