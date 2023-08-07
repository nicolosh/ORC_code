#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 05:30:56 2021

@author: adelprete
"""
import numpy as np
#from sol.ex_0_policy_evaluation_prof import policy_eval
from ex_0_policy_evaluation import policy_eval

def policy_iteration(env, gamma, pi, V, maxEvalIters, maxImprIters, value_thr, policy_thr, plot=False, nprint=1000):
    ''' Policy iteration algorithm 
        env: environment used for evaluating the policy
        gamma: discount factor
        pi: initial guess for the policy
        V: initial guess of the Value table
        maxEvalIters: max number of iterations for policy evaluation
        maxImprIters: max number of iterations for policy improvement
        value_thr: convergence threshold for policy evaluation
        policy_thr: convergence threshold for policy improvement
        plot: if True it plots the V table every nprint iterations
        nprint: print some info every nprint iterations
    '''
    # IMPLEMENT POLICY ITERATION HERE
    
    # Create an array to store the Q value of different controls
    Q = np.zeros(env.nu)

    # Iterate at most maxImprIters loops
    for k in range(maxImprIters):
        # Evaluate current policy using policy_eval for at most maxEvalIters iterations 
        V = policy_eval(env, gamma, pi, V, maxEvalIters, value_thr, False) # V function associated to the current policy PI
        # HERE at the next iteration WE are using the V of the previous policy as I.G to compute the V of the next policy!!!
        
        # Make a copy of current policy table (before starting to modify it)
        pi_old = np.copy(pi)
        # The number of states is env.nx
        # The number of controls is env.nu (FINITE)
        
        # POLICY IMPROVEMENT STEP
        # **********************
        for x in range(env.nx):
            for u in range(env.nu): #looping over the set of possible actions
                # You can set the state of the robot using env.reset(x)
                env.reset(x) #reset the env to be in that state
                # You can simulate the robot using: x_next,cost = env.step(u)
                x_next, cost = env.step(u) # Q = l(x,u) + gamma * V_pi_k(next_state)
                Q[u] = cost +  gamma * V[x_next]
            
            # You can find the index corresponding to the minimum of an array with np.argmin(Q)
            pi[x] = np.argmin(Q) # best action corresponding to the minimum of Q function and to that state x
        # **************************
        # END POLICY IMPROVEMENT STEP
        
        # Check for convergence based on how much the policy has changed from the previous loop
        err = np.max(np.abs(pi - pi_old))
        if(err < policy_thr):
            print("Policy Iteration has converged after %d iterations" % k)
            break
        # you can plot the policy with: env.plot_policy(pi)
        # You can plot the Value table with: env.plot_V_table(V)
        if(k % nprint == 0):
            print("Policy Iteration - Iter %d, err = %f" % (k, err))
            env.plot_V_table(V)
            env.plot_policy(pi)
        
    # At the end return the policy pi
    return pi

'''
We can see that only the first time policy evaluation took many many iteration (66)
while afterwards just 18, 9, 6, until 2 because the initial guess is changing goodly so we are converging faster among the 
different iterations!!!
Here we are not evaluating a policy but we are computing the OPTIMAL policy for the 
infinite horizon case.
'''


