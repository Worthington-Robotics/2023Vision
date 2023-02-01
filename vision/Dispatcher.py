from networktables import NetworkTables

class Dispatcher:
    def __init__(self):
        NetworkTables.startClientTeam(4145, 1250)
        NetworkTables.initialize()
        self.sd = NetworkTables.getTable("SmartDashboard")
    def dispatch_robot_pose(self, tx, ty, tz):
        self.sd.putNumber("Jetson/robotpose/tx", tx)
        self.sd.putNumber("Jetson/robotpose/ty", ty)
        self.sd.putNumber("Jetson/robotpose/tz", tz)
    def dispatch_tag_pose(self, tag_pose):
       if(tag_pose):
           for detection in tag_pose:
               self.sd.putNumber("Jetson/tag_pose/tag_id", detection.tag_id)
               self.sd.putNumber("Jetson/tag_pose/Z", detection.pose_t[2,0])
               self.sd.putNumber("Jetson/tag_pose/X", detection.pose_t[0,0])
               self.sd.putNumber("Jetson/tag_pose/Y", detection.pose_t[1,0])