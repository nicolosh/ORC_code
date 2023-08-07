#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 23:56:07 2021

@author: adelprete
"""
import numpy as np
from numpy.random import randint, uniform

def sarsa(env, gamma, Q, pi, nIter, nEpisodes, maxEpisodeLength, 
          learningRate, exploration_prob, exploration_decreasing_decay,
          min_exploration_prob, compute_V_pi_from_Q, plot=False, nprint=1000):
    ''' SARSA:
        env: environment 
        gamma: discount factor
        Q: initial guess for Q table
        pi: initial guess for policy
        nIter: number of iterations of the algorithm
        nEpisodes: number of episodes to be used for policy evaluation
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
    
    h_ctg = [] # Cost-to-go during learning (for plot).
    # Make a copy of the initial Q table guess
    Q = np.copy(Q) # to not modify the given in input Q
    nEp = 0 # number of episodes
    for k in range(nIter): # for every iteration
        # evaluate the current policy with TD(0)
        # for every episode
        for j in range(nEpisodes):
            nEp += 1
            # reset the state
            env.reset() # reset the state to a random value
            J = 0
            gamma_to_the_i = 1
            # simulate the system for maxEpisodeLength steps
            for i in range(maxEpisodeLength):
                x = env.x 
                if(uniform() < exploration_prob): # with probability exploration_prob take a random control input
                    u = randint(0, env.nu)
                else: # otherwise take a greedy control so we take the action from the policy pi
                    u = pi[x]
                
                # simulate the system
                x_next, cost = env.step(u)
                # Compute reference Q-value at state x: made a step in env, I can update my Q value estimate using Q-learning eq.
                delta = cost + gamma * Q[x_next, pi[x_next]] - Q[x,u] # PD error = delta = cost + gamma * minimum of Q for the next state - Q current value
                # being doing eps-greedy I do what my policy would do (policy evaluation)
                # Update Q-Table with the given learningRate
                Q[x,u] += learningRate * delta
                
                # keep track of the cost to go
                J += gamma_to_the_i * cost # we take increasing powers of gamma to discount cost coming later into the future
                gamma_to_the_i *= gamma
                
            # *** episode end
            h_ctg.append(J) # appending the cost to the list of history of cost to go
        
            # update the exploration probability with an exponential decay: 
            # eps = exp(-decay*episode)
            exploration_prob = np.exp(-exploration_decreasing_decay*nEp)
            # saturation of having a chance to explore a bit always
            exploration_prob = max(exploration_prob, min_exploration_prob)

            # use the function compute_V_pi_from_Q(env, Q) to compute and plot V and pi
            if(nEp % nprint == 0):
                print("SARSA - Episode %d, J = %.1f, eps = %.1f" % (nEp, J, 100*exploration_prob))
                if(plot):
                    V, pi = compute_V_pi_from_Q(env, Q)
                    env.plot_V_table(V)
                    env.plot_policy(pi)
        
        # *** POLICY IMPROVEMENT PHASE ***
        # improve policy by being greedy wrt Q
        for x in range(env.nx):
            pi[x] = np.argmin(Q[x,:]) # take the control minimizing Q function
        

    return Q, h_ctg