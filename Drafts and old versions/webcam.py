# USAGE
# python webcam.py --face cascades/haarcascade_frontalface_default.xml

# ********** NOAM'S PARAMETERS **********
showvideo = 1
camH = 640 #* 4
camW = 380 #* 4 #640,480 by default
resizeTo = 300 #* 2 # Value to resize to for processing
minValue = 10 # 30 by default
areaNumber = 0 #holds the surface total for all faces
FR = 32 # Frame Rate

# SMOOTHING
numReadings = 10
defaultNumber = 300 #base number for no faces (to not have zero)
readings = [0] * numReadings    # the readings from the analog input
readIndex = 0      	   # the index of the current reading
total = 0                # the running total
average = 0             # the average


# import the necessary packages
from pyimagesearch.facedetector import FaceDetector
from pyimagesearch import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required = True,
	help = "path to where the face cascade resides")
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
ap.add_argument("-d", "--display",
	help = "display on or off")
args = vars(ap.parse_args())

# initialize the camera and grab a reference to the raw camera
# capture
camera = PiCamera()
camera.resolution = (camH, camW)
camera.framerate = FR #32 by default, changed
# camera.vflip = True
# camera.hflip = True
rawCapture = PiRGBArray(camera, size=(camH, camW))


# construct the face detector and allow the camera to warm
# up
fd = FaceDetector(args["face"])
time.sleep(0.1)

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	#Reset Surface Area:

	areaNumber = 0;

	# grab the raw NumPy array representing the image
	frame = f.array


	# resize the frame and convert it to grayscale
	frame = imutils.resize(frame, width = resizeTo)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# detect faces in the image and then clone the frame
	# so that we can draw on it
	faceRects = fd.detect(gray, scaleFactor = 1.11, minNeighbors = 5,
		minSize = (minValue, minValue))
	frameClone = frame.copy()




	# loop over the face bounding boxes and draw them
	for (fX, fY, fW, fH) in faceRects:
		cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 2)
		fWi = int(fW)
		fHi = int(fH)
		tempArea = fWi * fHi
		# print("Face area Temp is %s  " % tempArea)
		areaNumber = areaNumber + tempArea
		# print("Face Width %s  " % fW)
		# print("Face Height %s  " % fH)

        # Print number of faces
	faces = len(faceRects)
	#print("Total faces is %s  " % faces)
	print("Total face Area is %s " % areaNumber)

	# ******* SMOOTHING ********
	# //subtract last reading
	total = (total - readings[readIndex])
	
 	# // read from the sensor:
  	readings[readIndex] = int(areaNumber)
  	#// add the reading to the total:

  	total = (total + readings[readIndex])

  	# // advance to the next position in the array:
  	readIndex = readIndex + 1

  	# // print total:
	print("total is: %s " %total)

  	# // if we're at the end of the array...
  	if readIndex >= numReadings:
  		readIndex = 0

  	# // calculate the average:
  	average = total / numReadings;
	#print("Average is: %s " %average)



	# show our detected faces, then clear the frame in
	# preparation for the next frame
	if showvideo == 1:
		cv2.imshow("Face", frameClone)
	
	rawCapture.truncate(0)

	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
