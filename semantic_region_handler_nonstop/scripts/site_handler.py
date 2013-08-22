#!/usr/bin/env python

import rospy
import json

from semantic_region_handler_nonstop import *
from semantic_region_handler_nonstop.msg import Region

def radius_compare(a, b):
    return a.radius == b.radius

if __name__ == '__main__':

    rospy.init_node('radius_region_handler')

    spatial_world_model_ns = 'spatial_world_model'
    concert_name = "concert"
    instance_tags = [concert_name,'site']
    description_tags = [concert_name,'site','radius']
    descriptor_ref = json.dumps({'type':'semantic_radius'}) 

    srv_name = {}
    srv_name['add'] = 'add_site_region'
    srv_name['get'] = 'get_site_region'
    srv_name['remove'] = 'remove_site_region'

    sph = SemanticRegionHandler(spatial_world_model_ns,concert_name,instance_tags,description_tags,descriptor_ref,radius_compare,srv_name)
    rospy.loginfo('Initialized')
    sph.spin()
    rospy.loginfo('Bye Bye')

