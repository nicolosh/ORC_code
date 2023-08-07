'''
Example of Value iteration with a simple discretized 1-DoF pendulum:
    value and policy iteration can be seen as special cases of modified policy iteration
    which like a generalization of policy iteration!!!
    Again we use the previous V function as I.G. 
    for computing V_k+1 (x) for the next state.
    
    Here we don't have any policy:
        we just update the value V using a policy which is optimal for the current
        estimation of the value every time.
    This algorithm doesn't give the optimal policy directly but we need to
    compute pi_* (optimal) using V* (optimal value).
'''

import numpy as np
from dpendulum import DPendulum
from ex_0_policy_evaluation import render_policy
#from sol.ex_2_value_iteration_sol_prof import value_iteration
from sol.ex_2_value_iteration_sol import value_iteration

### --- Hyper paramaters
MAX_ITERS       = 200     # Max number of iterations for the algorirthm
VALUE_THR       = 1e-4    # convergence threshold
NPRINT          = 3       # print some info every NPRINT iterations
PLOT            = False   # where to plot stuff during the algorithm
DISCOUNT        = 0.9     # Discount factor 
nq=51   # number of discretization steps for the joint angle q
nv=21   # number of discretization steps for the joint velocity v
nu=11   # number of discretization steps for the joint torque u

### --- Environment
env = DPendulum(nq, nv, nu)
V  = np.zeros(env.nx)           # Value table initialized to 0
    
def compute_policy_from_V(env, V):
    ''' Compute greedy policy with respect or from the given Value table V '''
    Q  = np.zeros(env.nu)   # temporary array to store value of different controls
    pi = np.zeros(env.nx)   # policy table
    for x in range(env.nx):     # for every state
        for u in range(env.nu): # for every action
            env.reset(x)        # reset state to x
            x_next,cost = env.step(u)   # apply action u
            Q[u] = cost + DISCOUNT * V[x_next] # store value associated to u 
        
        # Rather than simply using argmin we do something slightly more complex
        # to ensure simmetry of the policy color map when multiply control inputs/ minima of Q
        # result in the same value of Q function. In these cases we prefer the more extreme
        # actions (so largest in magnitude ones).
        
        # ************ MINIMIZATION after having computed all the values of the Q function **********
#        pi[x] = np.argmin(Q) # OLD METHOD
        
        # ****** New method *******
        u_best = np.where(Q==np.min(Q))[0] # computing the action u minimizing the Q function
        if(u_best[0]>env.c2du(0.0)):    # if all the best action corresponds to a positive torque
            pi[x] = u_best[-1]          # take the largest torque
        elif(u_best[-1]<env.c2du(0.0)): # if all the best action corresponds to a negative torque
            pi[x] = u_best[0]           # take the smallest torque (largest in abs value)
        else:                           # otherwise take the average value among the best actions
            pi[x] = u_best[int(u_best.shape[0]/2)]
        
    return pi
    
V = value_iteration(env, DISCOUNT, V, MAX_ITERS, VALUE_THR, PLOT, NPRINT)
  
pi = compute_policy_from_V(env, V)      
env.plot_policy(pi)
render_policy(env, pi, env.x2i(env.c2d([np.pi,0.])))
    