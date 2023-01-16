import pyzed.sl as sl
from vision.zed_params import *

def zed_init():
    zed = sl.Camera()
    zed_params = init_zed_params()
    tracking_params = init_tracking_params()
    
    status = zed.open(zed_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()
    zed.enable_positional_tracking(tracking_params)
    return zed
     
