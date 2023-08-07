#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 05:30:56 2021

@author: adelprete
"""
import numpy as np

def policy_eval(env, gamma, pi, V, maxIters, threshold, plot=False, nprint=1000):
    ''' Policy evaluation algorithm 
        env: environment used for evaluating the policy
        gamma: discount factor
        pi: policy to evaluate
        V: initial guess of the Value table
        maxIters: max number of iterations of the algorithm
        threshold: convergence threshold
        plot: if True it plots the V table every nprint iterations
        nprint: print some info every nprint iterations
    '''
    
    # IMPLEMENT POLICY EVALUATION HERE
    
    flag = False # to check if convergence is reached before maxIters
    
    # Iterate for at most maxIters loops
    for k in range(maxIters):
        # You can make a copy of the V table using np.copy
        V_old = np.copy(V)  # in order to not modify the current version of the V function because it's needed then to have it in memory
                            # to compute the convergence mesaurement in the end
        # The number of states is env.nx
        for x in range(env.nx):
            # Use env.reset(x) to re-set the robot/env current state
            env.reset(x) 
            # To simulate the system FW use env.step(u) which returns the next state and the cost
            if(callable(pi)): # if pi callable so if pi is a function
                u = pi(env, x)
            else:             # if not assumes pi is an array
                u = pi[x]
            x_next, cost = env.step(u)
            # Update V-Table with Bellman's equation
            V[x] = cost + gamma * V_old[x_next]
            

        # Check for convergence using the difference between the current and previous V table
        err = np.max(np.abs(V - V_old)) # infinity norm (max of abs value)
        if(err < threshold):
            print("Policy Evaluation has converged after %d iterations" % k)
            flag = True
            break
        
        # You can plot the V table with the function env.plot_V_table(V)
        if(k % nprint == 0):
            print("Policy Eval. Iter %d, err = %f" % (k, err))
            env.plot_V_table(V)
            
    # At the end return the V table
    if(flag==False):
        print("Policy evaluation has not converged before %d iterations" % maxIters)
        
    return V