import cv2
from typing import List, Union
import numpy as np
import math
from config import WorbotsConfig
from wpimath.geometry import *
from worbotsDetection import Detection, PoseDetection
from .worbotsPoseCalculator import PoseCalculator, Pose3d
from network import WorbotsTables
import os

class WorbotsVision:
    worConfig = WorbotsConfig()
    worNetwork = WorbotsTables()
    mtx, dist = worConfig.getCameraIntrinsicsFromJSON()
    axis_len = 0.1
    poseCalc = PoseCalculator()
    tag_size = worConfig.TAG_SIZE_METERS
    obj_1 = [-tag_size/2, tag_size/2, 0.0]
    obj_2 = [tag_size/2, tag_size/2, 0.0]
    obj_3 = [tag_size/2, -tag_size/2, 0.0]
    obj_4 = [-tag_size/2, -tag_size/2, 0.0]
    obj_all = obj_1 + obj_2 + obj_3 + obj_4
    objPoints = np.array(obj_all).reshape(4,3)
    axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

    def __init__(self):
        self.cap = cv2.VideoCapture(self.worConfig.CAMERA_ID)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.worConfig.RES_W)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.worConfig.RES_H)
        self.cap.set(cv2.CAP_PROP_FPS, self.worConfig.CAM_FPS)
        print("done init")

    def setCamResolution(self, width, height):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def openMain(self):
        while True:
            ret, frame = self.cap.read()
            frameCopy = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
            detectorParams = cv2.aruco.DetectorParameters()
            (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray, dictionary=dictionary, parameters=detectorParams)
            cv2.aruco.drawDetectedMarkers(image=frameCopy, corners=corners, ids=ids)
            cv2.imshow("out",frameCopy)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

    def calibrateCameraImages(self, folderName):
        images = os.listdir(folderName)

        # Define the board
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        board = cv2.aruco.CharucoBoard((11, 8), 0.024, 0.019, dictionary)

        allCharucoCorners: List[np.ndarray] = []
        allCharucoIds: List[np.ndarray] = []

        for fname in images:
            img = cv2.imread(os.path.join(folderName, fname))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
            # Detect corners as well as markers
            charucoParams = cv2.aruco.CharucoParameters()
            detectorParams = cv2.aruco.DetectorParameters()
            detector = cv2.aruco.CharucoDetector(board, charucoParams, detectorParams)
            (charucoCorners, charucoIds, markerCorners, markerIds) = detector.detectBoard(gray)

            if charucoCorners is not None and charucoIds is not None:
                if len(charucoCorners) == len(charucoIds):
                    allCharucoCorners.append(charucoCorners)
                    allCharucoIds.append(charucoIds)

        if len(allCharucoCorners) > 0:
            ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.aruco.calibrateCameraCharuco(
                allCharucoCorners, allCharucoIds, board, gray.shape[::-1], None, None
            )
            self.worConfig.saveCameraIntrinsics(self.mtx, self.dist, self.rvecs, self.tvecs)
            print(ret)
        else:
            print("No Charuco corners were detected for calibration.")

    def calibrateCamLive(self):
        allCharucoCorners: List[np.ndarray] = []
        allCharucoIds: List[np.ndarray] = []
        while True:
            ret, img = self.cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Define the board
            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
            board = cv2.aruco.CharucoBoard((11, 8), 0.024, 0.019, dictionary)

            # Detect corners as well as markers
            charucoParams = cv2.aruco.CharucoParameters()
            detectorParams = cv2.aruco.DetectorParameters()
            detector = cv2.aruco.CharucoDetector(board, charucoParams, detectorParams)
            (charucoCorners, charucoIds, markerCorners, markerIds) = detector.detectBoard(gray)
            if charucoCorners is not None and charucoIds is not None:
                cv2.aruco.drawDetectedCornersCharuco(img, charucoCorners, charucoIds, (0, 0, 255))
                if len(charucoCorners) == len(charucoIds):
                    if (len(charucoCorners) > 10):
                        allCharucoCorners.append(charucoCorners)
                        allCharucoIds.append(charucoIds)
            cv2.imshow("out", img)
            print(len(allCharucoCorners))
            if len(allCharucoCorners) > 10:
                ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.aruco.calibrateCameraCharuco(
                    allCharucoCorners, allCharucoIds, board, gray.shape[::-1], None, None
                )
                self.worConfig.saveCameraIntrinsics(self.mtx, self.dist, self.rvecs, self.tvecs)
                print(ret)
                break

        
    
    def mainPnP(self):
        while True:
            returnArray = np.array([], dtype=Detection)
            ret, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
            detectorParams = cv2.aruco.DetectorParameters()
            (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray, dictionary=dictionary, parameters=detectorParams)

            if ids is not None and len(ids) > 0:
                for i in range(len(ids)):
                    ret, rvec, tvec = cv2.solvePnP(self.objPoints, corners[i], self.mtx, self.dist, flags=cv2.SOLVEPNP_IPPE_SQUARE)
                    # print(f"Translation: {tvec[0]},{tvec[1]},{tvec[2]}, Rotation: {rvec[0]},{rvec[1]},{rvec[2]}")
                    detection = Detection(ids[i], tvec, rvec)
                    returnArray = np.append(returnArray, detection)
                    frame = cv2.drawFrameAxes(frame, self.mtx, self.dist, rvec, tvec, self.axis_len)
                cv2.aruco.drawDetectedMarkers(frame, corners, ids, (0, 0, 255))
            print(returnArray.size)
            cv2.imshow("out", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def mainPnPSingleFrame(self) -> any:
        returnArray = np.array([], Detection)
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
        detectorParams = cv2.aruco.DetectorParameters()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray, dictionary=dictionary, parameters=detectorParams)
        if ids is not None and len(ids) > 0:
            for i in range(len(ids)):
                ret, rvec, tvec = cv2.solvePnP(self.objPoints, corners[i], self.mtx, self.dist, flags=cv2.SOLVEPNP_IPPE_SQUARE)
                # print(f"Translation: {tvec[0]},{tvec[1]},{tvec[2]}, Rotation: {rvec[0]},{rvec[1]},{rvec[2]}")
                detection = Detection(ids[i], tvec, rvec)
                returnArray = np.append(returnArray, detection)
                frame = cv2.drawFrameAxes(frame, self.mtx, self.dist, rvec, tvec, self.axis_len)
            cv2.aruco.drawDetectedMarkers(frame, corners, ids, (0, 0, 255))
        return frame, returnArray
 
    def processFrame(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        imgPoints = []
        objPoints = []

        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
        detectorParams = cv2.aruco.DetectorParameters()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(gray, dictionary, None, None, detectorParams)

        if ids is not None:
            if len(ids) > 0:
                index = 0
                for id in ids:
                    pose = self.poseCalc.getPose3dFromTagID(id)
                    corner0 = pose + Transform3d((Translation3d(0, self.tag_size/2.0, -self.tag_size/2.0)), Rotation3d())
                    corner1 = pose + Transform3d((Translation3d(0, -self.tag_size/2.0, -self.tag_size/2.0)), Rotation3d())
                    corner2 = pose + Transform3d((Translation3d(0, -self.tag_size/2.0, self.tag_size/2.0)), Rotation3d())
                    corner3 = pose + Transform3d((Translation3d(0, self.tag_size/2.0, self.tag_size/2.0)), Rotation3d())
                    objPoints += [
                        self.poseCalc.wpiTranslationToOpenCV(corner0.translation()),
                        self.poseCalc.wpiTranslationToOpenCV(corner1.translation()),
                        self.poseCalc.wpiTranslationToOpenCV(corner2.translation()),
                        self.poseCalc.wpiTranslationToOpenCV(corner3.translation())
                    ]
                    imgPoints += [
                        [corners[index][0][0][0], corners[index][0][0][1]],
                        [corners[index][0][1][0], corners[index][0][1][1]],
                        [corners[index][0][2][0], corners[index][0][2][1]],
                        [corners[index][0][3][0], corners[index][0][3][1]]
                    ]
                    index +=1
            index = 0
            camera_to_robot_pose = self.poseCalc.openCvtoWpi(np.array([[self.worConfig.CAM_TO_ROBOT_X], [self.worConfig.CAM_TO_ROBOT_Y], [self.worConfig.CAM_TO_ROBOT_Z]]), np.array([[self.worConfig.CAM_TO_ROBOT_ROLL], [self.worConfig.CAM_TO_ROBOT_PITCH], [self.worConfig.CAM_TO_ROBOT_YAW]]))
            camera_to_robot = Transform3d(camera_to_robot_pose.translation(), camera_to_robot_pose.rotation())
            if len(ids)==1:
                _, rvec, tvec, errors = cv2.solvePnPGeneric(self.objPoints, np.array(imgPoints), self.mtx, self.dist, flags=cv2.SOLVEPNP_IPPE_SQUARE)
                field_to_tag_pose = self.poseCalc.getPose3dFromTagID(ids[0])
                camera_to_tag_pose_0 = self.poseCalc.openCvtoWpi(tvec[0], rvec[0])
                camera_to_tag_pose_1 = self.poseCalc.openCvtoWpi(tvec[1], rvec[1])
                camera_to_tag_0 = Transform3d(camera_to_tag_pose_0.translation(), camera_to_tag_pose_0.rotation())
                camera_to_tag_1 = Transform3d(camera_to_tag_pose_1.translation(), camera_to_tag_pose_1.rotation())
                field_to_camera_0 = field_to_tag_pose.transformBy(camera_to_tag_0.inverse())
                field_to_camera_1 = field_to_tag_pose.transformBy(camera_to_tag_1.inverse())
                field_to_camera_pose_0 = Pose3d(field_to_camera_0.translation(), field_to_camera_0.rotation())
                field_to_camera_pose_1 = Pose3d(field_to_camera_1.translation(), field_to_camera_1.rotation())
                field_to_robot_pose_0 = field_to_camera_pose_0.transformBy(camera_to_robot)
                field_to_robot_pose_1 = field_to_camera_pose_1.transformBy(camera_to_robot)
                return gray, PoseDetection(field_to_robot_pose_0, errors[0][0], field_to_robot_pose_1, errors[1][0], ids[0])
            if len(ids)>1:
                _, rvec, tvec, errors = cv2.solvePnPGeneric(np.array(objPoints), np.array(imgPoints), self.mtx, self.dist, flags=cv2.SOLVEPNP_SQPNP)
                camera_to_field_pose = self.poseCalc.openCvtoWpi(tvec[0], rvec[0])
                camera_to_field = Transform3d(camera_to_field_pose.translation(), camera_to_field_pose.rotation())
                field_to_camera = camera_to_field.inverse()
                field_to_camera_pose = Pose3d(field_to_camera.translation(), field_to_camera.rotation())
                field_to_robot_pose = field_to_camera_pose.transformBy(camera_to_robot)
                return gray, PoseDetection(field_to_robot_pose, errors[0][0], None, None, ids)
        else:
            return gray, None


    def checkCalib(self):
        mtx, dist, rvecs, tvecs = self.worConfig.getCameraIntrinsicsFromJSON()
        while True:
            ret, frame = self.cap.read()
            cv2.undistort(frame, mtx, dist, None)

            cv2.imshow("out", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

