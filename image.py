# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
from detect_color import ColorLabeler

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the image file")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, and blur it
image = cv2.imread(args["image"])
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
blurred = cv2.GaussianBlur(hsv, (11, 11), 0)



# threshold the image to reveal light regions in the
# blurred image
lower_green = np.array([55,160,70])
upper_green = np.array([75,255,255])
thresh = cv2.inRange(blurred, lower_green, upper_green)

# perform a series of erosions and dilations to remove
# any small blobs of noise from the thresholded image
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)

# perform a connected component analysis on the thresholded
# image, then initialize a mask to store only the "large"
# components
labels = measure.label(thresh, neighbors=8, background=0)
mask = np.zeros(thresh.shape, dtype="uint8")


##Debugging!!!
#cv2.imwrite("blurreddGray.png", blurred)
#cv2.imwrite("blurredLAB.png", lab)
#cv2.imwrite("threshed.png", thresh)

# loop over the unique components
for label in np.unique(labels):
	# if this is the background label, ignore it
	if label == 0:
		continue

	# otherwise, construct the label mask and count the
	# number of pixels
	labelMask = np.zeros(thresh.shape, dtype="uint8")
	labelMask[labels == label] = 255
	numPixels = cv2.countNonZero(labelMask)

	# if the number of pixels in the component is sufficiently
	# large, then add it to our mask of "large blobs"
	if numPixels > 300:
		mask = cv2.add(mask, labelMask)

# find the contours in the mask, then sort them from left to
# right
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cnts = contours.sort_contours(cnts)[0]

results = []
# loop over the contours
for (i, c) in enumerate(cnts):
	hull = cv2.convexHull(c)
	a2 = cv2.approxPolyDP(hull, 0.01*cv2.arcLength(hull, True), True)
	results.append(a2)


dst = np.zeros(shape=image.shape, dtype=image.dtype)
cv2.drawContours(dst, results, -1, (0, 0, 255), 1)
cv2.imwrite("Rect.png",dst)

cv2.drawContours(image, results, -1, (0, 0, 255), 1)


# show the output image
#cv2.imwrite("finished.png", image)


##Debugging!!!
#cv2.imwrite("blurredGray.png", blurred)
#cv2.imwrite("blurredLAB.png", lab)
##cv2.imwrite("threshed.png", thresh)
