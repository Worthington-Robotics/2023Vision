from pyzed import sl
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

    T_F_A1 = np.array([[-1, 0, 0, 610.77/12], 
                        [0, 1, 0, 42.19/12], 
                        [0, 0, 0,  18.22/12], 
                        [0, 0, 0, 1]])

