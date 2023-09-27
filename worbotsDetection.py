from wpimath.geometry import *

class Detection:
    tag_id = None
    tvec = None
    rvec = None

    def __init__(self, tag_id, tvec, rvec):
        self.tag_id = tag_id
        self.tvec = tvec
        self.rvec = rvec
    
class PoseDetection:
    pose1 = None
    err1 = None
    pose2 = None
    err2= None
    tag_ids = None

    def __init__(self, pose1:Pose3d, err1, pose2:Pose3d, err2, tag_ids):
        self.pose1 = pose1
        self.err1 = err1
        self.pose2 = pose2
        self.err2 = err2
        self.tag_ids = tag_ids