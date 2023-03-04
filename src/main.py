from pyzed import sl
from dt_apriltags import Detector
from vision import VisionProcessor, Dispatcher, Constants, PoseCalculator
import time


def main():
    zed = sl.Camera()
    cameraPose = sl.Pose()  
    runtime = sl.RuntimeParameters()

    detector = Detector(searchpath=['apriltags'],
                       families=Constants.TAG_FAMILY,
                       nthreads=5,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

    dispatcher = Dispatcher(4145)

    poseCalculator = PoseCalculator()

    visionProcessor = VisionProcessor(
        detector=detector, zed=zed, dispatcher=dispatcher, poseCalculator=poseCalculator, cameraPose=cameraPose)
        
    visionProcessor.initializeZed()
    # translation_left_to_center = zed.get_camera_information().calibration_parameters.T[0]

    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            tracking_state = zed.get_position(cameraPose)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:
                visionProcessor.processVision()

if __name__ == "__main__":
    main()
