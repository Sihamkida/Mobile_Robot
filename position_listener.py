#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
# from geometry_msgs.msg import PoseStamped

def callback(data):
	position = data.pose.position


def initSubscriber():
	global position
	rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, callback)


def getRobotPosition():
	return position


def main():
	rospy.init_node('position_listener', anonymous=True)
 	initSubscriber()
	rospy.spin()


if __name__ == '__main__':
    main()
