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

    def dispatchTagPose(self, pose):
        """Sends the pose of the robot based on tags to smartdashboard
        Args: 
            pose: pose of robot calculated from Apriltags (as Detection[]) 
        """
        # TODO Should only be one pose calculated from however many tags seen
        if pose:
            for detection in pose:
                x = detection.pose_t[0, 0]
                y = detection.pose_t[1, 0]
                z = detection.pose_t[2, 0]
                tagID = detection.tag_id
                print(tagID)
                self.nt.putBoolean("Jetson/tag_pose/Updating", True)
                self.nt.putNumber(f"Jetson/tag_pose/{tagID}/X", x)
                self.nt.putNumber(f"Jetson/tag_pose/{tagID}/Y", y)
                self.nt.putNumber(f"Jetson/tag_pose/{tagID}/Z", z)
            print("---------------------------")
        else:
            print("No Detection")
            self.nt.putBoolean("Jetson/tag_pose/Updating", False)
