import pyzed.sl as sl

def init_zed_params():

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.VGA # Use HD720 video mode (default fps: 60)
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP # Use a right-handed Y-up coordinate system
    init_params.coordinate_units = sl.UNIT.METER # Set units in meters

    return init_params

def init_calibration_params(zed: sl.Camera):
    calibration_params = zed.get_camera_information().camera_configuration.calibration_parameters
    return calibration_params

def init_tracking_params():
    tracking_params = sl.PositionalTrackingParameters()
    return tracking_params
