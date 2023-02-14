"""
----------------------------------------------------------------------------
Authors:     FRC Team 4145
Description: This script 
----------------------------------------------------------------------------
"""

from networktables import NetworkTables

class Reciever:
    def __init__(self) -> None:
        
        #this will connect to smart dashboard
        self.nt = NetworkTables.getTable("SmartDashboard")
        
    def recieve_turret_angle(self):
        #this function will get the turret angle
        pass