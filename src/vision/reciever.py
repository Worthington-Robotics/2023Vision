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

class Reciever:
    def __init__(self) -> None:
        #this will connect to smart dashboard
        self.nt = NetworkTables.getTable("SmartDashboard")
        
    def recieve_turret_angle(self):
        """This function recieves the turret angle of the robot
        """
        pass