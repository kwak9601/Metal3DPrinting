#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
from std_msgs.msg import String
from std_msgs.msg import Int16
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Empty

is_stopped = False
mm2step = 1 / 0.01239
inm2mms = 0.4233
in2mm = 25.4
##
angle_per_step = 1.8
##

pub_set_speed = rospy.Publisher('set_speed', Int16, queue_size=1)
pub_move_abs = rospy.Publisher('move_abs', Int16, queue_size=1)
pub_move_rel = rospy.Publisher('move_rel', Int16, queue_size=1)

##
pub_turn = rospy.Publisher('turn',Int16, queue_size=1)
##


def cb_motor_stop(msg):
    global is_stopped
    rospy.loginfo('motor stopped')
    is_stopped = True


def cb_debug(debug_msg):
    rospy.loginfo("debug msg %s", debug_msg.data)

##
def angle_to_steps(degree):
    return Int16(int(round(degree/angle_per_step)))
##


def inch_to_steps(dist_in):
    return Int16(int(dist_in * in2mm * mm2step))


def mm_to_steps(dist_mm):
    return Int16(int(dist_mm * mm2step))


def inch_min_to_step_s(speed_inmin):
    return Int16(int(speed_inmin * inm2mms * mm2step))


def set_speed_inmin(speed_inmin):
    speed_stps = inch_min_to_step_s(speed_inmin)
    pub_set_speed.publish(speed_stps)
    rospy.loginfo(speed_stps)


def cb_set_speed_inmin(msg):
    set_speed_inmin(msg.data)


def cb_move_abs_in(msg):
    steps = inch_to_steps(msg.data)
    rospy.loginfo(steps)
    if delay_s > 0:
        rospy.sleep(delay_s)
    pub_move_abs.publish(steps)


def cb_move_abs_mm(msg):
    steps = mm_to_steps(msg.data)
    rospy.loginfo(steps)
    if delay_s > 0:
        rospy.sleep(delay_s)
    pub_move_abs.publish(steps)


def cb_move_rel_in(msg):
    steps = inch_to_steps(msg.data)
    rospy.loginfo(steps)
    if delay_s > 0:
        rospy.sleep(delay_s)
    pub_move_rel.publish(steps)


def cb_move_rel_mm(msg):
    steps = mm_to_steps(msg.data)
    rospy.loginfo(steps)
    if delay_s != 0:
        rospy.loginfo('motion delay: ' + str(delay_s) + ' s')
        rospy.sleep(delay_s)
    pub_move_rel.publish(steps)

##
def cb_turn_deg(msg):
    steps = angle_to_steps(msg.data)
    pub_turn.publish(steps)
##


if __name__ == '__main__':
    rospy.init_node('arduino_interface', anonymous=True)  # True ensures unique node name.
    sub_set_speed_inmin = rospy.Subscriber('set_speed_inmin', Float32, cb_set_speed_inmin)
    sub_move_abs_lin = rospy.Subscriber('move_abs_in', Float32, cb_move_abs_in)
    sub_move_rel_lin = rospy.Subscriber('move_rel_in', Float32, cb_move_rel_in)
    sub_move_abs_lin = rospy.Subscriber('move_abs_mm', Float32, cb_move_abs_mm)
    sub_move_rel_lin = rospy.Subscriber('move_rel_mm', Float32, cb_move_rel_mm)
    ##    
    sub_turn_angle = rospy.Subscriber('turn_deg', Float32, cb_turn_deg)
    ##

    sub_debug = rospy.Subscriber('debug', String, cb_debug)
    sub_motor_stop = rospy.Subscriber('motor_stop', Empty, cb_motor_stop)

    set_speed_inmin(14)

    speed_inmin = rospy.get_param('/arduino_interface/speed_inmin', 14)
    delay_s = rospy.get_param('/arduino_interface_node/delay_s', 0)
    rospy.sleep(1)

    while not rospy.is_shutdown():
        rospy.sleep(0.01)
