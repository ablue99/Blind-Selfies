# Selfie taking assistance for blind people
import cv2
import numpy as np
import sched, time 
import threading


import speech_recognition as sr
#import pyttsx3 as p3

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



def find_face(frame, bound_rect):
	grey_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
	all_face_coords = face_cascade.detectMultiScale(grey_frame, 1.2, 5) # detect the face, return coordinates, may have more than one face
	move_right = False
	move_up = False

	if all_face_coords != ():
		face_coords = all_face_coords [0] # use only one face
		(x1,y1,x2,y2) = bound_rect
		(x, y, w, h) = face_coords
		
		#cv2.rectangle(frame, (x,y), (x+face_coords[2],y+ h),(0,255,255),2)
		# put this series of if statements in a loop, while a photo hasn't been taken yet?
		
		#if (x1 < x < x2 and (y1 < y < y2) and 
		#(x1 < x +face_coords[2]<x2) and (y1 < y + h < y2)):

		# double check that this logic is correct, it's not
		if ((x1 < x < x2 and y1 < y < y2) or # upper left corner of face
		(x1 < x + w < x2 and y1 < y < y2) or # upper right corner of face
		(x1 < x  < x2 and y1 < y + h < y2) or # lower right corner of face
		(x1 < x + w < x2 and y1 < y + h < y2)): # lower left corner of face
		    # then the face is in the specified rectangle and you can take a picture
		    print ("success")
		    return True # successful
		
		# bound_rect[0] = x1, br[1]= y1, br[2] = x2, br[3] = y2
		# fc[0]=x, fc[1] = y, fc[2] = w, fc[3] = h


		# determine right/ left orientation
		# will need to have something to skip these blocks of code if the top was completed successfully
		#if x1 == 0 and x + w  > x2: # if the face is too much to the right
		if x1 == 0 and x > x2: # if the face is too much to the right
			# give feedback, "move head to the right"(will be the opposite on the screen) or "move computer to the left"
			move_right = True 
		#elif x1 != 0 and x+ w < x1: # if the face is too much to the left
		elif x1 != 0 and x + w< x1: # if the face is too much to the left
			# give feedback, "move head to the left" or "move computer to the left"
			move_right = False

		#determine up/down orientation
		#if bound_rect[1] == 0 and y2 < y + h :   # if the face is too low
		if bound_rect[1] == 0 and y2 < y:   # if the face is too low
			# give feedback, "move head up" or "pull screen down a little"  
			move_up = True 
		#elif y1 != 0 and y1 > y: # if the face is too high
		elif y1 != 0 and y1 > (y +  h ): # if the face is too high
			# give feedback, "move head down" or "push screen up a little"
			move_up = False 

	# determine which instruction to give, this may need to be changed so that it won't say down if you already are within that boundary
	if move_up and move_right: print("Move head up and right") 
	elif (not move_up) and move_right: print("Move head down and right") 
	elif move_up and (not move_right): print("Move head up and left") 
	elif (not move_up) and (not move_right): print("Move head down and left") #is this effective or slow? 

	return False #did not take the photo




cv2.namedWindow('capture', cv2.WINDOW_FULLSCREEN)
window_coords = cv2.getWindowImageRect('capture')
(_,_,window_width, window_length) = window_coords
# 2= width, 3= length
width_mid = window_width*0.5
height_mid = window_length*0.5


# get the frame from the webcamera and change to grey
cap = cv2.VideoCapture(0)
# give starting prompt


#quad_command  = input("quadrant: ")
quad_command = "bottom right"

# after it recieves a command
match quad_command: # boundary rectangle (x1, y1, x2, y2)
	case "top left":
		bound_rect = (0,0, width_mid/2, height_mid/2)
	case "top right":
		bound_rect = (width_mid*1.5, 0, window_width, height_mid/2)
	case "bottom left":
		bound_rect = (0, height_mid*1.5, width_mid/2, window_length)
	case "bottom right":
		bound_rect = (width_mid*1.5, height_mid*1.5, window_width, window_length)
		# ask the user to say the command again
		# think about adding another option if voice doesn't work, like maybe pressing the space bar a certain number of times?
		# or press the space bar when the option you want is said

	
while True:
	timeout = time.time() + 2 #two seconds	 
	while True:
	# take and analyze a photo  
		_, frame = cap.read() 

		# bound_frame outline
		cv2.rectangle(frame, (int(bound_rect [0]),int (bound_rect [1])), (int (bound_rect [2]),int (bound_rect [3])), (255,0,0),2)
		
		'''
		grey_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
		all_face_coords = face_cascade.detectMultiScale(grey_frame, 1.2, 5) # detect the face, return coordinates, may have more than one face
		if all_face_coords != ():
			face_coords = all_face_coords [0] # use only one face
			cv2.rectangle(frame, (face_coords[0],face_coords[1]), (face_coords[0]+face_coords[2],face_coords[1]+face_coords[3]),(0,255,255),2)
		'''


		cv2.imshow('capture',frame)	
		if cv2.waitKey(1) & 0xFF == ord('q') or time.time()>timeout:
			break

	#face_t = threading.Thread(target = find_face, args = (frame, bound_rect))
	#	face_t.start()	
	successful = find_face(frame, bound_rect)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


	if successful: # needs to be changed to not just exit but to give a countdown then read and save the current frame
		# then ask if the user wants to take another photo
		print ("All done")
		# would need to put a check here if they want to repeat it
		break

print ("Exiting")
cap.release()
cv2.destroyAllWindows()






# add a feature that calculates the percent of the screen taken up by the face?
# if it is too great or too small then tell the person to move closer or further away
# add a countdown for when the photo is taken? maybe
# could also add a pinging sound that can help the person orientate themselves to the position of the camera
# sometimes it's the computer screen you need to move the position of, so it could tell the person to move or to move their screen in a certain way


# have the space bar be the shutter button? 

# be waiting for input, should there be a signal? Maybe a pinging sound? What is a good to go sound for blind people?
# receive directional input from user, analyze where the face is, give corrective audio prompts for where to move (a little a lot etc)
# have a prompt for if no face is sighted, like maybe turn on your lights or come closer? 


# should it prompt when to stop? 
