# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

#import calculations as calc

def threshold_image(blurred_image=""):
	lower_green = np.array([55, 160, 70])
	upper_green = np.array([75, 255, 255])

	result = cv2.inRange(blurred_image, lower_green, upper_green)

	return result

def component_analysis(thresh=""):

	# remove noise
	result = cv2.erode(thresh, None, iterations=2)
	result = cv2.dilate(thresh, None, iterations=4)

	# perform a connected component analysis on the thresholded
	# initialize a mask to store only the "large" components

	labels = measure.label(thresh, neighbors=8, background=0)
	mask = np.zeros(thresh.shape, dtype="uint8")

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

	return mask

def get_contours(mask=""):
	# find the contours in the mask, then sort them from left to right

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
							cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	cnts = contours.sort_contours(cnts)[0]

	return cnts

def contour_approximation(contours=""):
	results = []
	# loop over the contours
	for (i, c) in enumerate(contours):
		hull = cv2.convexHull(c)
		a2 = cv2.approxPolyDP(hull, 0.01 * cv2.arcLength(hull, True), True)
		results.append(a2)

	return results

def start_img_processing(image_path=""):

	# load image with opencv
	image = cv2.imread(image_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	blurred = cv2.GaussianBlur(gray, (11, 11), 0)
	# convert color space
	lab = cv2.cvtColor(cv2.GaussianBlur(image, (5, 5), 0), cv2.COLOR_BGR2LAB)

	thresh = threshold_image(blurred_image=blurred)
	mask = component_analysis(thresh=thresh)

	cnts = get_contours(mask=mask)

	results = contour_approximation(contours=cnts)

	dst = np.zeros(shape=image.shape, dtype=image.dtype)
	cv2.drawContours(dst, results, -1, (0, 0, 255), 1)
	cv2.imwrite("Rect.png", dst)

	cv2.drawContours(image, results, -1, (0, 0, 255), 1)

	# show the output image
	cv2.imwrite("finished.png", image)



# known distance / known width (need to make calculation once)
#focalLength = (dst[1][0] * 48)/6
#distance = calc.camera_distance(width=6, focal_length=focalLength, pixel_width=dst[1][0])


if __name__ == "__main__":
	start_img_processing(image_path="input1.jpg")
