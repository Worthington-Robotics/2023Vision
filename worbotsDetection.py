from wpimath.geometry import *

class Detection:
    tag_id = None
    tvec = None
    rvec = None

    def __init__(self, tag_id, tvec, rvec):
        self.tag_id = tag_id
        self.tvec = tvec
        self.rvec = rvec

# Pose3d that can be pickled and sent between threads
class SendablePose3d:
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float

    def __init__(self, x, y, z, rx, ry, rz):
        self.x = x
        self.y = y
        self.z = z
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def fromPose3d(pose: Pose3d):
        SendablePose3d(pose.X(), pose.Y(), pose.Z(), pose.rotation().X(), pose.rotation().Y(), pose.rotation().Z())

    def toPose3d(self) -> Pose3d:
        Pose3d(self.x, self.y, self.x, Rotation3d(self.rx, self.ry, self.rz))

    
class PoseDetection:
    pose1: SendablePose3d = None
    err1: float = None
    pose2: SendablePose3d = None
    err2: float = None
    tag_ids: list = None

    def __init__(self, pose1: Pose3d, err1: float, pose2: Pose3d, err2: float, tag_ids: list):
        self.pose1 = SendablePose3d.fromPose3d(pose1)
        self.err1 = err1
        self.pose2 = SendablePose3d.fromPose3d(pose2)
        self.err2 = err2
        self.tag_ids = tag_ids
