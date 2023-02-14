import math
import numpy as np
from .constants import Constants


class PoseCalculator:
    def __init__(self) -> None:
        pass
    

    def get_zed_to_robot(self, theta):
        t_zp_r = np.array([[math.cos(theta), -math.sin(theta), 0,                     0], 
                           [math.sin(theta),  math.cos(theta), 0,                     0], 
                           [              0,                0, 1, -Constants.ZED_HEIGHT], 
                           [              0,                0, 0,                     1]])
        return t_zp_r

    def translateZedPose(self, theta, point: np.ndarray):
        """Translates points relative to the pose of the zed 
           to pose of the robot
        Args:
            theta: turret angle from 0
            point: pose of the tag as [x, y, z].T

        Returns:
            translatedPose: pose of a tag relative to the robot
        """

        t_z_r = np.matmul(Constants.t_z_zp,  self.get_zed_to_robot(theta))

        translatedPose = np.add(np.matmul(t_z_r[0:3, 0:3], point), t_z_r[0:3, -1])
        return translatedPose

    def getRobotTranslation(self, tagID, t_z_a, theta):
        # TODO translate tagID to field positions
        if tagID == 1:
            t_f_a = Constants.T_F_A1
        elif tagID == 2:
            t_f_a = Constants.T_F_A2
        elif tagID == 3:
            t_f_a = Constants.T_F_A3
        elif tagID == 4:
            t_f_a = Constants.T_F_A4
        elif tagID == 5:
            t_f_a = Constants.T_F_A5
        elif tagID == 6:
            t_f_a = Constants.T_F_A6
        elif tagID == 7:  
            t_f_a = Constants.T_F_A7
        elif tagID == 8:
            t_f_a = Constants.T_F_A8
        else:
            return None
        T_f_s = np.matmul(np.matmul(np.matmul(t_f_a, np.linalg.inv(t_z_a)), Constants.t_z_zp), self.get_zed_to_robot(theta))
        return T_f_s
