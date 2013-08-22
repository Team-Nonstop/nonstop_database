#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['semantic_region_handler_nonstop'],
    package_dir={'':'src'},
    scripts = [ 
                'scripts/site_handler.py',
                'scripts/site_poller.py',
                'scripts/site_loader.py',
                'scripts/alvar_ar_handler.py',
                'scripts/alvar_ar_poller.py',
                'scripts/alvar_ar_loader.py',
              ]
#    requires=['actionlib','rospy_message_converter','world_msgs','worldlib']
)

setup(**d)
