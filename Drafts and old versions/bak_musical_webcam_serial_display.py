# USAGE
# python webcam.py --face cascades/haarcascade_frontalface_default.xml

# ********** NOAM'S PARAMETERS **********
showvideo = 1
camH = 640 #* 2
camW = 514 #* 2 #640,480 by default
resizeTo = 300 * 2 # Value to resize to for processing
minValue = 10 # 30 by default (10 is good)
areaNumber = 0 #holds the surface total for all faces
FR = 32 # Frame Rate
# rotateAngle = -90
rotateAngle = 0
#TextString = "I like it when you watch."
TextString = "#iLlikeItWhenYouWatch"

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
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import time
import cv2
import serial
import Tkinter


# ********** Serial **********
usbport = '/dev/ttyACM0'
ser = serial.Serial(usbport, 250000)


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
camera.hflip = True
camera.rotation=rotateAngle
rawCapture = PiRGBArray(camera, size=(camH, camW))

root = Tkinter.Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.destroy()

print("Screen Width: %s" % screenWidth)
print("Screen Height: %s" % screenHeight)



# construct the face detector and allow the camera to warm
# up
fd = FaceDetector(args["face"])
time.sleep(0.1)
lastTime = time.time()

# send to 0
ser.write('0\n')
# print ser.readline()

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
	faceRects = fd.detect(gray, scaleFactor = 1.11, minNeighbors = 5, minSize = (minValue, minValue))
	frameClone = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)


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
			if average <= 1000:
				try:
					ser.write('e1\n')
					print("playing E1")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 2500:
				try:
					ser.write('b\n')
					print("playing B")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 6000:
				try:
					ser.write('g\n')
					print("playing G")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 15000:
				try:
					ser.write('d\n')
					print("playing D")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 20000:
				try:
					ser.write('a\n')
					print("playing A")
				except serial.SerialException as e:
					print("Serial Error, ignoring")
					ser.close()             # close port
					time.sleep(0.1)
					ser.open()
			elif average <= 33000:
				try:
					ser.write('e\n')
					print("playing E")
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
		# frameClone = imutils.resize(frameClone, width = screenWidth)
   		cv2.putText(frameClone, TextString, (5,460),cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0,255,0),2)		
   		cv2.namedWindow('I LIKE IT WHEN YOU WATCH', cv2.WINDOW_NORMAL)
   		cv2.setWindowProperty('I LIKE IT WHEN YOU WATCH', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);
		cv2.imshow('I LIKE IT WHEN YOU WATCH', frameClone)
	
	rawCapture.truncate(0)

	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		# send to 0
		ser.write('0\n')
		break
