#!/usr/bin/env python
import rospy
import math
import tf
import tf_conversions
import geometry_msgs.msg
import numpy as np

def point_camera_to_robotBase(point):
    camera_point = geometry_msgs.msg.PointStamped()
    camera_point.header.frame_id = "/camera_optical_link"
    camera_point.point = point
    try:
        listener.waitForTransform("/base_footprint", "/camera_optical_link", rospy.Time.now(), rospy.Duration(4.0))
        map_point = listener.transformPoint("/base_footprint", camera_point)
        map_point.point.z = 0
        return map_point.point
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print("Something went wrong")

def point_camera_to_map(point):
    camera_point = geometry_msgs.msg.PointStamped()
    camera_point.header.frame_id = "/camera_optical_link"
    camera_point.point = point
    try:
        listener.waitForTransform("/map", "/camera_optical_link", rospy.Time.now(), rospy.Duration(4.0))
        map_point = listener.transformPoint("/map", camera_point)
        map_point.point.z = 0
        return map_point.point
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print("Something went wrong")

def point_qr_to_map(x,y):
    qr_point = geometry_msgs.msg.PoseStamped()
    qr_point.header.frame_id = "hidden_frame"
    qr_point.pose.position.x = x
    qr_point.pose.position.y = y
    try:
        listener.waitForTransform("/map", "/hidden_frame", rospy.Time.now(), rospy.Duration(4.0))
        map_point = listener.transformPose("/map", qr_point)
        return map_point
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print("Something went wrong")


def find_and_broadcast_hidden_frame(pA1, pA2, pB1, pB2):
    a = np.array([[pA1.x, -pA1.y, 1., 0.], [pA1.y, pA1.x, 0., 1.], [pA2.x, -pA2.y, 1., 0.], [pA2.y, pA2.x, 0., 1.]])
    b = np.array([pB1.x, pB1.y, pB2.x, pB2.y])
    result = np.linalg.solve(a, b)

    theta = math.atan2(result.item(1), result.item(0))
    xt = result.item(2)
    yt = result.item(3)

    pose = geometry_msgs.msg.Pose()
    pose.position.x = xt
    pose.position.y = yt
    orientation = tf_conversions.transformations.quaternion_from_euler(0., 0., theta)
    pose.orientation.x = orientation[0]
    pose.orientation.y = orientation[1]
    pose.orientation.z = orientation[2]
    pose.orientation.w = orientation[3]
    print('Transformation of the hidden frame is: ({}, {}, {})({}, {}, {}, {})'.format(pose.position.x, pose.position.y, 0, pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w))
    hidden_frame_pub.publish(pose)
    #br.sendTransform((xt, yt, 0.0),
    #                    tf_conversions.transformations.quaternion_from_euler(0., 0., theta),
    #                     rospy.Time.now(),
    #                     "hidden_frame",
    #                     "map")
    #print('Hidden frame broadcasted')


def initialize():
    global listener
    global hidden_frame_pub
    listener = tf.TransformListener()
    hidden_frame_pub = rospy.Publisher('hidden_frame', geometry_msgs.msg.Pose, queue_size=1)
    #br = tf.TransformBroadcaster()
    
if __name__ == '__main__':
    rospy.init_node('tf_listener')
    initialize()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        test = point_camera_to_map(2.0, 0.0, 0.0)
        print(test)
