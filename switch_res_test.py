import sys
import pyzed.sl as sl
import cv2
import sys
import time
import numpy
from dt_apriltags import Detector

if __name__ == "__main__":

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.VGA # Use HD720 video mode (default fps: 60)
    init_params.camera_fps = 100
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP # Use a right-handed Y-up coordinate system
    init_params.coordinate_units = sl.UNIT.METER # Set units in meters
                                 
    # If applicable, use the SVO given as parameter
    # Otherwise use ZED live stream
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        print("Using SVO file: {0}".format(filepath))
        init_params.set_from_svo_file(filepath)

    zed = sl.Camera()
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    tracking_params = sl.PositionalTrackingParameters()
    zed.enable_positional_tracking(tracking_params)

    runtime = sl.RuntimeParameters()
    camera_pose = sl.Pose()

    camera_info = zed.get_camera_information()
    calibration_params = zed.get_camera_information().camera_configuration.calibration_parameters
    focal_left_x = calibration_params.left_cam.fx
    focal_left_y = calibration_params.left_cam.fy
    center_left_x = calibration_params.left_cam.cx
    center_left_y = calibration_params.left_cam.cy
    # Create OpenGL viewer
    #viewer = gl.GLViewer()
    # viewer.init(camera_info.camera_model)

    
    pose_data = sl.Transform()

    automous = True
    start_time = time.time()
    teleop = True

    keyPress = None

    text_translation = ""
    text_rotation = ""
    detect = Detector(searchpath=['apriltags'],
                       families='tag16h5',
                       nthreads=4,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
    while keyPress != ord('q'):
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            tracking_state = zed.get_position(camera_pose)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:
                #get april tag location
                image = sl.Mat()
                zed.retrieve_image(image, sl.VIEW.LEFT)
                image_data = image.get_data()
                cv2.imshow("img", image_data)
                keyPress = cv2.waitKey(5)
                image_data = cv2.cvtColor(image_data, cv2.COLOR_BGRA2GRAY)
                tag_pose = detect.detect(img=image_data, estimate_tag_pose=True, camera_params=(focal_left_x,  focal_left_y, center_left_x, center_left_y), tag_size=0.1524)
                #positional tracking
                if tag_pose:
                    for detection in tag_pose:
                        if detection.hamming == 0:
                            print(f"Pose_T: {detection.pose_t}")
            # viewer.updateData(pose_data, text_translation, text_rotation, tracking_state)
    print("Closing ZED")
    start_time = time.time()
    zed.close()
    init_params.camera_resolution = sl.RESOLUTION.HD720 # Use HD720 video mode (default fps: 60)
    zed.open(init_params)
    print(f"Took {time.time() - start_time}s to open, change res")
    zed.close()
    
  #62 in 1.57m Z
  #40 in 1.016m X
  #25 in .635m Y

  # Z is forwards,back X is Left,right Y is Up down

            
            
            
