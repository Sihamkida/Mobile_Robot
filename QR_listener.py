#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Bool
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
import numpy as np
import tf_listener

class Marker:
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.nx = 0.0
		self.ny = 0.0
		self.number = 0
		self.letter = "" 
		self.map_point = []
		self.positionDetermined = False

def distance_cb(data):
	global distance_reading
	distance_reading = data.data

def callback2(data):
	# get the object position from QR codes
	#rospy.loginfo("x: \n%s ", data.pose.position.x)
	#rospy.loginfo("y: \n%s ", data.pose.position.y)
	global mPos
	# rPos = tf_listener.point_camera_to_robotBase(Point(data.pose.position.x, data.pose.position.y, data.pose.position.z))
	# if (data.pose.position.z < 0.5 or data.pose.position.z > 2.5):
		# mPos.x = 0.0
		# return
	# print(data.pose.position)
	try:
		mPos = tf_listener.point_camera_to_map(Point(data.pose.position.x, data.pose.position.y, data.pose.position.z))
		# if outside of room exit
		if mPos.x < -8 and mPos.x > 8 and mPos.y < - 4 and mPos.y > 4:
			mPos.x = 0.0
	except:
		print("Camera transform not available")


def callback(data):
	# get the information from QR codes
	#rospy.loginfo("The info from QR code is: \n%s ", data.data)
	test = data.data
	info = test.split('\n')

	#create a global variable to store the info separately
	global values
	values = [0 for i in range(6)]	
	try:
		for j in range(6):
			values[j] = info[j].split('=')[1]
			#print(values[j])
		# Look for keyword from the QR codes
		if (values[4].strip()=="1") :
			word[0]=values[5]
		elif (values[4].strip()=="2") :
			word[1]=values[5]
		elif (values[4].strip()=="3") :
			word[2]=values[5]
		elif (values[4].strip()=="4") :
			word[3]=values[5]
		elif (values[4].strip()=="5") :
			word[4]=values[5]
		
		#store marker
		number = int(values[4]) - 1
		markers[number].x = float(values[0])
		markers[number].y = float(values[1])
		markers[number].nx = float(values[2])
		markers[number].ny = float(values[3])
		markers[number].number = number + 1
		markers[number].letter = values[5]

		if not distance_reading:
			return

		if mPos.x != 0.0:
			markers[number].map_point.append(mPos)
		if not markers[number].positionDetermined :
			stop_publisher.publish(True)
		else:
			stop_publisher.publish(False)
	except:
		pass

def initSubscriber():
	#create a global variable to store the word we are looking for
	global word
	#create a global variable to store information from second subscriber
	global mPos
	mPos = Point()
	word = ["" for i in range(5)]
	#create a global array to store markers
	global markers
	markers = [Marker() for i in range(5)]
	global distance_reading
	distance_reading = False
	#initialize our subscribers
	tf_listener.initialize()
	rospy.Subscriber("/visp_auto_tracker/object_position", PoseStamped, callback2)
	rospy.Subscriber("/visp_auto_tracker/code_message", String, callback)
	rospy.Subscriber("distance", Bool, distance_cb)
	#initialize publisher
	global stop_publisher
	stop_publisher = rospy.Publisher('stopAndWait', Bool, queue_size=1)


def get_information():
	for j in range(5):
		i = j+1
		print("The information inside marker %d are : \n" % i)
		print(markers[j].x)  
		print(markers[j].y)  
		print(markers[j].nx)  
		print(markers[j].ny)  
		print(markers[j].number)  
		print(markers[j].letter)  
		print(markers[j].map_point)


def getWord():
	#check if you found the word, if yes print it.
	key_word = ''.join(word)
	if(len(key_word)==5):
		print("Hallelujah, you found the key word: {}".format(key_word))
		return key_word
	else :
		if __name__ == '__main__':
			print("You could not find the key word")
		return None

if __name__ == '__main__':
	rospy.init_node('information_QR', anonymous=True)
 	initSubscriber()
	rospy.spin()
	getWord()
	get_information()
