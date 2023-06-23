#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import String
from std_msgs.msg import Int16
from std_msgs.msg import Empty
is_stopped = False
def cb_motor_stop(msg):
    global is_stopped
    rospy.loginfo('motor stopped')
    is_stopped = True
def cb_chatter(chatter):
    rospy.loginfo("%s",chatter.data)
if __name__ == '__main__':
    rospy.init_node('motor', anonymous = True) #True ensures unique node name.
    sub_debug = rospy.Subscriber('chatter', String, cb_chatter)
    pub = rospy.Publisher('cmd_steps', Int16, queue_size=1)
    sub_motor_stop = rospy.Subscriber('motor_stop', Empty, cb_motor_stop)
    rospy.sleep(1)
    cmd = Int16(200)
    rospy.loginfo(cmd)
    pub.publish(cmd)
    while not rospy.is_shutdown() and not is_stopped:
        rospy.sleep(0.1)
    # try:
    #     # rotate()
    # except rospy.ROSInterruptException:
    #     pass
