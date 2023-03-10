#!/usr/bin/env python3

"""
----------------------------------------------------------------------------
Authors:     FRC Team 4145

Description: This script uses duckie-town apriltags and the zed sdk to
             process input from the Zed 2i Camera and publish certain values
             to SmartDashboard. This script designed to be used on the 
             Jetson Xavier.
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
        else:
            self.nt.putBoolean("Jetson/tag_pose/Updating", False)
        
    def getTurretAngle(self):
        """This function gets the turret angle from smartdashboard
        Returns:
            the turret angle recieved from smartdashboard
        """
        return self.nt.getNumber("Vision/Turret Offset", 0)
