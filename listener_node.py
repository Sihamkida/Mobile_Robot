#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import numpy as np


class Marker:
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.nx = 0.0
		self.ny = 0.0
		self.number = 0
		self.letter = "" 
		self.xMap = 0.0
		self.yMap = 0.0

def callback2(data):
	# get the object position from QR codes
	#rospy.loginfo("x: \n%s ", data.pose.position.x)
	#rospy.loginfo("y: \n%s ", data.pose.position.y)
	xPos = data.pose.position.x
	yPos = data.pose.position.y
	print("HI")
	print(xPos)
	print(yPos)
	print("Bye")
	
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
		print("Siham")
		print(xPos)
		print("Kida")
		if xPos != 0:	
			print("Done")	
			markers[number].xMap = xPos
			markers[number].yMap = yPos

		
		
	except:
		print("not facing qr code")


def initSubscriber():
	#create a global variable to store the word we are looking for
	global word
	global xPos
	global yPos
	word = ["" for i in range(5)]
	#create a global array to store markers
	global markers
	markers = [Marker() for i in range(5)]
	#initialize our subscriber
	#rospy.Subscriber("/visp_auto_tracker/code_message", String, callback)
	rospy.Subscriber("/visp_auto_tracker/object_position", PoseStamped, callback2)
	rospy.Subscriber("/visp_auto_tracker/code_message", String, callback)
	#get_the_word()

def get_information():
	print("The values are : \n")
	for j in range(6):
		print(values[j])  

def getWord():
	#check if you found the word, if yes print it.
	key_word = ''.join(word)
	if(len(key_word)==5):
		print("Hallelujah, you found the key word: \n")
		print(key_word)
		return key_word
	else :
		if __name__ == '__main__':
			print("You could not find the key word")
		return ""


def get_markers():
	return markers

if __name__ == '__main__':
	rospy.init_node('information_QR', anonymous=True)
 	initSubscriber()
	rospy.spin()
	print("The QR : \n", markers[0].yMap)
	print("The QR : \n", markers[1].yMap)
	print("The QR : \n", markers[2].yMap)

