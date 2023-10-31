import time
import ntcore
import math
import numpy as np
from config import WorbotsConfig
from worbotsDetection import Detection, PoseDetection
from wpimath.geometry import *

class WorbotsTables:
    config = WorbotsConfig()
    ntInstance = None

    # Output Publishers
    fpsPublisher = None
    dataPublisher = None

    # Config Subscribers
    cameraIdSubscriber: ntcore.IntegerSubscriber

    def __init__(self):
        self.ntInstance = ntcore.NetworkTableInstance.getDefault()
        if self.config.SIM_MODE:
            self.ntInstance.setServer("127.0.0.1")
            self.ntInstance.startClient4(f"VisionModule{self.config.MODULE_ID}")
        else:
            self.ntInstance.setServerTeam(self.config.TEAM_NUMBER)
            self.ntInstance.startClient4(f"VisionModule{self.config.MODULE_ID}")

        self.moduleTable = self.ntInstance.getTable(f"/module{self.config.MODULE_ID}")
        table = self.moduleTable.getSubTable("output")
        configTable = self.moduleTable.getSubTable("config")
        self.dataPublisher = table.getDoubleArrayTopic("data").publish(ntcore.PubSubOptions())
        self.fpsPublisher = table.getDoubleTopic("fps").publish(ntcore.PubSubOptions())
        configTable.getBooleanTopic("liveCalib").publish().set(False)
        self.calibListener = configTable.getBooleanTopic("liveCalib").subscribe(False)

    def sendPoseDetection(self, poseDetection: PoseDetection, timestamp: float):
        if poseDetection is not None:
            dataArray = [0]
            dataArray[0] = 1
            if poseDetection.err1 and poseDetection.pose1 is not None:
                dataArray.append(poseDetection.err1)
                dataArray.append(poseDetection.pose1.X())
                dataArray.append(poseDetection.pose1.Y())
                dataArray.append(poseDetection.pose1.Z())
                dataArray.append(poseDetection.pose1.rotation().getQuaternion().W())
                dataArray.append(poseDetection.pose1.rotation().getQuaternion().X())
                dataArray.append(poseDetection.pose1.rotation().getQuaternion().Y())
                dataArray.append(poseDetection.pose1.rotation().getQuaternion().Z())
            if poseDetection.err2 and poseDetection.pose2 is not None:
                dataArray[0] = 2
                dataArray.append(poseDetection.err2)
                dataArray.append(poseDetection.pose2.X())
                dataArray.append(poseDetection.pose2.Y())
                dataArray.append(poseDetection.pose2.Z())
                dataArray.append(poseDetection.pose2.rotation().getQuaternion().W())
                dataArray.append(poseDetection.pose2.rotation().getQuaternion().X())
                dataArray.append(poseDetection.pose2.rotation().getQuaternion().Y())
                dataArray.append(poseDetection.pose2.rotation().getQuaternion().Z())
            for tag_id in poseDetection.tag_ids:
                dataArray.append(tag_id)
            self.dataPublisher.set(dataArray, math.floor(timestamp * 1000000))
    
    def sendPose3d(self, pose: Pose3d):
        self.dataPublisher.set(self.getArrayFromPose3d(pose))

    def sendFps(self, fps):
        self.fpsPublisher.set(fps)

    def sendConfig(self):
        configTable = ntcore.NetworkTableInstance.getDefault().getTable(f"/module{self.config.MODULE_ID}/config")
        self.cameraIdSubscriber = configTable.getDoubleTopic("cameraId").subscribe(self.config.CAMERA_ID, ntcore.PubSubOptions())

    def getArrayFromPose3d(self, pose: Pose3d) -> any:
        outArray = []
        outArray.append(pose.X())
        outArray.append(pose.Y())
        outArray.append(pose.Z())
        outArray.append(pose.rotation().getQuaternion().W())
        outArray.append(pose.rotation().getQuaternion().X())
        outArray.append(pose.rotation().getQuaternion().Y())
        outArray.append(pose.rotation().getQuaternion().Z())
        return outArray