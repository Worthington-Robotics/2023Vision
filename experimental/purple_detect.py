import cv2
import numpy as np

#hopefully this script will be able to detect the color purple

# Load image
img = cv2.imread('image.jpg')

# Convert image to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define lower and upper bounds for purple color in HSV color space
lower_purple = np.array([125, 50, 50])
upper_purple = np.array([175, 255, 255])

# Threshold the image to get a binary mask
mask = cv2.inRange(hsv, lower_purple, upper_purple)

# Set up SimpleBlobDetector parameters
params = cv2.SimpleBlobDetector_Params()

# Filter by Area.
params.filterByArea = True
params.minArea = 100

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs
keypoints = detector.detect(mask)

# Draw detected blobs as red circles
img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show image with detected blobs
cv2.imshow("Blob Detection", img_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()
