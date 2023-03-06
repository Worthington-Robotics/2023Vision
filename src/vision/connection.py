"""
----------------------------------------------------------------------------
Authors:     FRC Team 4145
Description: This script 
----------------------------------------------------------------------------
"""

from networktables import NetworkTables


class Connection:
    def __init__(self, teamNum) -> None:
        NetworkTables.startClientTeam(teamNum)
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
        # print(f"x offset {tx}")
        # print(f"y offset {ty}")

    def dispatchTagPose(self, pose, yaw):
        """Sends the pose of the robot based on tags to smartdashboard
        Args: 
            pose: pose of robot calculated from Apriltags (as Detection[]) 
        """
        # TODO Should only be one pose calculated from however many tags seen
        if pose is not None:
            self.nt.putNumber("Jetson/AprilPose/x", pose[0][0] * 3.28084)
            self.nt.putNumber("Jetson/AprilPose/y", pose[0][1] * 3.28084)
            self.nt.putNumber("Jetson/AprilPose/z", pose[0][2] * 3.28084)
            self.nt.putNumber("Jetson/AprilPose/yaw", yaw)
             # Z is forwards,back X is Left,right Y is Up down
            # print(yaw)
            #forwards back
            # print(f"forwards: {pose[0][0] * 3.28084 * 12}")
            # #left right
            # print(f"left right: {pose[0][1] * 3.28084 * 12}")
            # #up down
            # print(f"up down: {pose[0][2]}")
            
        else:
            # print("No Detection")
            self.nt.putBoolean("Jetson/tag_pose/Updating", False)
        
    def getTurretAngle(self):
        return self.nt.getNumber("Vision/Turret Offset", 0)