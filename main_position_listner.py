#!/usr/bin/env python
import rospy
import numpy as np # For random numbers
import time
 
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped 
 
class Position:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    #Create callback. This is what happens when a new message is received
    def sub_cal(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.z = msg.pose.pose.position.z

    #Initialize publisher
    def initSubscriber(self):
        rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, Position.sub_cal, queue_size=1000)

    def getRobotPosition(self):
        return self


def main():
    print("start test")
    rospy.init_node('position_listener')
    position = Position()
    position.initSubscriber()
    print("subscriber initialized")
    rate = rospy.Rate(1000)
    while (  ):
        print("loop start")
        print(position.getRobotPosition())
        rate.sleep


if __name__ == '__main__':
    main()
