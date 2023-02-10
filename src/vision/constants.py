from pyzed import sl
import math
import numpy as np


class Constants:
    ZED_HEIGHT = 5

    ZED_INIT_PARAMS = sl.InitParameters()
    # Use HD720 video mode (default fps: 60)
    ZED_INIT_PARAMS.camera_resolution = sl.RESOLUTION.VGA
    # Use a right-handed Z-up coordinate system
    ZED_INIT_PARAMS.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Z_UP
    ZED_INIT_PARAMS.coordinate_units = sl.UNIT.FOOT  # Set units in feet

    # Apriltag constants
    TAG_FAMILY = "tag16h5"
    # In inches
    TAG_SIZE = 6.5

    ZED_CAMERA_OFFSET = .3938

    T_F_A1 = np.array([[-1, 0, 0, 50.8975], 
                        [0, 1, 0, 3.515833], 
                        [0, 0, 0,  1.518333], 
                        [0, 0, 0, 1]])

    R_F_A1 = np.array([[math.cos(180), -math.sin(180), 0,         0], 
                       [math.sin(180),  math.cos(180), 0,         0], 
                       [            0,              0, 1,  3.515833], 
                       [            0,              0, 0,         1]])

    T_F_A2 = np.array([[-1, 0, 0, 50.8975], 
                        [0, 1, 0, 9.015833], 
                        [0, 0, 0,  1.518333], 
                        [0, 0, 0, 1]])

    R_F_A2 = np.array([[math.cos(180), -math.sin(180), 0,         0], 
                       [math.sin(180),  math.cos(180), 0,         0], 
                       [            0,              0, 1,  9.015833], 
                       [            0,              0, 0,         1]])

    T_F_A3 = np.array([[-1, 0, 0, 50.8975], 
                        [0, 1, 0, 14.515833], 
                        [0, 0, 0,  1.518333], 
                        [0, 0, 0, 1]])

    R_F_A3 = np.array([[math.cos(180), -math.sin(180), 0,         0], 
                       [math.sin(180),  math.cos(180), 0,         0], 
                       [            0,              0, 1, 14.515833], 
                       [            0,              0, 0,         1]])   

    T_F_A4 = np.array([[-1, 0, 0, 53.08], 
                        [0, 1, 0, 22.145], 
                        [0, 0, 0,  2.281667], 
                        [0, 0, 0, 1]])

    R_F_A4 = np.array([[math.cos(180), -math.sin(180), 0,         0], 
                       [math.sin(180),  math.cos(180), 0,         0], 
                       [            0,              0, 1,  22.145], 
                       [            0,              0, 0,         1]])

    T_F_A5 = np.array([[1, 0, 0, 1.1875], 
                        [0, 1, 0, 22.145], 
                        [0, 0, 0,  2.281667], 
                        [0, 0, 0, 1]])

    R_F_A5 = np.array([[math.cos(0), -math.sin(0), 0,         0], 
                       [math.sin(0),  math.cos(0), 0,         0], 
                       [          0,            0, 1,    22.145], 
                       [          0,            0, 0,         1]])

    T_F_A6 = np.array([[1, 0, 0, 3.370833], 
                        [0, 1, 0, 14.515833], 
                        [0, 0, 0,  1.518333], 
                        [0, 0, 0, 1]])
    
    R_F_A6 = np.array([[math.cos(0), -math.sin(0), 0,         0], 
                       [math.sin(0),  math.cos(0), 0,         0], 
                       [          0,            0, 1, 14.515833], 
                       [          0,            0, 0,         1]])

    T_F_A7 = np.array([[1, 0, 0, 3.370833], 
                        [0, 1, 0, 9.015833], 
                        [0, 0, 0,  1.518333], 
                        [0, 0, 0, 1]])
    
    R_F_A7 = np.array([[math.cos(0), -math.sin(0), 0,         0], 
                       [math.sin(0),  math.cos(0), 0,         0], 
                       [          0,            0, 1,  9.015833], 
                       [          0,            0, 0,         1]])

    T_F_A8 = np.array([[1, 0, 0, 3.370833], 
                        [0, 1, 0, 3.515833], 
                        [0, 0, 0,  1.518333], 
                        [0, 0, 0, 1]])

    R_F_A8 = np.array([[math.cos(0), -math.sin(0), 0,         0], 
                       [math.sin(0),  math.cos(0), 0,         0], 
                       [          0,            0, 1,  3.515833], 
                       [          0,            0, 0,         1]])