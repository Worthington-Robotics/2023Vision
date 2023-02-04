import math
import numpy as np
from .constants import Constants


class PoseCalculator:
    def __init__(self) -> None:
        pass

    def translateZedPose(self, theta, points: np.ndarray):
        """Translates points relative to the pose of the zed 
           to pose of the robot
        Args:
            theta: turret angle from 0
            point: pose of the tag as [x, y, z].T

        Returns:
            translatedPose: pose of a tag relative to the robot
        """
        rot_rz = np.array([[math.cos(theta), -math.sin(theta), 0],
                           [math.sin(theta), math.cos(theta),  0],
                           [0,               0,                1]])
        p_rz = np.array([0, 0, Constants.ZED_HEIGHT]).T
        translatedPose = np.add(np.matmul(rot_rz, points), p_rz)

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
