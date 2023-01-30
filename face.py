# Selfie taking assistance for blind people
import cv2
import numpy as np
import sched, time
import threading
from datetime import datetime
import speech_recognition as sr
import pyttsx3 as p3
import pyaudio
import time
import os

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def txt_to_speech(phrase):
	computer = p3.init()
	computer.say(phrase)
	computer.runAndWait()


def command_menu():
	computer = p3.init()
	r = sr.Recognizer()
	while True:
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source, duration=2)
			computer.say("Specify a position your face should appear in the selfie, or ask for a list of positions by simply stating list. Speak now!")
			computer.runAndWait()
			audio = r.listen(source)
		try:
			quad = r.recognize_google(audio);
			quad = str.lower(quad)
			if quad == "list":
				computer.say("The list options are: top left, top right, bottom left, and bottom right")
				computer.runAndWait()
			elif quad in {"top left", "top right", "bottom left", "bottom right"}:
				computer.say("Selected " + quad + ".")
				computer.runAndWait()
				break
			else:
				computer.say("Could not understand audio.")
				computer.runAndWait()

		except sr.UnknownValueError:
			computer.say("Could not understand audio.")
		computer.runAndWait()
	return quad



def find_face(frame, bound_rect, no_face_flag):

	grey_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	all_face_coords = face_cascade.detectMultiScale(grey_frame, 1.2, 5) # detect the face, return coordinates, may have more than one face
	move_right = False
	move_up = False
	move_left = False
	move_down = False

	if all_face_coords != ():
		face_coords = all_face_coords [0] # use only one face
		(x1,y1,x2,y2) = bound_rect
		(x, y, w, h) = face_coords

		if ((x1 < x < x2 and y1 < y < y2) or # upper left corner of face
				(x1 < x + w < x2 and y1 < y < y2) or # upper right corner of face
				(x1 < x  < x2 and y1 < y + h < y2) or # lower right corner of face
				(x1 < x + w < x2 and y1 < y + h < y2)): # lower left corner of face
			# then the face is in the specified rectangle and you can take a picture
			txt_to_speech ("Hold position, taking picture in 3")
			time.sleep(0.05)
			txt_to_speech("2")
			time.sleep(0.05)
			txt_to_speech("1")
			#time.sleep(0.05)
			#txt_to_speech("2")
			#time.sleep(0.05)
			#txt_to_speech("1")

			return (True, no_face_flag) # successful

		# determine right/ left orientation
		if x1 == 0 and x > x2: # if the face is too much to the right
			# give feedback, "move head to the right"(will be the opposite on the screen) or "move computer to the left"
			move_right = True
		elif x1 != 0 and x + w< x1: # if the face is too much to the left
			# give feedback, "move head to the left" or "move computer to the left"
			move_left = True

		#determine up/down orientation
		if bound_rect[1] == 0 and y2 < y:   # if the face is too low
			# give feedback, "move head up" or "pull screen down a little"  
			move_up = True
		elif y1 != 0 and y1 > (y +  h ): # if the face is too high
			# give feedback, "move head down" or "push screen up a little"
			move_down = True
	else:
		# no face detected
		txt_to_speech("No face found")
		match no_face_flag:
			case 0: # has not given instructions yet
				# move left 
				txt_to_speech("Move left")
				no_face_flag = 1
				return (False, no_face_flag)
			case 1: # told them to go left already
				txt_to_speech("Go back to original position")
				txt_to_speech("Move right")
				no_face_flag = 2
				return (False, no_face_flag)
			case 2: # told them to go left and right 
				txt_to_speech("Go back to original position")
				txt_to_speech("Move up")
				no_face_flag = 3
				return (False, no_face_flag)
			case 3: # told them to move left and right and up
				txt_to_speech("Go back to original position")
				txt_to_speech("Move down")
				no_face_flag = 0
				return (False, no_face_flag)
  

	# determine which instruction to give if a face is within the camera sight
	if move_right:
		txt_to_speech("Move head right")
		no_face_flag = 0
	elif move_left:
		txt_to_speech("Move head left")
		no_face_flag = 1
	elif move_up:
		txt_to_speech("Move head up")
		no_face_flag = 3
	elif move_down:
		txt_to_speech("Move head down")
		no_face_flag = 2

	return (False, no_face_flag) #did not take the photo



# end of fuctions

repeat = True
# repeat taking the picture from here
while repeat:

	cv2.namedWindow('capture', cv2.WINDOW_FULLSCREEN)
	window_coords = cv2.getWindowImageRect('capture')
	(_,_,window_width, window_length) = window_coords
	width_mid = window_width*0.5
	height_mid = window_length*0.5

	no_face_flag = 0


	# get the frame from the webcamera and change to grey
	cap = cv2.VideoCapture(0)
	# give starting prompt and start timing
	quad_command = command_menu()


	match quad_command: # boundary rectangle (x1, y1, x2, y2)
		case "top left":
			bound_rect = (0,0, width_mid/2, height_mid/2)
		case "top right":
			bound_rect = (width_mid*1.5, 0, window_width, height_mid/2)
		case "bottom left":
			bound_rect = (0, height_mid*1.5, width_mid/2, window_length)
		case "bottom right":
			bound_rect = (width_mid*1.5, height_mid*1.5, window_width, window_length)


	while True:
		timeout = time.time() + 3 #three seconds	 
		while True:
			# take and analyze a photo
			_, frame = cap.read()

			# bound_frame outline
			# get rid of later
			#cv2.rectangle(frame, (int(bound_rect [0]),int (bound_rect [1])), (int (bound_rect [2]),int (bound_rect [3])), (255,0,0),2)
			cv2.imshow('capture',frame)
			if cv2.waitKey(1) & 0xFF == ord('q') or time.time()>timeout:
				break
		
		(successful, no_face_flag) = find_face(frame, bound_rect, no_face_flag)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		if successful: # gives a countdown then reads and saves the current frame
			# then asks if the user wants to take another photo
			_, frame = cap.read()
			now = datetime.now()
			dt_str = now.strftime("%d_%m_%Y_%H_%M_%S")
			cv2.imwrite('selfie_' + dt_str + '.jpg', frame)

			another_picture_start = time.time()
			while True:
				r = sr.Recognizer()
				with sr.Microphone() as source:
					r.adjust_for_ambient_noise(source, duration=2)
					txt_to_speech("Picture saved, would you like to take another picture? Speak now!")
					audio = r.listen(source)
				try:
					y_n_reply = r.recognize_google(audio);
					y_n_reply = str.lower(y_n_reply)
					if y_n_reply == "yes":
						txt_to_speech("Taking another photo")
						break
					elif y_n_reply == "no":
						repeat = False
						break
					else:
						txt_to_speech("Could not understand audio.")

				except sr.UnknownValueError:
					txt_to_speech("Could not understand audio.")
			another_picture_start = time.time() - another_picture_start
			if repeat == False: break

txt_to_speech("Exiting")
cap.release()
cv2.destroyAllWindows()
