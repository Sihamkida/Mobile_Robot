#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import numpy as np
import geometry_msgs.msg


class Marker:
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.nx = 0.0
		self.ny = 0.0
		self.map_position = geometry_msgs.msg.PoseStamped()
		self.number = 0
		self.letter = "" 


def marker_callback(data):
	# get the information from QR codes
	rospy.loginfo("The info from QR code is: \n%s ", data.data)
	test = data.data
	info = test.split('\n')

	values = [0 for i in range(6)]
	for j in range(6):
		values[j] = info[j].split('=')[1].strip()
		#print(values[j])
	number = int(values[4])-1
	if(number != markers[number].number):
		#store marker
		word[number] = values[5]
		markers[number].x = float(values[0])
		markers[number].y = float(values[1])
		markers[number].nx = float(values[2])
		markers[number].ny = float(values[3])
		markers[number].number = number
		markers[number].letter = values[5]
		markers[number].map_position = position
		


def position_callback(pose):
	position = pose


def initSubscriber():
	#create a global variable to store the word we are looking for
	global word
	word = ["" for i in range(5)]
	#create a global array to store markers
	global markers
	markers = [Marker() for i in range(5)]
	global count
	global position
	global target
	#initialize our subscriber
	rospy.Subscriber("/visp_auto_tracker/code_message", String, marker_callback)
	rospy.Subscriber("/visp_auto_tracker/object_position", geometry_msgs.msg.PoseStamped(), position_callback)
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction) 
	get_the_word()

def get_information():
	print("The values are : \n")
	for j in range(6):
		print(values[j])  

def get_the_word():
	#check if you found the word, if yes print it.
	key_word = ''.join(word)
	if(len(key_word)==5):
		print("Hallelujah, you found the key word: \n")
		print(key_word)
	else :
		print("You could not find the key word")


if __name__ == '__main__':
	while not rospy.is_shutdown():