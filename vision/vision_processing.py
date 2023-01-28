import pyzed.sl as sl
from pupil_apriltags import Detector
import cv2
from vision.constants import Constants
from vision.zed_params import init_calibration_params


class VisionProcesser():
    def __init__(self, tag_detector: Detector, zed: sl.Camera):
        self.zed = zed
        self.detector = tag_detector

        
    def track_position(self, camera_pose, zed):
        rotation = camera_pose.get_rotation_vector()
        py_translation = sl.Translation()
        translation = camera_pose.get_translation(py_translation)
        text_rotation = str((round(rotation[0], 2), round(rotation[1], 2), round(rotation[2], 2)))
        text_translation = str((round(translation.get()[0], 2), round(translation.get()[1], 2), round(translation.get()[2], 2)))
        pose_data = camera_pose.pose_data(sl.Transform())
        tx = round(camera_pose.get_translation(py_translation).get()[0], 3)
        ty = round(camera_pose.get_translation(py_translation).get()[1], 3)
        tz = round(camera_pose.get_translation(py_translation).get()[2], 3)

        return [tx, ty, tz]

    def april_tag_tracking(self):
        calibration_params = init_calibration_params(self.zed)
        image = sl.Mat()
        self.zed.retrieve_image(image, sl.VIEW.LEFT)
        image_data = image.get_data()
        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGRA2GRAY)
        tag_pose = self.detector.detect(img=image_data, estimate_tag_pose=True, camera_params=(calibration_params.left_cam.fx,  calibration_params.left_cam.fy, calibration_params.left_cam.cx, calibration_params.left_cam.cy), tag_size=Constants.TAG_SIZE)
        return tag_pose
    
