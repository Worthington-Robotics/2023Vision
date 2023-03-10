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

from pyzed import sl
import math
import numpy as np


class Constants:
    ZED_HEIGHT = 0.9652 # change to robot height when mounted

    ZED_INIT_PARAMS = sl.InitParameters()
    # Use HD720 video mode (default fps: 60)
    ZED_INIT_PARAMS.camera_resolution = sl.RESOLUTION.HD720
    # Use a right-handed Z-up coordinate system
    ZED_INIT_PARAMS.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Z_UP_X_FWD
    ZED_INIT_PARAMS.coordinate_units = sl.UNIT.FOOT  # Set units in meters

    # Apriltag constants
    TAG_FAMILY = "tag16h5"
    # actually tag is 6in x 6in
    TAG_SIZE = 6

    # 0.12003468811511994
    ZED_CAMERA_OFFSET =  0.0635

    t_z_zp = np.array([[ 1,       0,       0,  ZED_CAMERA_OFFSET], 
                       [ 0,  0.9271838546, -0.3746065934,                  0], 
                       [ 0,  0.3746065934,  0.9271838546,                  0], 
                       [ 0,       0,       0,                  1]])
    
    #Field to april tag matrices
    T_F_A1 = np.array([[ 0,  0, 1,  15.513558], 
                       [-1,  0, 0,   1.071626], 
                       [ 0, -1, 0,   0.462788], 
                       [ 0,  0, 0,          1]])


    T_F_A2 = np.array([[0,  0, 1, 15.513558], 
                       [-1, 0, 0,  2.748026], 
                       [0, -1, 0,  0.462788], 
                       [0,  0, 0,         1]])


    T_F_A3 = np.array([[ 0,  0, 1, 15.513558], 
                       [-1,  0, 0,  4.424426], 
                       [ 0, -1, 0,    0.5842],  #change this value back to actual amount
                       [ 0,  0, 0,         1]])


    T_F_A4 = np.array([[0, 0, 1,  16.178784], 
                       [-1, 0, 0,  6.749796], 
                       [0, -1, 0,  0.695452], 
                       [0, 0, 0,          1]])


    T_F_A5 = np.array([[0,  0, -1,   0.36195], 
                       [1,  0,  0,  6.749796], 
                       [0, -1,  0,  0.695452], 
                       [0,  0,  0,         1]])


    T_F_A6 = np.array([[0,  0, -1,   1.02743], 
                       [1,  0,  0,  4.424426], 
                       [0, -1,  0,  0.5334], #CHANGE BACK
                       [0,  0,  0,         1]])

    T_F_A7 = np.array([[0,  0, -1,   1.02743], 
                       [1,  0,  0,  2.748026], 
                       [0, -1,  0,  0.462788], 
                       [0,  0,  0,         1]])

    T_F_A8 = np.array([[0,  0, -1,   1.02743], 
                       [1,  0,  0,  1.071626], 
                       [0, -1,  0,   0.56642], 
                       [0,  0,  0,         1]])