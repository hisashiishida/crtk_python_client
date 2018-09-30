#!/usr/bin/env python

# Author: Anton Deguet
# Date: 2018-09-29

# (C) Copyright 2018 Johns Hopkins University (JHU), All Rights Reserved.

# --- begin cisst license - do not edit ---

# This software is provided "as is" under an open source license, with
# no warranty.  The complete license can be found in license.txt and
# http://www.cisst.org/cisst/license.txt.

# --- end cisst license ---

# Start your crtk compatible device first!
# dVRK example:
# > rosrun dvrk_robot dvrk_console_json -j <console-file> -c crtk_alpha
# Phantom Omni example:
# > rosrun sensable_phantom_ros sensable_phantom -j sawSensablePhantomRight.json

# To communicate with the device using ROS topics, see the python based example:
# > rosrun crtk_python_client crtk_haptic_example <device-namespace>

import crtk
import math
import sys
import rospy
import numpy
import PyKDL

# example of application using device.py
class crtk_haptic_example:

    # configuration
    def configure(self, device_namespace):
        # ROS initialization
        if not rospy.get_node_uri():
            rospy.init_node('crtk_haptic_example', anonymous = True, log_level = rospy.WARN)

        print(rospy.get_caller_id(), ' -> configuring crtk_device_test for ', device_namespace)
        # populate this class with all the ROS topics we need
        self.crtk_utils = crtk.utils(device_namespace)
        self.crtk_utils.add_measured_cp(self)
        self.crtk_utils.add_servo_cf(self)
        self.duration = 10 # 10 seconds
        self.rate = 200    # aiming for 200 Hz
        self.samples = self.duration * self.rate

    # main loop
    def run(self):
        self.running = True
        while (self.running):
            print ('\n- q: quit\n- p: print position\n- b: virtual box around current position with linear forces (10s)\n')
            answer = raw_input('Enter your choice and [enter] to continue\n')
            if answer == 'q':
                self.running = False
            elif answer == 'p':
                self.run_print()
            elif answer == 'b':
                self.run_box()
            else:
                print('Invalid choice\n')

    # just print current positions
    def run_print(self):
        print(self.measured_cp())

    # update base on linear forces
    def run_box(self):
        # save current position
        dim = 0.02
        p_gain = -50.0
        center = PyKDL.Frame()
        center.p = self.measured_cp().p
        for i in xrange(self.samples):
            wrench = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            # foreach d dimension x, y, z
            for d in xrange(3):
                distance = self.measured_cp().p[d] - center.p[d]
                if (distance > dim):
                    wrench[d] = p_gain * (distance - dim)
                elif  (distance < -dim):
                    wrench[d] = p_gain * (distance + dim)
            self.servo_cf(wrench)
            rospy.sleep(1.0 / self.rate)
        wrench = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.servo_cf(wrench)

# use the class now, i.e. main program
if __name__ == '__main__':
    try:
        if (len(sys.argv) != 2):
            print(sys.argv[0], ' requires one argument, i.e. crtk device namespace')
        else:
            example = crtk_haptic_example()
            example.configure(sys.argv[1])
            example.run()

    except rospy.ROSInterruptException:
        pass
