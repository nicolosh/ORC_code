# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 09:47:07 2019

@author: student
"""

'''
N.B. we have only 1 task at the moment in the cost function-->changing the task for now is NOT important (the robot behaviour won't change):
    changing the weight is not gonna change anything:
        the minimum will change (also if we minimize f(x) 10000 times) but 
        what will NOT change argmin!
        
N.B. Joint torques present some discontinuities in the plots if we have some inequality
constraints inside the solver otherwise they are continuos functions

N.B discontinuities in the accelerations plots comes from the fact that we reached the bounds
for the velocities and so the solver decided to have a step in the acceleration
in just one time step and this is reflected also into the torques that are dynamically
coupled!

N.B. higher feedback gains typically help speeding up the convergence: in simulations
we have no problems. Instead with TOO high gains, in reality, when we are above a certain time 
we can have troubles of stability (INSTABILITY)


'''

import numpy as np

np.set_printoptions(precision=3, linewidth=200, suppress=True)
LINE_WIDTH = 60

N_SIMULATION = 3000             # number of time steps simulated (simulation time)
dt = 0.002                      # controller time step (2 ms)
q0 = np.array([ 0. , -1.0,  0.7,  0. ,  0. ,  0. ])  # initial configuration

# REFERENCE SINUSOIDAL TRAJECTORY
amp                  = np.array([0*0.02, 0.1, 0.10])           # amplitude
phi                  = np.array([0.0, 0.5*np.pi, 0.0])         # phase
two_pi_f             = 1.4*2*np.pi*np.array([1.0, 0.5, 0.5])   # frequency (time 2 PI)
offset               = np.array([0.0, 0.0, 0.0])

w_ee = 1.0                      # weight of end-effector task
w_posture = 1e-3                # weight of joint posture task
w_torque_bounds = 1.0           # weight of the torque bounds
w_joint_bounds = 1.0

kp_ee = 5.0                   # proportional gain of end-effector constraint
kp_posture = 10.0               # proportional gain of joint posture task

tau_max_scaling = 0.4           # scaling factor of torque bounds
v_max_scaling = 0.4

ee_frame_name = "ee_fixed_joint"        # end-effector frame name
ee_task_mask = np.array([1., 1, 1, 0, 0, 0])

PRINT_N = 500                   # print every PRINT_N time steps
DISPLAY_N = 20                  # update robot configuration in viwewer every DISPLAY_N time steps
CAMERA_TRANSFORM = [2.582354784011841, 1.620774507522583, 1.0674564838409424, 0.2770655155181885, 0.5401807427406311, 0.6969326734542847, 0.3817386031150818]
SPHERE_RADIUS = 0.03
REF_SPHERE_RADIUS = 0.03
EE_SPHERE_COLOR  = (1, 0.5, 0, 0.5)
EE_REF_SPHERE_COLOR  = (1, 0, 0, 0.5)

path      = '/opt/openrobots/share/'
urdf      = path + "example-robot-data/robots/ur_description/urdf/ur5_robot.urdf";
srdf      = path + 'example-robot-data/robots/ur_description/srdf/ur5_robot.srdf'
