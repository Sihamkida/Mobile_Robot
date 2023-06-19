#!/usr/bin/env python
 
import rospy
import actionlib
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
import random
import math


 

class moving_client:

	def point_callback(self, pose):
		print('Goal Received. Moving to x={} y={}'.format(pose.pose.position.x, pose.pose.position.y))
		self.receiving_goals = True
		self.moving = False
		twist = Twist()
		twist.linear.x = 0.0
		twist.angular.z = 0.0
		self.cmd_vel_pub.publish(twist)
		
		goal = MoveBaseGoal()
		goal.target_pose = pose
		goal.target_pose.pose.orientation.w = 1
		self.currentGoal = goal
		self.client.send_goal(goal, self.goal_reached_cb)

	def stop_callback(self, flag):
		if self.receiving_goals:
			return
		if flag.data:
			self.printOnce("Stopped to gather enough position values for the QR Code")
			self.pause = True
			self.moveLock = True
			twist = Twist()
			twist.linear.x = 0.0
			twist.angular.z = 0.0
			self.cmd_vel_pub.publish(twist)
		else:
			self.printOnce("Finished reading QR code")
			self.moveLock = False

	def scan_callback(self, msg):
		tmp=[msg.ranges[0]]
		for i in range(1,21):
			tmp.append(msg.ranges[i])
		for i in range(len(msg.ranges)-21,len(msg.ranges)):
			tmp.append(msg.ranges[i])
		self.g_range_ahead = min(tmp)

	def goal_reached_cb(self, state, result):
		print(state)
		print('Goal reached without getting the information. Moving around the goal.')
		self.moving = True
		goal = self.currentGoal
		if goal.target_pose.pose.position.x <= 0.0:
			goal.target_pose.pose.position.x = goal.target_pose.pose.position.x + 1
			goal.target_pose.pose.orientation.w = 0
			goal.target_pose.pose.orientation.z = 1
		else:
			goal.target_pose.pose.position.x = goal.target_pose.pose.position.x - 1
			goal.target_pose.pose.orientation.w = 1
			goal.target_pose.pose.orientation.z = 0
		self.client.send_goal_and_wait(goal, rospy.Duration(20))
		if not self.moving:
			return
		goal = self.currentGoal
		if goal.target_pose.pose.position.y <= 0.0:
			goal.target_pose.pose.position.y = goal.target_pose.pose.position.y + 1
			goal.target_pose.pose.orientation.w = -0.7071068
			goal.target_pose.pose.orientation.z = 0.7071068
		else:
			goal.target_pose.pose.position.y = goal.target_pose.pose.position.y - 1
			goal.target_pose.pose.orientation.w = 0.7071068
			goal.target_pose.pose.orientation.z = 0.7071068
		self.client.send_goal_and_wait(goal, rospy.Duration(20))


	def check_Lock(self):
		counter = 0
		while self.moveLock and counter < 8*60:
			self.rate.sleep()
			counter = counter + 1
		self.moveLock = False

	def routine(self):
		for i in range(len(self.points_to_check)):
			print('Doing routine {}'.format(i))
			if self.receiving_goals:
				break
			goal_pose = self.points_to_check[i]
			self.client.send_goal_and_wait(goal_pose, rospy.Duration(50))
			self.distance_pub.publish(True)
			while self.pause:
				self.pause = False
				self.check_Lock()
				if self.receiving_goals:
					break
				self.rotate(self.time)
			self.pause = True
			self.distance_pub.publish(False)
			if self.receiving_goals:
				break

		if not self.receiving_goals:
			self.wander()


	def rotate(self,t):
		twist = Twist()
		twist.linear.x = 0.0
		twist.angular.z = 2*math.pi/t
		self.cmd_vel_pub.publish(twist)
		counter = 0
		while counter < t*60 and not self.moveLock:
			counter = counter + 1
			self.rate.sleep()
		twist.angular.z = 0.0
		self.cmd_vel_pub.publish(twist)

	def printOnce(self, string):
		if string != self.message:
			print(string)
			self.message = string



	def wander(self):
		while (not rospy.is_shutdown()) and (not self.receiving_goals):
			driving_forward = True
			if self.g_range_ahead < 0.8:
				# TURN
				driving_forward = False
			
			twist = Twist()
			if driving_forward:
				twist.linear.x = self.speed
				twist.angular.z = 0.0
			else:
				twist.linear.x = 0.0
				twist.angular.z = self.speed
			if not self.moveLock:
				print("Wander")
				self.cmd_vel_pub.publish(twist)
			self.rate.sleep()


	def create_points_to_check(self):
		x = [-4, -5, -6, -5, 1, 5, 6, 4]
		y = [0, -2, 0, 2, 0, 0, -2, 2]
		for i in range(len(x)):
			goal_pose = MoveBaseGoal()
			goal_pose.target_pose.header.frame_id = 'map'
			goal_pose.target_pose.pose.position.x = x[i]
			goal_pose.target_pose.pose.position.y = y[i]
			goal_pose.target_pose.pose.orientation.w = 1
			self.points_to_check.append(goal_pose)

	def __init__(self):
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction) 
		self.receiving_goals = False
		self.moving = False
		self.message = ''
		self.points_to_check = []
		self.client.wait_for_server()
		self.currentGoal = MoveBaseGoal()
		rospy.Subscriber('destination', PoseStamped, self.point_callback)
		rospy.Subscriber('stopAndWait', Bool, self.stop_callback)
		self.moveLock = False
		self.pause = True
		self.time = 20
		self.speed = 2*math.pi/self.time
		self.create_points_to_check()

		self.g_range_ahead = 1 # to start
		rospy.Subscriber('scan', LaserScan, self.scan_callback)
		self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

		self.distance_pub = rospy.Publisher("distance", Bool, queue_size=1)
		
		self.rate = rospy.Rate(60.0)

		rospy.sleep(0.5)
		self.routine()
		while not rospy.is_shutdown():
			self.rate.sleep()


if __name__ == '__main__':
	rospy.init_node('moving_client')
	moving_client()
