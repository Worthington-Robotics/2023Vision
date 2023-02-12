"""
----------------------------------------------------------------------------
Authors:     FRC Team 4145
Description: This script 
----------------------------------------------------------------------------
"""

from networktables import NetworkTables


class Dispatcher:
    def __init__(self, teamNum) -> None:
        NetworkTables.startClientTeam(4145)
        NetworkTables.initialize()
        self.nt = NetworkTables.getTable("SmartDashboard")

    def dispatchVIOPose(self, position):
        """Sends the pose calculated from VIO of the ZED to SmartDashboard
        Args:
            position: position of the robot relative to beginning of auto
        """
        tx, ty, tz = position
        self.nt.putNumber("Jetson/robotpose/tx", tx)
        self.nt.putNumber("Jetson/robotpose/ty", ty)
        self.nt.putNumber("Jetson/robotpose/tz", tz)

    def dispatchTagPose(self, pose, yaw):
        """Sends the pose of the robot based on tags to smartdashboard
        Args: 
            pose: pose of robot calculated from Apriltags (as Detection[]) 
        """
        # TODO Should only be one pose calculated from however many tags seen
        if pose is not None:
            self.nt.putNumber("Jetson/AprilPose/x", pose[0][0])
            self.nt.putNumber("Jetson/AprilPose/y", pose[0][1])
            self.nt.putNumber("Jetson/AprilPose/z", pose[0][2])
            self.nt.putNumber("Jetson/AprilPose/yaw", yaw)
        else:
            print("No Detection")
            self.nt.putBoolean("Jetson/tag_pose/Updating", False)