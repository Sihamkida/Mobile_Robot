#!/usr/bin/env python  
import rospy
 
import tf
from geometry_msgs.msg import Pose

class static_hidden_frame_broadcaster():

	def frame_cb(self, pose):
		print('Hidden frame broadcasted')
		self.hidden_frame = pose
		self.has_tf = True

	def __init__(self):
		self.hidden_frame = Pose()
		self.has_tf = False
		self.br = tf.TransformBroadcaster()
		rospy.Subscriber('hidden_frame', Pose, self.frame_cb)

		while not rospy.is_shutdown():
			if self.has_tf:
				self.br.sendTransform((self.hidden_frame.position.x, self.hidden_frame.position.y, self.hidden_frame.position.z),
                         (self.hidden_frame.orientation.x, self.hidden_frame.orientation.y, self.hidden_frame.orientation.z, self.hidden_frame.orientation.w),
                         rospy.Time.now(),
                         "hidden_frame",
                         "map")
			rospy.sleep(0.001)


if __name__ == '__main__':
	rospy.init_node('static_hidden_frame_broadcaster')
	static_hidden_frame_broadcaster()