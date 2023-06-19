#!/usr/bin/env python
# BEGIN ALL
import rospy
import actionlib
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from listener_node import markers
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
 
def scan_callback(msg):
  global g_range_ahead
  tmp=[msg.ranges[0]]
  for i in range(1,21):
    tmp.append(msg.ranges[i])
  for i in range(len(msg.ranges)-21,len(msg.ranges)):
    tmp.append(msg.ranges[i])
  g_range_ahead = min(tmp)
 
 
g_range_ahead = 1 # to start
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rospy.init_node('wander')
state_change_time = rospy.Time.now() + rospy.Duration(1)
driving_forward = True
rate = rospy.Rate(60)

#def goal_pose(pose):  working on it...
#    goal_pose = MoveBaseGoal()
#    goal_pose.target_pose.header.frame_id = 'map'
#    goal_pose.target_pose.pose.position.x = pose[0][0]
#    goal_pose.target_pose.pose.position.y = pose[0][1]
#    goal_pose.target_pose.pose.position.z = pose[0][2]
#    goal_pose.target_pose.pose.orientation.x = pose[1][0]
#    goal_pose.target_pose.pose.orientation.y = pose[1][1]
#    goal_pose.target_pose.pose.orientation.z = pose[1][2]
#    goal_pose.target_pose.pose.orientation.w = pose[1][3]

#    return goal_pose 

#going around randomly while there are no 2 QR codes detected.
if(len(markers) < 2): 
 while not rospy.is_shutdown():
   print g_range_ahead
   if g_range_ahead < 0.8:
     # TURN
     driving_forward = False
     print "Turn"
   
   else: # we're not driving_forward
     driving_forward = True # we're done spinning, time to go forward!
     #DRIVE
     print "Drive"
   
   twist = Twist()
   if driving_forward:
     twist.linear.x = 0.4
     twist.angular.z = 0.0
   else:
     twist.linear.x = 0.0
     twist.angular.z = 0.4
   cmd_vel_pub.publish(twist)
 
   rate.sleep()
# for more than 2 qr
else: 
 print("This should be implemented")
 #if __name__ == '__main__':
 #      rospy.init_node('patrol')
 #
 #  client = actionlib.SimpleActionClient('move_base', MoveBaseAction) 
 #  client.wait_for_server()
   
 #  while True:
 #      for pose in waypoints:   
 #         goal = goal_pose(pose)
 #         client.send_goal(goal)
 #          client.wait_for_result()
 #          rospy.sleep(3)
# END ALL