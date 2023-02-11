from pyzed import sl
from pupil_apriltags import Detector
from vision import VisionProcessor, Dispatcher, Constants, PoseCalculator
import time


def main():
    zed = sl.Camera()
    cameraPose = sl.Pose()  
    runtime = sl.RuntimeParameters()

    detector = Detector(families=Constants.TAG_FAMILY)

    dispatcher = Dispatcher(4145)

    poseCalculator = PoseCalculator()

    visionProcessor = VisionProcessor(
        detector=detector, zed=zed, dispatcher=dispatcher, poseCalculator=poseCalculator, cameraPose=cameraPose)
    visionProcessor.initializeZed()
    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            tracking_state = zed.get_position(cameraPose)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:
                visionProcessor.processVision()

if __name__ == "__main__":
    main()
