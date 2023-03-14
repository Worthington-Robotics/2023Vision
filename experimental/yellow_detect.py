#hopefully this scipt will be able to detect anything that is yellow.
import cv2
import numpy as np
# Load image
img = cv2.imread('image.jpg')

# Convert image to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define lower and upper bounds for yellow color in HSV color space
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])


# Threshold the image to get a binary mask
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

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
