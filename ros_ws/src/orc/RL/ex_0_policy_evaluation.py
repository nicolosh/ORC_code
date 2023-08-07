'''
Example of policy evaluation with a simple discretized 1-DoF pendulum:
    policy is fixed and we want to evaluate that policy and we wanna find the V function of that policy
    Vk+1(x) = l(x, pi(x)) + gamma * Vk(f(x, pi(x))) for all the x E X (state space) with f(x, pi(x)) the next state
'''

'''
V = 0 (not reached the goal) so cost = 0
V non 0 ( goal reached :) ) so cost = -1
    
We have different magnitudes inside the V function because the cost gets discounted (gamma discount makes V decreases over time)!
What changes V is how time we take to reach the goal: if reached immediately, we are gonna get 
the cost/reward for the all horizon (infinite), if instead it takes us 5 time steps to reach it then
we have 5 time steps for which we don't get the cost and then we get it only from step 5 onwards.
Discount factor is very important otherwise we have a V infinite for all the states at which we reach the goal.
Value function here is associated to the infinite horizon problem.
If we have a larger gamma but always smaller than 1, then the cost over time and so
to the range of values of V function increases because we discount with a larger value so we discount less.
So also, the convergence of the algorithm is slower with a larger gamma!!!
Also decreasing nq = 21 each iteration of the algorithm is faster

Of course opposite behaviour if we decrease gamma.

'''

import numpy as np
from dpendulum import DPendulum
#from sol.ex_0_policy_evaluation_sol_prof import policy_eval
from sol.ex_0_policy_evaluation_sol import policy_eval

def policy(env, x): # env is a instance of the dpendulum class and x is the state (INTEGER VALUE from now on !!!)
    ''' The fixed policy to be evaluated(heuristic policy for reaching the top 0 configuration) '''
    q, dq = env.d2c(env.i2x(x)) # convert state from discrete to continuous
    if(abs(q) < 2*env.DQ): # if joint position close to zero
        return env.c2du(-kp*q-kd*dq)    # PD control law trying to regulate the system at 0 (top position)
    if(dq > 0): # if velocity is positive
        return env.c2du(env.uMax) # accelerate as much as possible
    if(dq < 0): # if velocity is negative
        return env.c2du(-env.uMax) # decelerate as much as possible
    if(q > 0): # if velocity is null and q > 0
        return env.c2du(env.uMax) # accelerate as much as possible
    return env.c2du(-env.uMax) # if velocity is null and q<=0 decelerate as much as possible


def render_policy(env, pi, x0=None, T=30): # displays how the policy makes the system behave in our viewer
    '''Roll-out (i.e., simulate) from state x0 using policy pi for T time steps'''
    x = env.reset(x0)
    for i in range(T):
        if(callable(pi)):   # if pi is a function
            u = pi(env, x)
        else:   # otherwise assume it's a vector
            u = pi[x]
        x_next,l = env.step(u)
        env.render()
#        q,dq = env.d2c(env.i2x(x))
#        print("u=", u, "%.2f"%env.d2cu(u), "x", x, "q=%.3f"%q, 
#              "dq=%.3f"%dq, "ddq=%.3f"%env.pendulum.a[0])
#        if l!=0: print('Cost not zero!');
        x = x_next


if __name__=="__main__":    
    ### --- Hyper paramaters
    MAX_ITERS         = 200         # Max number of iterations
    CONVERGENCE_THR   = 1e-4        # convergence threshold (difference between V at the next iteration and V at current iteration)
    NPRINT            = 5           # Print info every NPRINT iterations
    PLOT              = True        # Plot the V table
    DISCOUNT          = 0.9      # Discount factor 
    
    ### --- Environment
    nq=51   # number of discretization steps for the joint angle q
    nv=21   # number of discretization steps for the joint velocity v
    nu=11   # number of discretization steps for the joint torque u
    env = DPendulum(nq, nv, nu) # create the environment
    kd = 1.0/env.dt             # derivative gain used in the control policy
    kp = kd**2 / 2              # proportional gain used in the control policy (gives me a critical damped if applied to a LinDynSys)
    V  = np.zeros([env.nx])     # V-table initialized to 0 (initial guess)
    
    # display policy behavior
#    render_policy(env, policy)
    
    V = policy_eval(env, DISCOUNT, policy, V, MAX_ITERS, CONVERGENCE_THR, PLOT, NPRINT)
    