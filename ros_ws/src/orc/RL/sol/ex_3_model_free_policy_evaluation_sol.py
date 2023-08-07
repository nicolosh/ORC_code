#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 23:56:07 2021

@author: adelprete
"""
import numpy as np

def mc_policy_eval(env, gamma, pi, nEpisodes, maxEpisodeLength, 
                   V_real, plot=False, nprint=1000):
    ''' Monte-Carlo Policy Evaluation (FIRST VISIT):
        env: environment 
        gamma: discount factor
        pi: policy to evaluate
        nEpisodes: number of episodes to be used for evaluation
        maxEpisodeLength: maximum length of an episode
        V_real: real Value table
        plot: if True plot the V table every nprint iterations
        nprint: print some info every nprint iterations
        J(x) = cost to go / total sum of the cost starting from that state (time) until the end of the episode
        N(x) # of times a state has been visited
        To compute the total cost to go we need to wait until the end of an episode:
            we need to keep track of all the states that we visit and all the cost got in an episode
            so than, after having reached episode end, we can compute the cost to go for each state and so 
            we can do the update of the total cost C(x) and estimated value function V(x)
    '''
    # create a vector N to store the number of times each state has been visited
    N = np.zeros(env.nx)
    # create a vector C to store the cumulative cost associated to each state
    C = np.zeros(env.nx)
    # create a vector V to store the Value
    V = np.zeros(env.nx)
    # create a list V_err to store history of the error between real and estimated V table
    V_err = [] # used just for plotting / performance of the algorithm
    
    # for each episode
    for k in range(nEpisodes):
        # reset the environment to a random state (because we don't have the model of the robot)
        env.reset()
        x_list = [] # list for storing all the visited states because later we need to update the value for those states
        cost_list = [] 
        # SIMULATING THE SYSTEM WITH GIVEN POLICY 
        for i in range(maxEpisodeLength):
            # compute the control from the policy
            x = env.x
            if(callable(pi)): # check if policy is a function
                u = pi(env, x)
            else: # check if policy is a vector
                u = pi[x]
                
            # simulate the system using the given policy pi
            x_next, cost = env.step(u)                     # x_next NOT USED!!!
            # keep track of the states visited in this episode
            # keep track of the costs received at each state in this episode
            x_list.append(x) # adding the visited state !
            cost_list.append(cost) # cost is the one we got when we apply action u from state x
        
        # *** EPISODE HAS FINISHED ***
        
        # we are moving backward in order to not add the same things (going from the end of Ep to -1 with a step of -1)
        
        # Update the V-Table by computing the cost-to-go J backward in time        
        J = 0
        for i in range(maxEpisodeLength-1, -1, -1): # going through all the visited states we need to compute the total cost for that state until the 
                                    # end of horizon using this cost to update the V(x) for that state x
            x = x_list[i]
            N[x] += 1 # update of how many times we visited state i
            J = cost_list[i] + gamma*J      # J = sum of all the costs from that state until the end (J is the cost to go of the previous iteration)
            
            '''
            naive way 
            for i in range(len(x_list))
                J = 0
                # loop for computing the cost to go for the rest of the time horizon
                for j in range(i, maxEpisodeLength): # loop from time i until the maxEpLength = end of horizon
                    J += gamma**(j-i) * cost_list[j] # for us this is the present: we solve an infinite horizon problem (there's no begin and no end):
                    # at time j we are at the beginning from our perspective so there is no discounting but only into the future (that's why (j-i)) there will be a cost discount
            '''
            C[x] += J
            V[x] = C[x]/N[x] # update V
            
        # compute V_err as: mean(abs(V-V_real))
        err = np.mean(np.abs(V - V_real))
        V_err.append(err)
        if(k % nprint == 0):
            print("Monte Carlo - Iter. %d, err = %f" % (k, err))
            if(plot): env.plot_V_table(V) # display the V function
    
    return V, V_err

'''
For MC and TD we have no convergence criteria, we run for a certain # of iter. and we wait
'''

def td0_policy_eval(env, gamma, pi, V0, nEpisodes, maxEpisodeLength, 
                    V_real, learningRate, plot=False, nprint=1000):
    ''' TD(0) Policy Evaluation: # we update the V function at each step not at the end of the episode
        env: environment 
        gamma: discount factor
        pi: policy to evaluate
        V0: initial guess for V table
        nEpisodes: number of episodes to be used for evaluation
        maxEpisodeLength: maximum length of an episode
        V_real: real Value table
        learningRate: learning rate of the algorithm
        plot: if True plot the V table every nprint iterations
        nprint: print some info every nprint iterations
        alpha: learning rate
        V is the I.G for the V that we update iteratively
    '''
    
    # make a copy of V0 using np.copy(V0)
    V = np.copy(V0) # just to not modify the passed in input array
    # create a list V__err to store the history of the error between real and estimated V table
    V_err = []
    # for each episode
    for k in range(nEpisodes):
        # reset the environment to a random state (because we don't have the model of the robot)
        env.reset()
        
        # SIMULATING THE SYSTEM WITH GIVEN POLICY pi
        for i in range(maxEpisodeLength):
            # compute the control from the policy
            x = env.x
            if(callable(pi)): # check if policy is a function
                u = pi(env, x)
            else: # check if policy is a vector
                u = pi[x]
                
            # simulate the system using the given policy pi
            x_next, cost = env.step(u)                    
            # at each simulation step update the Value of the current state  
            V[x] += learningRate * (cost + gamma * V[x_next] - V[x])
            
            
        # *** EPISODE HAS FINISHED ***
        
        # compute V_err as: mean(abs(V-V_real))
        err = np.mean(np.abs(V - V_real))
        V_err.append(err)
        if(k % nprint == 0):
            print("TD(0) - Iter. %d, err = %f" % (k, err))
            if(plot): env.plot_V_table(V) # display the V function
    
    return V, V_err


'''
M.C is the best one over TD(0) in the general behaviour
'''