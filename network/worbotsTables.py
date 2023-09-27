import time
import ntcore
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
    pose0Publisher = None
    pose1Publisher = None

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

        table = self.ntInstance.getTable(f"/module{self.config.MODULE_ID}/output")
        self.dataPublisher = table.getDoubleArrayTopic("data").publish(ntcore.PubSubOptions())
        self.pose0Publisher = table.getDoubleArrayTopic("pose0").publish(ntcore.PubSubOptions())
        self.pose1Publisher = table.getDoubleArrayTopic("pose1").publish(ntcore.PubSubOptions())
        self.fpsPublisher = table.getDoubleTopic("fps").publish(ntcore.PubSubOptions())

    def sendPoseDetection(self, poseDetection: PoseDetection):
        if poseDetection is None:
            self.pose0Publisher.set([])
            self.pose1Publisher.set([])
        else:
            if poseDetection.pose1 is not None:
                self.pose0Publisher.set(self.getArrayFromPose3d(poseDetection.pose1))
            else:
                self.pose0Publisher.set([])
            if poseDetection.pose2 is not None:
                self.pose1Publisher.set(self.getArrayFromPose3d(poseDetection.pose2))
            else:
                self.pose1Publisher.set([])

    def checkForConfigChange(self):
        print("Checking for config changes..")
    
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