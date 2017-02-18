import numpy
import cv2






def main() :
	cv2.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
	camera_index = 0
	capture = cv.CaptureFromCAM(camera_index)

	while True:
		image=repeat()
		print('repeated')




def repeat():
    global capture #declare as globals since we are assigning to them now
    global camera_index
    frame = cv.QueryFrame(capture)
    cv2.ShowImage("w1", frame)
    time.sleep(10)
    #warning!! the camera index, might not work if it's the wrong
    #device
    capture = cv.CaptureFromCAM(camera_index)
    return capture

main()
