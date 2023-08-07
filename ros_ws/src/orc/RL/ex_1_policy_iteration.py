'''
Example of policy iteration with a simple discretized 1-DoF pendulum:
    goal is to find the optimal policy pi*
    To start we need an arbitrary initial policy pi_0 which is a map/array
    between the state value and a control value (2 integers both).
    We evaluate the policy using policy evaluation finding V_pi_k and so 
    we improve the policy acting greedily wrt V_pi_k.
    This is done by choosing the action that minimizes the cost + discount * V_pi_k(next state)
    getting pi_k+1(x)!
    We have also a guarantee that the policy pi_k+1 cannot be worse (typically is better :P )  
    than the policy at the previous iteration k!
    
'''

import numpy as np
from dpendulum import DPendulum
from ex_0_policy_evaluation import render_policy 
#from sol.ex_1_policy_iteration_sol_prof import policy_iteration
from sol.ex_1_policy_iteration_sol import policy_iteration
import time

### --- Random seed
RANDOM_SEED = int((time.time()%10)*1000)
print("Seed = %d" % RANDOM_SEED)
np.random.seed(RANDOM_SEED)

### --- Hyper paramaters
MAX_EVAL_ITERS    = 200     # Max number of iterations for policy evaluation
MAX_IMPR_ITERS    = 20      # Max number of iterations for policy improvement
VALUE_THR         = 1e-3    # convergence threshold for policy evaluation
POLICY_THR        = 1e-4    # convergence threshold for policy improvement
DISCOUNT          = 0.9     # Discount factor 
NPRINT            = 1       # print some info every NPRINT iterations
PLOT              = False
nq=51   # number of discretization steps for the joint angle q
nv=21   # number of discretization steps for the joint velocity v
nu=11   # number of discretization steps for the joint torque u

### --- Environment
env = DPendulum(nq, nv, nu)
V  = np.zeros(env.nx)                       # Value table initialized to 0 (I.G for V)
pi = env.c2du(0.0)*np.ones(env.nx, np.int64)  # policy table initialized to zero torque (I.G for policy)
  
pi = policy_iteration(env, DISCOUNT, pi, V, MAX_EVAL_ITERS, MAX_IMPR_ITERS, VALUE_THR, POLICY_THR, PLOT, NPRINT)
        
render_policy(env, pi, env.x2i(env.c2d([np.pi,0.]))) # to display how the computed policy 
                                                     # behaves in the viewer