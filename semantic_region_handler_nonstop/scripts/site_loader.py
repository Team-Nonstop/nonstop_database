#!/usr/bin/env python

import rospy
import actionlib
import yaml

from worldlib.msg import *
from world_msgs.msg import *
from geometry_msgs.msg import *
from semantic_region_handler_nonstop.srv import *
from semantic_region_handler_nonstop.msg import *
from rospy_message_converter import json_message_converter, message_converter
from semantic_region_handler_nonstop import RegionLoader

def insert_site(site):
    req = AddSemanticRegionRequest()
    req.name = site['name']

    req.pose_stamped.pose = message_converter.convert_dictionary_to_ros_message('geometry_msgs/Pose',site['pose'])
    req.pose_stamped.header.frame_id = site['frame_id']
    req.region.radius = float(site['radius'])

    return req

def publish(site):
    return

if __name__ == '__main__':
    global site_pub
    rospy.init_node('site_loader')
    filename = rospy.get_param('~filename')
    srv_name = 'add_site_region'
    rl = RegionLoader(insert_site,srv_name,filename,publish,False)
    rospy.loginfo('Initialized')
    rl.spin()
    rospy.loginfo('Bye Bye')

