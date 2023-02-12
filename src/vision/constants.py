from pyzed import sl
import math
import numpy as np


class Constants:
    ZED_HEIGHT = 1.604167

    ZED_INIT_PARAMS = sl.InitParameters()
    # Use HD720 video mode (default fps: 60)
    ZED_INIT_PARAMS.camera_resolution = sl.RESOLUTION.VGA
    # Use a right-handed Z-up coordinate system
    ZED_INIT_PARAMS.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Z_UP
    ZED_INIT_PARAMS.coordinate_units = sl.UNIT.FOOT  # Set units in feet

    # Apriltag constants
    TAG_FAMILY = "tag16h5"
    # In inches
    # actually tag is 6in x 6in
    TAG_SIZE = 6

    ZED_CAMERA_OFFSET = .3938


    t_z_zp = np.array([[0, -1,  0, -ZED_CAMERA_OFFSET], 
                       [0,  0, -1,                  0], 
                       [1,  0,  0,                  0], 
                       [0,  0,  0,                  1]])

    T_F_A1 = np.array([[ 0,  0, 1,    50.8975], 
                       [-1,  0, 0,   3.515833], 
                       [ 0, -1, 0,   1.518333], 
                       [ 0,  0, 0,          1]])


    T_F_A2 = np.array([[0, 0, 1, 50.8975], 
                       [-1, 0, 0, 9.015833], 
                       [0, -1, 0,  1.518333], 
                       [0, 0, 0, 1]])


    T_F_A3 = np.array([[ 0,  0, 1,   50.8975], 
                       [-1,  0, 0, 14.515833], 
                       [ 0, -1, 0,  1.518333], 
                       [ 0,  0, 0,         1]])


    T_F_A4 = np.array([[0, 0, 1,      53.08], 
                       [-1, 0, 0,    22.145], 
                       [0, -1, 0,  2.281667], 
                       [0, 0, 0,          1]])


    T_F_A5 = np.array([[0,  0, -1,    1.1875], 
                       [1,  0,  0,    22.145], 
                       [0, -1,  0,  2.281667], 
                       [0,  0,  0,         1]])


    T_F_A6 = np.array([[0,  0, -1,  3.370833], 
                       [1,  0,  0, 14.515833], 
                       [0, -1,  0,  1.518333], 
                       [0,  0,  0,         1]])

    T_F_A7 = np.array([[0,  0, -1,  3.370833], 
                       [1,  0,  0,  9.015833], 
                       [0, -1,  0,  1.518333], 
                       [0,  0,  0,         1]])

    T_F_A8 = np.array([[0,  0, -1,  3.370833], 
                       [1,  0,  0,  3.515833], 
                       [0, -1,  0,  1.518333], 
                       [0,  0,  0,         1]])