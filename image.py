# import the necessary packages
from imutils import contours
from skimage import measure
from webcamvideostream import WebcamVideoStream as wvs
from networktablesstream import NetworkTablesStream as nts

import numpy as np
import argparse
import imutils
import cv2
import math

image_width = 1280
image_height = 960
image_cX = 640
image_cY = 480
horiz_fov = 60
vert_fov = 30
target_width = 10.25
horiz_focal_length = image_width/(2*math.tan(math.radians(horiz_fov/2)))
vert_focal_length = image_height/(2*math.tan(math.radians(vert_fov/2)))
dist_focal_length = 72

stream = wvs(0).start()
table = nts('roborio-6072-frc.local').start()
#import calculations as calc

def threshold_image(blurred_image=""):
	#lower_green = np.array([55, 160, 70])
	lower_green = np.array([55, 160, 65])
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

def contour_coordinates(contours=""):
	results = []
	# loop over the contours
	for (i, c) in enumerate(contours):
		rect = cv2.minAreaRect(c)
		centerX, centerY = rect[0]
		#width, height = rect[1]
		#if height > width:
		#print centerX
		#print centerY
		results.append(centerX)
		results.append(centerY)
	return results

def start_img_processing(image_path=""):
	
	#stream = wvs(0).start()
	#image = stream.read()

	# load image with opencv
	while true:	
		image = stream.read()
		#height, width = image.shape[:2]	
		#print height
		#print width
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		blurred = cv2.GaussianBlur(hsv, (11, 11), 0)
		# convert color space
		#lab = cv2.cvtColor(cv2.GaussianBlur(image, (5, 5), 0), cv2.COLOR_BGR2LAB)

		thresh = threshold_image(blurred_image=blurred)
		mask = component_analysis(thresh=thresh)

		cnts = get_contours(mask=mask)

		results = contour_approximation(contours=cnts)

		if len(results) == 6:
			coordinates = contour_coordinates(contours=results)	
	
			angle = get_angle(coordinates=coordinates)
			distance = distance_to_target()
			table.send_data(angle,0,distance)
			table.send_viewability(true)
		else:
			table.send_viewability(false)
		#dst = np.zeros(shape=image.shape, dtype=image.dtype)
		#cv2.drawContours(dst, results, -1, (0, 0, 255), 1)
	
		#cv2.imwrite("Rect.png", dst)

		#cv2.drawContours(image, results, -1, (0, 0, 255), 5)

		#drawing(unnecessary)
		#target_cX = (coordinates[0]+coordinates[2])/2
		#target_cY = (coordinates[1]+coordinates[3])/2
		#target_cX = int(target_cX)
		#target_cY = int(target_cY)
		#l1 = (target_cX, 1)
		#l2 = (target_cX, 959)
		#cv2.line(image, l1, l2, (0,255,255), 1)
		#l1 = (1, target_cY)
		#l2 = (1279, target_cY)
		#cv2.line(image, l1, l2, (0,255,255), 1)

		# show the output image
		#cv2.imwrite("finished.png", image)

def get_angle(coordinates=""):

	target_cX = (coordinates[0]+coordinates[2])/2
	target_cY = (coordinates[1]+coordinates[3])/2
	
	horiz_angle = math.degrees(math.atan((target_cX-image_cX)/horiz_focal_length))
	vert_angle = math.degrees(math.atan((target_cY-image_cY)/vert_focal_length))
	#print horiz_angle
	#print vert_angle
	return horiz_angle

def get_distance(angle=""):
	height = -14.5
	temp = (math.tan(math.radians(angle)) ** -1) * height
	print temp


def distance_to_camera(coordinates=""):
	# compute and return the distance from the maker to the camera
	perWidth = coordinates[0]-coordinates[2]
	return (target_width * dist_focal_length) / perWidth

# known distance / known width (need to make calculation once)
#focalLength = (dst[1][0] * 48)/6
#distance = calc.camera_distance(width=6, focal_length=focalLength, pixel_width=dst[1][0])

if __name__ == "__main__":
	start_img_processing(image_path="input9.jpg")
