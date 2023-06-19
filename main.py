#!/usr/bin/env python

import rospy
import QR_listener
import main_move_publisher
import tf_listener
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point

def nextIndex(i):
    i += 1
    if i > 4:
        i = 0
    return i

def meanMapPoint(mapPoints):
    if len(mapPoints) < 10:
        return None
    sumX = 0
    sumY = 0
    for mapPoint in mapPoints:
        sumX += mapPoint.x
        sumY += mapPoint.y
    meanX = sumX / len(mapPoints)
    meanY = sumY / len(mapPoints)
    meanPoint = Point(meanX, meanY, 0) 
    return meanPoint

def printOnce(string):
    global printed
    if string in printed:
        return
    else:
        print(string)
        printed.append(string)

def main():

    printFlag = [False] * 10

    print("Start")
    rospy.init_node('main_script', anonymous=True)
    QR_listener.initSubscriber()
    main_move_publisher.initialize()
    tf_listener.initialize()
    
    global printed
    printed = []
    allMarkersfound = False
    while (allMarkersfound == False and not rospy.is_shutdown()):
        nKnownMarkers = 0
        knownMarker = [None] * 2
        # if all letters are found dont try to find frame
        count = 0
        for marker in QR_listener.markers:
            if marker.letter != "":
                count += 1
        if count == 5:
            allMarkersfound = True
            
        #see which markers have well known positions
        for i, marker in enumerate(QR_listener.markers):
            temp = marker.map_point[:]
            mean = meanMapPoint(temp)
            if mean != None:
                marker.positionDetermined = True
                nKnownMarkers += 1
                if knownMarker[0] == None:
                    knownMarker[0] = i
                else:
                    knownMarker[1] = i
        if (nKnownMarkers == 1):
            printOnce("First marker found. Looking for second one.")
        elif (nKnownMarkers > 1):
            print('Found enough values to calculate the hidden frame.')
            # calculate frameTransfer
            p1x = QR_listener.markers[knownMarker[0]].x
            p1y = QR_listener.markers[knownMarker[0]].y
            p1 = Point(p1x, p1y, 0)
            
            p1MapList = QR_listener.markers[knownMarker[0]].map_point
            p1Map = meanMapPoint(p1MapList)
            
            p2x = QR_listener.markers[knownMarker[1]].x
            p2y = QR_listener.markers[knownMarker[1]].y
            p2 = Point(p2x, p2y, 0)

            p2MapList = QR_listener.markers[knownMarker[1]].map_point
            p2Map = meanMapPoint(p2MapList)
            tf_listener.find_and_broadcast_hidden_frame(p1, p2, p1Map, p2Map)

            frameTransfer = True
            rospy.sleep(1)
            print('Starting the loop to find and scan unknown markers.')

            while (not rospy.is_shutdown() and QR_listener.getWord() == None and frameTransfer):
                #print("start loop")
                for i, marker in enumerate(QR_listener.markers):
                    print("i ",i)
                    print("marker.letter ",marker.letter)
                    if marker.letter != "":
                        print("next marker.letter ",QR_listener.markers[nextIndex(i)].letter)
                        if (QR_listener.markers[nextIndex(i)].letter == ""):
                            goal = tf_listener.point_qr_to_map(marker.nx, marker.ny)
                            print("goal: {},{}".format(goal.pose.position.x, goal.pose.position.y))
                            # check if frame is resonable
                            if (goal.pose.position.x < -8 and goal.pose.position.x > 8 and goal.pose.position.y < - 4 and goal.pose.position.y > 4):
                                #goal outside of room - discard frame
                                print("goal outside of room - discard frame")
                                frameTransfer = False
                                QR_listener.markers[knownMarker[0]].map_point = [] 
                                QR_listener.markers[knownMarker[1]].map_point = [] 
                            else:
                                main_move_publisher.publish(goal)
                                #print("moving to goal")
                                while (QR_listener.markers[nextIndex(i)].letter == ""):
                                    rospy.sleep(0.2)
                                break
                        else: continue
                rospy.sleep(0.1)
            
        else:
            printOnce("Looking for the first marker.")
        rospy.sleep(0.1)

    rate = rospy.Rate(1)
    QR_listener.getWord()
    print('Finished!')
    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == '__main__':
    main()
