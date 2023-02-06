import math
import numpy as np
from .constants import Constants


class PoseCalculator:
    def __init__(self) -> None:
        pass

    def translateZedPose(self, theta, point: np.ndarray):
        """Translates points relative to the pose of the zed 
           to pose of the robot
        Args:
            theta: turret angle from 0
            point: pose of the tag as [x, y, z].T

        Returns:
            translatedPose: pose of a tag relative to the robot
        """

        t_z_zp = np.array([[1, 0, 0,                           0], 
                           [0, 1, 0, Constants.ZED_CAMERA_OFFSET], 
                           [0, 0, 1,                           0], 
                           [0, 0, 0,                           1]])

        t_zp_r = np.array([[math.cos(theta), -math.sin(theta), 0,                    0], 
                           [math.sin(theta),  math.cos(theta), 0,                    0], 
                           [              0,                0, 1, Constants.ZED_HEIGHT], 
                           [              0,                0, 0,                    1]])

        t_z_r = np.matmul(t_z_zp,  t_zp_r)

        translatedPose = np.add(np.matmul(t_z_r[0:3, 0:3], point), t_z_r[0:3, -1])
        return translatedPose

    def getRobotPose(self, tagID):
        # TODO translate tagID to field positions
        if tagID == 1:
            pass
        elif tagID == 2:
            pass
        elif tagID == 3:
            pass
        elif tagID == 4:
            pass
        elif tagID == 5:
            pass
        elif tagID == 6:
            pass
        elif tagID == 7:
            pass
        elif tagID == 8:
            pass
        else:
            pass
