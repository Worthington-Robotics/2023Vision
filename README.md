# 2023Vision

Vision projects for the 2023-2024 summer.

Installation:  
- Use `pip install -r ./setup/requirements.txt` to automatically install all of the dependencies above.

Dependencies:
- OpenCV `pip install opencv-contrib-python`, build on version 4.8.0.74
- Robot Py `pip install robotpy`
- Python NetworkTables `pip install pyntcore`

Description:  
This code uses OpenCV's built in ArUco library for detecting AprilTags. This was chosen over other libraries due to its flexibility and customization abilities.  
The board.jpg is the ChArUco board that is used to calibrate the camera. The Checker width is 24mm, and the Marker width is 19mm. This is crucial to the calibration of the camera. It is also crucial to keep it flat while calibrating. RobotPy/PyNtCore are used for NetworkTables 4.0, as well as bringing WPI types to our code. [Here](https://github.com/wpilibsuite/allwpilib/blob/main/apriltag/src/main/native/resources/edu/wpi/first/apriltag/2023-chargedup.json) is a link to the current field layout as a .json file.