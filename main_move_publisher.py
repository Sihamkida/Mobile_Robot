#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped


def initialize():
    global destination_pub
    destination_pub = rospy.Publisher('destination', PoseStamped, queue_size=1)


def publish(destination):
    destination.header.frame_id = 'map'
    destination_pub.publish(destination)


def main():
    rospy.init_node("destination_publisher")
    destination = PoseStamped()
    destination.header.frame_id = "map"
    destination.pose.position.x = 0
    destination.pose.position.y = 0
    initialize()
    publish(destination)
    rospy.spin()
    

if __name__ == '__main__':
    initialize()
    main()
