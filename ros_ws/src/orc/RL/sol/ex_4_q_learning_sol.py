#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 23:56:07 2021

@author: adelprete
"""
import numpy as np
from numpy.random import randint, uniform

def q_learning(env, gamma, Q, nEpisodes, maxEpisodeLength, 
               learningRate, exploration_prob, exploration_decreasing_decay,
               min_exploration_prob, compute_V_pi_from_Q, plot=False, nprint=1000):
    ''' Q learning algorithm:
        env: environment 
        gamma: discount factor
        Q: initial guess for Q table
        nEpisodes: number of episodes to be used for evaluation
        maxEpisodeLength: maximum length of an episode
        learningRate: learning rate of the algorithm
        exploration_prob: initial exploration probability for epsilon-greedy policy
        exploration_decreasing_decay: rate of exponential decay of exploration prob
        min_exploration_prob: lower bound of exploration probability
        compute_V_pi_from_Q: function to compute V and pi from Q
        plot: if True plot the V table every nprint iterations
        nprint: print some info every nprint iterations
    '''
    # Keep track of the cost-to-go history (for plot)
    h_ctg = []
    # Make a copy of the initial Q table guess
    Q = np.copy(Q) # to not modify the given in input Q
    # for every episode
    for k in range(nEpisodes):
        # reset the state
        env.reset() # reset the state to a random value
        J = 0
        gamma_to_the_i = 1
        # simulate the system for maxEpisodeLength steps
        for i in range(maxEpisodeLength):
            x = env.x
            # with probability exploration_prob take a random control input
            if(uniform() < exploration_prob):
                u = randint(0, env.nu)
            # otherwise take a greedy control so we take the action minimizing the Q function
            else:
                u = np.argmin(Q[x,:])
            
            # simulate the system
            x_next, cost = env.step(u)
            # Compute reference Q-value at state x: made a step in env, I can update my Q value estimate using Q-learning eq.
            delta = cost + gamma * np.min(Q[x_next,:]) - Q[x,u] # PD error = delta = cost + gamma * minimum of Q for the next state - Q current value
            # Update Q-Table with the given learningRate
            Q[x,u] += learningRate * delta
            
            # keep track of the cost to go
            J += gamma_to_the_i * cost # we take increasing powers of gamma to discount cost coming later into the future
            gamma_to_the_i *= gamma
            
        # *** episode end
        h_ctg.append(J) # appending the cost to the list of history of cost to go
        
        # update the exploration probability with an exponential decay: 
        # eps = exp(-decay*episode)
        exploration_prob = np.exp(-exploration_decreasing_decay*k)
        # saturation of having a chance to explore a bit always
        exploration_prob = max(exploration_prob, min_exploration_prob)
        # use the function compute_V_pi_from_Q(env, Q) to compute and plot V and pi
        if(k % nprint == 0):
            print("Q learning - Iter %d, J = %.1f, eps = %.1f" % (k, J, 100*exploration_prob))
            if(plot):
                V, pi = compute_V_pi_from_Q(env, Q)
                env.plot_V_table(V)
                env.plot_policy(pi)
    
    return Q, h_ctg