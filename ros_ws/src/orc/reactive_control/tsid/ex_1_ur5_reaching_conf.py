# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 09:47:07 2019

@author: student
"""

'''
E.E position tracking task (we are asking the robot to follow a circle basically) is in conflict with the postural task which asks 
the robot to remain still:
    everytime we increase the weight for postural task everything is smoothing
    but at the same time we are sacrifising the performance of E.E task: we are 
    'decreasing' the weight on the E.E tracking position task--> we are gonna have higher error

'''

import numpy as np
import os

np.set_printoptions(precision=3, linewidth=200, suppress=True)
LINE_WIDTH = 60

N_SIMULATION = 50000             # number of time steps simulated
dt = 0.002                      # controller time step
q0 = np.array([ 0. , -1.0,  0.7,  0. ,  0. ,  0. ])  # initial configuration

# REFERENCE SINUSOIDAL TRAJECTORY (3D vector cartesian space sinusoid definition )
amp                  = np.array([0.05, 0.0, 0.05])           # amplitude (3D vector not 6D)
phi                  = np.array([0.0, 0.0, np.pi/2])         # phase (3D vector not 6D)
two_pi_f             = 2*np.pi*np.array([0.3, 0.3, 0.3])   # frequency (time 2 PI)
offset               = np.array([0.1, 0.0, 0.0]) # changing something which is NOT reachable for the robot: set values here higher than 0.1!

w_ee = 1.0                      # weight of end-effector task

w_posture = 0e-2                # weight of joint posture task #if this weight is 0 we are gonna have much troubles: oscillations, peaks very frequently:
# the problem basically becomes underconstrained or not specified well so the solver is gonna choose one solution out of infinite for solving the problem: we have NO control
# over it

w_torque_bounds = 1.0           # weight of the torque bounds
w_joint_bounds = 1.0            # weight of the joint bounds

kp_ee = 50.0                   # proportional gain of end-effector constraint
kp_posture = 1.0               # proportional gain of joint posture task

tau_max_scaling = 0.4           # scaling factor of torque bounds
v_max_scaling = 0.4             # scaling factor of velocity bounds

ee_frame_name = "ee_fixed_joint"        # end-effector frame name
ee_task_mask = np.array([1., 1, 1, 0, 0, 0]) # 6D vector(x,y,z, \th, \phi, \ksi): 1 --> we are controlling that dimension
# 0 instead no control on that dimension.

PRINT_N = 500                   # print every PRINT_N time steps
DISPLAY_N = 20                  # update robot configuration in viwewer every DISPLAY_N time steps
CAMERA_TRANSFORM = [2.582354784011841, 1.620774507522583, 1.0674564838409424, 0.2770655155181885, 0.5401807427406311, 0.6969326734542847, 0.3817386031150818]
SPHERE_RADIUS = 0.03
REF_SPHERE_RADIUS = 0.03
EE_SPHERE_COLOR  = (1, 0.5, 0, 0.5)
EE_REF_SPHERE_COLOR  = (1, 0, 0, 0.5)

#ERROR_MSG = 'You should set the environment variable UR5_MODEL_DIR to something like "$DEVEL_DIR/install/share"\n';
#path      = os.environ.get('UR5_MODEL_DIR', ERROR_MSG)
path      = '/opt/openrobots/share/'
urdf      = path + "example-robot-data/robots/ur_description/urdf/ur5_robot.urdf";
srdf      = path + 'example-robot-data/robots/ur_description/srdf/ur5_robot.srdf'