#!/usr/bin/env python

# Author: Anton Deguet
# Date: 2015-02-22

# (C) Copyright 2015-2018 Johns Hopkins University (JHU), All Rights Reserved.

# --- begin cisst license - do not edit ---

# This software is provided "as is" under an open source license, with
# no warranty.  The complete license can be found in license.txt and
# http://www.cisst.org/cisst/license.txt.

# --- end cisst license ---

# Start a single arm using
# > rosrun dvrk_robot dvrk_console_json -j <console-file> -c crtk_alpha

# To communicate with the arm using ROS topics, see the python based example dvrk_arm_test.py:
# > rosrun crtk_python_client crtk_arm_test.py <arm-name>

import crtk
import math
import sys
import rospy
import numpy
import PyKDL

# example of application using arm.py
class example_application:

    def __del__(self):
        print ("delete application")
        delattr(self, 'arm')

    # configuration
    def configure(self, robot_name):
        print(rospy.get_caller_id(), ' -> configuring crtk_arm_test for ', robot_name)
        self.arm = crtk.arm(robot_name)

    # direct joint control example
    def servo_jp(self):
        print(rospy.get_caller_id(), ' -> starting joint direct')
        # get current position
        initial_joint_position = numpy.copy(self.arm.setpoint_jp())
        goal = numpy.copy(self.arm.setpoint_jp())
        print(rospy.get_caller_id(), ' -> testing direct joint position for 2 joints of ', initial_joint_position.size)
        amplitude = math.radians(10.0) # +/- 10 degrees
        duration = 5  # seconds
        rate = 200 # aiming for 200 Hz
        samples = duration * rate
        # create a new goal starting with current position
        goal = numpy.copy(initial_joint_position)
        for i in xrange(samples):
            goal[0] = initial_joint_position[0] + amplitude *  math.sin(i * math.radians(360.0) / samples)
            goal[1] = initial_joint_position[1] + amplitude *  math.sin(i * math.radians(360.0) / samples)
            self.arm.servo_jp(goal)
            rospy.sleep(1.0 / rate)
        print(rospy.get_caller_id(), ' <- joint direct complete')

    # # goal joint control example
    # def move_jp(self):
    #     print rospy.get_caller_id(), ' -> starting joint goal'
    #     # get current position
    #     initial_joint_position = numpy.copy(self.arm.measured_jp())
    #     print rospy.get_caller_id(), ' -> testing goal joint position for 2 joints of ', initial_joint_position.size)
    #     amplitude = math.radians(10.0)
    #     # create a new goal starting with current position
    #     goal = numpy.copy(initial_joint_position)
    #     # first motion
    #     goal[0] = initial_joint_position[0] + amplitude
    #     goal[1] = initial_joint_position[1] - amplitude
    #     self.arm.move_joint(goal, interpolate = True)
    #     # second motion
    #     goal[0] = initial_joint_position[0] - amplitude
    #     goal[1] = initial_joint_position[1] + amplitude
    #     self.arm.move_joint(goal, interpolate = True)
    #     # back to initial position
    #     self.arm.move_joint(initial_joint_position, interpolate = True)
    #     print rospy.get_caller_id(), ' <- joint goal complete'

    # # utility to position tool/camera deep enough before cartesian examples
    # def prepare_cartesian(self):
    #     # make sure the camera is past the cannula and tool vertical
    #     goal = numpy.copy(self.arm.measured_jp())
    #     if ((self.arm.name() == 'PSM1') or (self.arm.name() == 'PSM2') or (self.arm.name() == 'PSM3') or (self.arm.name() == 'ECM')):
    #         # set in position joint mode
    #         goal[0] = 0.0
    #         goal[1] = 0.0
    #         goal[2] = 0.12
    #         self.arm.move_joint(goal, interpolate = True)

    # direct cartesian control example
    def servo_cp(self):
        print(rospy.get_caller_id(), ' -> starting cartesian direct')

        # create a new goal starting with current position
        initial_cartesian_position = PyKDL.Frame()
        initial_cartesian_position.p = self.arm.setpoint_cp().p
        initial_cartesian_position.M = self.arm.setpoint_cp().M
        goal = PyKDL.Frame()
        goal.p = self.arm.setpoint_cp().p
        goal.M = self.arm.setpoint_cp().M
        # motion parameters
        amplitude = 0.05 # 5 cm
        duration = 5  # 5 seconds
        rate = 200 # aiming for 200 Hz
        samples = duration * rate
        for i in xrange(samples):
            goal.p[0] =  initial_cartesian_position.p[0] + amplitude *  math.sin(i * math.radians(360.0) / samples)
            goal.p[1] =  initial_cartesian_position.p[1] + amplitude *  math.sin(i * math.radians(360.0) / samples)
            self.arm.servo_cp(goal)
            rospy.sleep(1.0 / rate)
        print(rospy.get_caller_id(), ' <- cartesian direct complete')

    # # direct cartesian control example
    # def cartesian_goal(self):
    #     print rospy.get_caller_id(), ' -> starting cartesian goal'
    #     self.prepare_cartesian()

    #     # create a new goal starting with current position
    #     initial_cartesian_position = PyKDL.Frame()
    #     initial_cartesian_position.p = self.arm.servoed_cp().p
    #     initial_cartesian_position.M = self.arm.servoed_cp().M
    #     goal = PyKDL.Frame()
    #     goal.p = self.arm.servoed_cp().p
    #     goal.M = self.arm.servoed_cp().M

    #     # motion parameters
    #     amplitude = 0.05 # 5 cm

    #     # first motion
    #     goal.p[0] =  initial_cartesian_position.p[0] - amplitude
    #     goal.p[1] =  initial_cartesian_position.p[1]
    #     self.arm.move(goal)
    #     # second motion
    #     goal.p[0] =  initial_cartesian_position.p[0] + amplitude
    #     goal.p[1] =  initial_cartesian_position.p[1]
    #     self.arm.move(goal)
    #     # back to initial position
    #     goal.p[0] =  initial_cartesian_position.p[0]
    #     goal.p[1] =  initial_cartesian_position.p[1]
    #     self.arm.move(goal)
    #     # first motion
    #     goal.p[0] =  initial_cartesian_position.p[0]
    #     goal.p[1] =  initial_cartesian_position.p[1] - amplitude
    #     self.arm.move(goal)
    #     # second motion
    #     goal.p[0] =  initial_cartesian_position.p[0]
    #     goal.p[1] =  initial_cartesian_position.p[1] + amplitude
    #     self.arm.move(goal)
    #     # back to initial position
    #     goal.p[0] =  initial_cartesian_position.p[0]
    #     goal.p[1] =  initial_cartesian_position.p[1]
    #     self.arm.move(goal)
    #     print rospy.get_caller_id(), ' <- cartesian goal complete'

    # main method
    def run(self):
        self.servo_jp()
        # self.joint_goal()
        self.servo_cp()
        # self.cartesian_goal()

if __name__ == '__main__':
    try:
        if (len(sys.argv) != 2):
            print(sys.argv[0], ' requires one argument, i.e. name of crtk arm')
        else:
            application = example_application()
            application.configure(sys.argv[1])
            application.run()

    except rospy.ROSInterruptException:
        pass
