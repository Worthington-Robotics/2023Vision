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

import math
import numpy as np
from .constants import Constants


class PoseCalculator:
    def __init__(self) -> None:
        pass
    
    def invert(self, m):
        """This function finds the inverse of a given matrix
        Args:
            m: invertable matrix
        """
        m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33 = np.ravel(m)
        a2323 = m22 * m33 - m23 * m32
        a1323 = m21 * m33 - m23 * m31
        a1223 = m21 * m32 - m22 * m31
        a0323 = m20 * m33 - m23 * m30
        a0223 = m20 * m32 - m22 * m30
        a0123 = m20 * m31 - m21 * m30
        a2313 = m12 * m33 - m13 * m32
        a1313 = m11 * m33 - m13 * m31
        a1213 = m11 * m32 - m12 * m31
        a2312 = m12 * m23 - m13 * m22
        a1312 = m11 * m23 - m13 * m21
        a1212 = m11 * m22 - m12 * m21
        a0313 = m10 * m33 - m13 * m30
        a0213 = m10 * m32 - m12 * m30
        a0312 = m10 * m23 - m13 * m20
        a0212 = m10 * m22 - m12 * m20
        a0113 = m10 * m31 - m11 * m30
        a0112 = m10 * m21 - m11 * m20

        det = m00 * (m11 * a2323 - m12 * a1323 + m13 * a1223) \
            - m01 * (m10 * a2323 - m12 * a0323 + m13 * a0223) \
            + m02 * (m10 * a1323 - m11 * a0323 + m13 * a0123) \
            - m03 * (m10 * a1223 - m11 * a0223 + m12 * a0123)
        det = 1 / det

        return np.array([ \
            det *  (m11 * a2323 - m12 * a1323 + m13 * a1223), \
            det * -(m01 * a2323 - m02 * a1323 + m03 * a1223), \
            det *  (m01 * a2313 - m02 * a1313 + m03 * a1213), \
            det * -(m01 * a2312 - m02 * a1312 + m03 * a1212), \
            det * -(m10 * a2323 - m12 * a0323 + m13 * a0223), \
            det *  (m00 * a2323 - m02 * a0323 + m03 * a0223), \
            det * -(m00 * a2313 - m02 * a0313 + m03 * a0213), \
            det *  (m00 * a2312 - m02 * a0312 + m03 * a0212), \
            det *  (m10 * a1323 - m11 * a0323 + m13 * a0123), \
            det * -(m00 * a1323 - m01 * a0323 + m03 * a0123), \
            det *  (m00 * a1313 - m01 * a0313 + m03 * a0113), \
            det * -(m00 * a1312 - m01 * a0312 + m03 * a0112), \
            det * -(m10 * a1223 - m11 * a0223 + m12 * a0123), \
            det *  (m00 * a1223 - m01 * a0223 + m02 * a0123), \
            det * -(m00 * a1213 - m01 * a0213 + m02 * a0113), \
            det *  (m00 * a1212 - m01 * a0212 + m02 * a0112)  \
        ]).reshape(4, 4)


    def get_zed_to_robot(self, theta):
        # t_zp_r = np.array([[0 , -math.sin(math.radians(theta)),  math.cos(math.radians(theta)),                    0], 
        #                    [1, 0, 0, Constants.ZED_HEIGHT], 
        #                    [0, 0,  -math.sin(math.radians(theta)),                    0],
        #                    [                            0,                             0,  0,                    1]])

        t_zp_r = np.array([[1 , 0,  0,                    0], 
                           [0, 1, 0, Constants.ZED_HEIGHT], 
                           [0, 0,  1,                    0],
                           [                            0,                             0,  0,                    1]])
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

        translatedPose = np.matmul(Constants.t_z_zp[0:3, 0:3], point)
        return translatedPose

    def getRobotTranslation(self, tagID, t_z_a, theta):
        """Gets the robot's position as coordinates on the field
        Args:
            tagID: the id of the apriltag detected
            t_z_a: the matrix provided from the zed. This matrix
            represents the the location of the apriltag relative
            to the zed
            theta: turret angle from zero
        """
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

        T_f_z = np.matmul(t_f_a, self.invert(t_z_a))
        # print(self.get_zed_to_robot(theta))
        print(np.matmul(T_f_z, Constants.t_z_zp))
        T_f_r = np.matmul(np.matmul(np.matmul(t_f_a, self.invert(t_z_a)), Constants.t_z_zp), self.get_zed_to_robot(theta))
        return T_f_r
