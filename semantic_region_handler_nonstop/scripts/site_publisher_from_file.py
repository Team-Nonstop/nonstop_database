#!/usr/bin/env python

import rospy
import actionlib
import yaml
import tf

from worldlib.msg import *
from world_msgs.msg import *
from geometry_msgs.msg import *
from semantic_region_handler_nonstop.srv import *
from semantic_region_handler_nonstop.msg import *
from rospy_message_converter import json_message_converter, message_converter
from semantic_region_handler_nonstop import RegionLoader
from visualization_msgs.msg import *

def insert_site(site):
    req = AddSemanticRegionRequest()
    req.name = site['name']

    req.pose_stamped.pose = message_converter.convert_dictionary_to_ros_message('geometry_msgs/Pose',site['pose'])
    req.pose_stamped.header.frame_id = site['frame_id']
    req.region.radius = float(site['radius'])

    return req

def publish(site):
    site_list = SitePoseList()
    # Markers
    marker_list = MarkerArray()    

    marker_id = 1
    for t in site:
        sp = SitePose()
        sp.name = t['name']
        sp.pose_cov_stamped.header.frame_id = t['frame_id']
        sp.radius = float(t['radius'])
        sp.pose_cov_stamped.pose.pose = message_converter.convert_dictionary_to_ros_message('geometry_msgs/Pose',t['pose'])
        site_list.sites.append(sp)
        

        p = sp.pose_cov_stamped.pose.pose.position
        position = (p.x,p.y,p.z)
        o= sp.pose_cov_stamped.pose.pose.orientation
        orientation = (o.x,o.y,o.z,o.w)
        tf_pub.sendTransform(position,orientation,rospy.Time.now(),str(sp.name),'map')
                                                                                                                                                    
        marker = Marker()
        marker.id = marker_id
        marker.header = sp.pose_cov_stamped.header
        marker.header.stamp = rospy.Time.now()
        marker.type = Marker.CYLINDER
        marker.ns = "concert"
        marker.action = Marker.ADD
        marker.lifetime = rospy.Duration.from_sec(0)
        marker.pose = sp.pose_cov_stamped.pose.pose
        marker.scale.x = sp.radius * 2
        marker.scale.y = sp.radius * 2  
        marker.scale.z = 0.1
        marker.color.r = 0
        marker.color.g = 0
        marker.color.b = 1.0
        marker.color.a = 0.5
                                                                                                                                                    
        marker_list.markers.append(marker)
                                                                                                                                                    
        marker_id = marker_id + 1

    site_pub.publish(site_list)
    marker_pub.publish(marker_list)
    
    return

if __name__ == '__main__':
    global site_pub
    rospy.init_node('site_loader')
    filename = rospy.get_param('~filename')
    srv_name = 'add_site_region'
    
    marker_pub = rospy.Publisher('site_marker',MarkerArray,latch=True)
    site_pub = rospy.Publisher('site_pose_list',SitePoseList,latch=True)
    tf_pub = tf.TransformBroadcaster()
    
    rl = RegionLoader(insert_site,srv_name,filename,publish,True)
    rospy.loginfo('Initialized')
    rl.spin()
    rospy.spin()
    rospy.loginfo('Bye Bye')

