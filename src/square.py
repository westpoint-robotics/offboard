#!/usr/bin/env python3.8

import rospy
import mavros
from geometry_msgs.msg import PoseStamped, Twist
from mavros_msgs.msg import State, WaypointList, Waypoint
from mavros_msgs.srv import CommandBool, SetMode, WaypointPush
from sensor_msgs.msg import NavSatFix
import numpy as np
from start_up import Start

def coordinates(radius,center_x,center_y):
    theta = np.linspace(0,2*np.pi,1000)
    coords = []
    for i in range(1000):
        X = radius * np.cos(theta[i]) + center_x
        Y = radius * np.sin(theta[i]) + center_y
        coords.append((X,Y,2))
    return coords

def motion():

    rospy.init_node('rectangle', anonymous=True)
    rate = rospy.Rate(10.0)

    lat_long_sub = rospy.Subscriber('global_position/global', NavSatFix)
    waypoint_sub = rospy.Subscriber('mission/waypoints',WaypointList)
    

    waypoint_pub = rospy.Publisher('mission/waypoints', WaypointList, queue_size=10)
    vel_pub = rospy.Publisher('setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=1000)
    waypoint_srv = rospy.ServiceProxy('mission/push', WaypointPush)

    vel = Twist()
    waypoint_l = WaypointList()
    wp = Waypoint()

    wp.frame = 0
    wp.command =16
    wp.is_current = True
    wp.autocontinue = True
    wp.x_lat = -73.953220
    wp.y_long = 41.390722
    wp.z_alt = 5
    waypoint_l.waypoints.append(wp)

    wp.frame = 0
    wp.command =16
    wp.is_current = True
    wp.autocontinue = True
    wp.x_lat = -73.952799
    wp.y_long = 41.391646
    wp.z_alt = 7
    waypoint_l.waypoints.append(wp)

    wp.frame = 0
    wp.command =16
    wp.is_current = True
    wp.autocontinue = True
    wp.x_lat = -73.953039
    wp.y_long = 41.391728
    wp.z_alt = 7
    waypoint_l.waypoints.append(wp)

    wp.frame = 0
    wp.command =16
    wp.is_current = True
    wp.autocontinue = True
    wp.x_lat = -73.953519
    wp.y_long = 41.390800
    wp.z_alt = 5
    waypoint_l.waypoints.append(wp)

    wp.frame = 0
    wp.command =16
    wp.is_current = True
    wp.autocontinue = True
    wp.x_lat = -73.953220
    wp.y_long = 41.390722
    wp.z_alt = 5
    waypoint_l.waypoints.append(wp)

    try:
        if waypoint_srv.call(waypoint_l.waypoints).success:
            rospy.loginfo('Waypoints Sent Successfully')
        else:
            rospy.loginfo('Unable to send waypoints')
    except rospy.ServiceException as e:
        rospy.loginfo('Service call faild: %i' %e)


    while not rospy.is_shutdown():

        rate.sleep()


if __name__ == '__main__':
    set_mode_srv = rospy.ServiceProxy('mavros/set_mode', SetMode)
    if State().mode != 'GUIDED':
        set_mode_srv(base_mode=0, custom_mode='GUIDED')
    
    try:
        motion()
    except rospy.ROSInterruptException:
        pass