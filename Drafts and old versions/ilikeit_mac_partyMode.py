# USAGE
# python webcam.py --face cascades/haarcascade_frontalface_default.xml

# ********** NOAM'S PARAMETERS **********
showvideo = 1
camH = 640 * 2
camW = 360 * 2 
resizeTo = 400 * 2 # Value to resize to for processing
minValue = 30 # 30 by default (10 is good)
areaNumber = 0 #holds the surface total for all faces
FR = 32 # Frame Rat4
# rotateAngle = -90
rotateAngle = 0
TextString = "Dance like"
TextString2 = "no one"
TextString3 = "is watching"
#TextString = "I like it when you watch."
#TextString = "#iLikeItWhenYouWatch"
multiplier = 0.7

# SMOOTHING
numReadings = 6 #used to be 10
defaultNumber = 300 #base number for no faces (to not have zero)
readings = [0] * numReadings    # the readings from the analog input
readIndex = 0      	   # the index of the current reading
total = 0                # the running total
average = 0             # the average
delay = 1				# the delay between sending commands in seconds
notesPlayed = 0


# import the necessary packages
from pyimagesearch.facedetector import FaceDetector
from pyimagesearch import imutils
import argparse
import time
import cv2
import serial
import Tkinter
import os
import pty
import numpy as np


# ********** Serial **********
usbport = '/dev/cu.usbmodem1421' # Need to change based on what it shows when connected. 
ser = serial.Serial(usbport, 250000)

# # *** virtual FAKE serial device *** disable when arduino is connected
# master, slave = pty.openpty()
# s_name = os.ttyname(slave)

# ser = serial.Serial(s_name)


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
camera = cv2.VideoCapture(0)
# camera.set(cv2.CV_CAP_PROP_FRAME_WIDTH, 1280)

# camera.resolution = (camH, camW)
# camera.framerate = FR #32 by default, changed
# camera.vflip = True
# camera.hflip = True
# camera.rotation=rotateAngle
# rawCapture = PiRGBArray(camera, size=(camH, camW))

root = Tkinter.Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.destroy()

print("Screen Width: %s" % screenWidth)
print("Screen Height: %s" % screenHeight)

# if a video path was not supplied, grab the reference
# to the gray
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, load the video
else:
	camera = cv2.VideoCapture(args["video"])


# construct the face detector and allow the camera to warm
# up
fd = FaceDetector(args["face"])
time.sleep(0.1)
lastTime = time.time()

# send to 0

ser.write('0\n')


# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a
	# frame, then we have reached the end of the video
	if args.get("video") and not grabbed:
		break


	#Reset Surface Area: #DO I NEED THAT FOR MAC?

	areaNumber = 0;

	# grab the raw NumPy array representing the image - ONLY FOR PI? 
	# frame = f.array


	# resize the frame and convert it to grayscale
	frame = cv2.flip(frame,1)
	frameorig = frame
	frame = imutils.resize(frame, width = resizeTo)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	grayorig = cv2.cvtColor(frameorig, cv2.COLOR_BGR2GRAY)
	# gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# detect faces in the image and then clone the frame
	# so that we can draw on it
	faceRects = fd.detect(gray, scaleFactor = 1.11, minNeighbors = 5, minSize = (minValue, minValue))
	frameClone = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB) #	
	# frameClone = frame.copy() # (the original line)
	# frameClone = gray
	overlay = np.zeros((screenHeight,screenWidth,3), np.uint8) # EXP overlay maybe for rects on fullres? 


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
	# print("total is: %s " %total)

  	# // if we're at the end of the array...
  	if readIndex >= numReadings:
  		readIndex = 0

  	# // calculate the average:
  	average = total / numReadings;
	print("Average is: %s " % average)

	if resizeTo < 500:	
		if average >= 0:
			if average <= 100:
				ser.write('e1\n')
				print("playing B")
			elif average <= 200:
				ser.write('e\n')
				print("playing B")
			elif average <= 800:
				ser.write('b\n')
				print("playing G")
			elif average <= 2500:
				ser.write('d\n')
				print("playing D")
			elif average <= 5000:
				ser.write('A\n')
				print("playing A")
			elif average <= 7500:
				ser.write('e\n')
				print("playing all")
	elif resizeTo > 500:
		# if time.time() - lastTime >= delay:
			# if notesPlayed >= 4:
			# 	print("FULL CYCLE")
			# 	ser.write('f\n')
			# 	notesPlayed = 0
		if average >= 10:
			# notesPlayed += 1
			if average <= 1000*multiplier:
				try:
					ser.write('e1\n')
					print("playing E1")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 2500*multiplier:
				try:
					ser.write('b\n')
					print("playing B")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 6000*multiplier:
				try:
					ser.write('g\n')
					print("playing G")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 15000*multiplier:
				try:
					ser.write('d\n')
					print("playing D")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 20000*multiplier:
				try:
					ser.write('a\n')
					print("playing A")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 30000*multiplier:
				try:
					ser.write('e\n')
					print("playing E")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 300000*multiplier:
				try:
					ser.write('f\n')
					print("playing full")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
		elif average < 10:
			try:
				ser.write('0\n')
			except serial.SerialException as e:
				print("Serial Error, ignoring")
				ser.close()             # close port
				time.sleep(0.1)
				ser.open()
				# ser.write('blarg\n')
				# print ser.readline()
				# lastTime = time.time()




	# print(resizeTo)

	# show our detected faces, then clear the frame in
	# preparation for the next frame
	if showvideo == 1:
		frameClone = imutils.resize(frameClone, width = screenWidth, height=screenHeight)
		window_name = 'I LIKE IT WHEN YOU WATCH'
   		cv2.putText(frameClone, TextString, (100,160),cv2.FONT_HERSHEY_SIMPLEX, 5, (0,255,0),10)		
   		cv2.putText(frameClone, TextString2, (100,340),cv2.FONT_HERSHEY_SIMPLEX, 5, (0,255,0),10)		
   		cv2.putText(frameClone, TextString3, (100,520),cv2.FONT_HERSHEY_SIMPLEX, 5, (0,255,0),10)		
   		cv2.namedWindow(window_name, cv2.WINDOW_GUI_EXPANDED)
		cv2.moveWindow(window_name, -1, -1)
   		cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);
   		# cv2.setWindowProperty('I LIKE IT WHEN YOU WATCH', 0, 1);
		cv2.imshow(window_name, frameClone)
		# cv2.imshow("Face", frameClone) #original
	
	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		# send to 0
		ser.write('0\n')
		break

		
camera.release()
cv2.destroyAllWindows()
