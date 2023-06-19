#!/usr/bin/env python

import rospy
import QR_listener
import main_move_publisher
import position_listener
import tf_listener
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point

def nextIndex(i):
    i += 1
    if i > 4:
        i = 0
    return i


def main():

    printFlag = [False] * 10

    print("starting")
    rospy.init_node('main_script', anonymous=True)
    print("node init")
    QR_listener.initSubscriber()
    main_move_publisher.initialize()
    tf_listener.initialize()
    
    frameTransfer = None
    while (frameTransfer == None and not rospy.is_shutdown()):
        nKnownMarkers = 0
        knownMarker = [None]*2
        for marker in QR_listener.markers:
            if marker.letter != "":
                nKnownMarkers += 1
                if knownMarker[0] == None:
                    knownMarker[0] = marker
                else:
                    knownMarker[1] = marker
        if (nKnownMarkers == 1):
            print("1 marker found. Looking for second one")
        elif (nKnownMarkers > 1):
            # calculate frameTransfer
            p1x = knownMarker[0].x
            p1y = knownMarker[0].y
            p1 = Point(p1x, p1y, 0)
            
            p1Map = knownMarker[0].map_point
            
            p2x = knownMarker[1].x
            p2y = knownMarker[1].y
            p2 = Point(p2x, p2y, 0)

            p2Map = knownMarker[1].map_point
            
            tf_listener.find_and_broadcast_hidden_frame(p1Map, p2Map, p1, p2)
            frameTransfer = 1
            rospy.sleep(0.1)
        else:
            print("no markers found, yet")
        rospy.sleep(1)

    print("getWord ",QR_listener.getWord())
    while (not rospy.is_shutdown() and QR_listener.getWord() == None):
        print("start loop")
        for i, marker in enumerate(QR_listener.markers):
            print("i ",i)
            print("marker.letter ",marker.letter)
            if marker.letter != "":
                print("next marker.letter ",QR_listener.markers[nextIndex(i)].letter)
                if (QR_listener.markers[nextIndex(i)].letter == ""):
                    goal = tf_listener.point_qr_to_map(marker.nx, marker.ny)
                    print("goal: {},{}".format(goal.pose.position.x, goal.pose.position.y))
                    main_move_publisher.publish(goal)
                    print("moving to goal")
                    while (QR_listener.markers[nextIndex(i)].letter == ""):
                        rospy.sleep(0.2)
                    break
                else: continue
        rospy.sleep(1)
        
    rate = rospy.Rate(1)
    print('Finished')
    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == '__main__':
    main()
