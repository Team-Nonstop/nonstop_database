#!/usr/bin/env python
import rospy
import json
import tf

from semantic_region_handler_nonstop import RegionPoller
from semantic_region_handler_nonstop.msg import *
from visualization_msgs.msg import *

def parse(instances,region_poller):
    global tf_pub

    # sitePostList preparation
    site_pose_list = SitePoseList()
    # Markers
    marker_list = MarkerArray()

    marker_id = 1
    for i in instances:
        site = SitePose()
        site.name = i.name
        site.pose_cov_stamped = i.pose
        region = region_poller.get_region(i.description_id)
        site.radius = region.radius
        site_pose_list.sites.append(site)

        position = (i.pose.pose.pose.position.x,i.pose.pose.pose.position.y,i.pose.pose.pose.position.z)
        orientation = (i.pose.pose.pose.orientation.x,i.pose.pose.pose.orientation.y,i.pose.pose.pose.orientation.z,i.pose.pose.pose.orientation.w)
        tf_pub.sendTransform(position,orientation,rospy.Time.now(),str(i.name) + '_' + str(i.instance_id),'map')

        marker = Marker()
        marker.id = marker_id
        marker.header = i.pose.header
        marker.header.stamp = rospy.Time.now()
        marker.type = Marker.CYLINDER
        marker.ns = region_poller.concert_name
        marker.action = Marker.ADD
        marker.lifetime = rospy.Duration.from_sec(3)
        marker.pose = i.pose.pose.pose
        marker.scale.x = site.radius * 2
        marker.scale.y = site.radius * 2  
        marker.scale.z = 0.1
        marker.color.r = 0
        marker.color.g = 0
        marker.color.b = 1.0
        marker.color.a = 0.5

        marker_list.markers.append(marker)

        marker_id = marker_id + 1

    return [marker_list, site_pose_list]

def publisher(lists):
    global marker_pub
    global site_pub

    marker_pub.publish(lists[0])
    site_pub.publish(lists[1])


if __name__ == '__main__':
    global marker_pub
    global site_pub
    global tf_pub

    rospy.init_node('polling_site')
    spatial_world_model_ns = 'spatial_world_model'
    concert_name = "concert"
    instance_tags = [concert_name,'site']
    description_tags = [concert_name,'site','radius']
    descriptor_ref = json.dumps({'type':'semantic_circle'}) 

    marker_pub = rospy.Publisher('site_marker',MarkerArray,latch=True)
    site_pub = rospy.Publisher('site_pose_list',SitePoseList,latch=True)
    tf_pub = tf.TransformBroadcaster()

    sph = RegionPoller(spatial_world_model_ns,concert_name,instance_tags,description_tags,descriptor_ref,parse,publisher)
    rospy.loginfo('Initialized')
    sph.spin()
    rospy.loginfo('Bye Bye')

