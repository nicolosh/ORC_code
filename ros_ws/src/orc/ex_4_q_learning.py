'''
Example of Q-table learning with a simple discretized 1-pendulum environment.
'''

import numpy as np
from dpendulum import DPendulum
from sol.ex_0_policy_evaluation_sol import policy_eval
from sol.ex_4_q_learning_sol import q_learning
#from sol.ex_4_q_learning_sol_prof import q_learning
import matplotlib.pyplot as plt
import time

def render_greedy_policy(env, Q, gamma, x0=None, maxiter=20):
    '''Roll-out from random state using greedy policy.'''
    x0 = x = env.reset(x0)
    costToGo = 0.0
    gamma_i = 1
    for i in range(maxiter):
        u = np.argmin(Q[x,:])
#        print("State", x, "Control", u, "Q", Q[x,u])
        x,c = env.step(u)
        costToGo += gamma_i*c
        gamma_i *= gamma
        env.render()
    print("Real cost to go of state", x0, ":", costToGo)
    
def compute_V_pi_from_Q(env, Q):
    ''' Compute Value table and greedy policy pi from Q table. '''
    V = np.zeros(Q.shape[0])
    pi = np.zeros(Q.shape[0], np.int64)
    for x in range(Q.shape[0]):
#        pi[x] = np.argmin(Q[x,:])
        # Rather than simply using argmin we do something slightly more complex
        # to ensure simmetry of the policy when multiply control inputs
        # result in the same value. In these cases we prefer the more extreme
        # actions
        V[x] = np.min(Q[x,:]) # computes the minimum of Q for that state
        u_best = np.where(Q[x,:]==V[x])[0] # optimal action so it's the policy function
        
        # trying to have a symmetric policy
        if(u_best[0]>env.c2du(0.0)):
            pi[x] = u_best[-1]
        elif(u_best[-1]<env.c2du(0.0)):
            pi[x] = u_best[0]
        else:
            pi[x] = u_best[int(u_best.shape[0]/2)]

    return V, pi


if __name__=='__main__':
    ### --- Random seed
    RANDOM_SEED = int((time.time()%10)*1000)
    print("Seed = %d" % RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    
    ### --- Hyper paramaters
    NEPISODES               = 5000          # Number of training episodes
    NPRINT                  = 500           # print something every NPRINT episodes
    MAX_EPISODE_LENGTH      = 100           # Max episode length
    LEARNING_RATE           = 0.8           # alpha coefficient of Q learning algorithm
    DISCOUNT                = 0.9           # Discount factor 
    PLOT                    = True          # Plot stuff if True
    exploration_prob                = 1     # initial exploration probability of eps-greedy policy (eps defines how often we should explore VS exploit)
    # if eps large (close to 1), we explore a lot because with a large probab. we take a random action / I.G for exploring the Q function
    # if eps small (close to 0), we exploit a lot because we act mainly greedily wrt our Q function
    exploration_decreasing_decay    = 0.001 # exploration decay for exponential decreasing
    min_exploration_prob            = 0.001 # minimum of exploration probability ( we really never go to 0 exploration probability, but we have a 0.001 chance to have a random action)
    
    ### --- Discrete Pendulum Environment
    nq=51   # number of discretization steps for the joint angle q
    nv=21   # number of discretization steps for the joint velocity v
    nu=11   # number of discretization steps for the joint torque u
    env = DPendulum(nq, nv, nu)
    Q   = np.zeros([env.nx,env.nu])       # Q-table initialized to 0
    
    # Q function and history of the cost to go during training (just for plotting)
    Q, h_ctg = q_learning(env, DISCOUNT, Q, NEPISODES, MAX_EPISODE_LENGTH, 
                            LEARNING_RATE, exploration_prob, exploration_decreasing_decay,
                            min_exploration_prob, compute_V_pi_from_Q, PLOT, NPRINT)
    '''
    q learning only computes the optimal Q function not the optimal policy
    '''
    
    print("\nTraining finished")
    V, pi = compute_V_pi_from_Q(env,Q)
    env.plot_V_table(V)
    env.plot_policy(pi)
    print("Average/min/max Value:", np.mean(V), np.min(V), np.max(V)) 
    
    print("Compute real Value function of greedy policy found by the Q learning")
    MAX_EVAL_ITERS    = 200     # Max number of iterations for policy evaluation
    VALUE_THR         = 1e-3    # convergence threshold for policy evaluation
    V_pi = policy_eval(env, DISCOUNT, pi, V, MAX_EVAL_ITERS, VALUE_THR, False) # real value function of real policy pi
    env.plot_V_table(V_pi)
    print("Average/min/max Value:", np.mean(V_pi), np.min(V_pi), np.max(V_pi)) 
        
    # compute real optimal Value function
    print("Compute optimal Value table using policy iteratiton")
    from sol.ex_1_policy_iteration_sol_prof import policy_iteration
    MAX_EVAL_ITERS    = 200     # Max number of iterations for policy evaluation
    MAX_IMPR_ITERS    = 20      # Max number of iterations for policy improvement
    VALUE_THR         = 1e-3    # convergence threshold for policy evaluation
    POLICY_THR        = 1e-4    # convergence threshold for policy improvement
    V_opt  = np.zeros(env.nx)                       # Value table initialized to 0
    pi_opt = env.c2du(0.0)*np.ones(env.nx, np.int64)  # policy table initialized to zero torque
    pi_opt = policy_iteration(env, DISCOUNT, pi_opt, V_opt, MAX_EVAL_ITERS, MAX_IMPR_ITERS, VALUE_THR, POLICY_THR, False, 10000)
    env.plot_V_table(V_opt)
    print("Average/min/max Value:", np.mean(V_opt), np.min(V_opt), np.max(V_opt)) 
    # used to describe how far i am from the optimal policy and optimal value function using Q learning
    '''
    We get an optimal value function which is better than the one computed from the computed policy
    At the end we get a max value (worst case) for the 
    optimal V function, whereas the worst case for our policy is smaller and negative 
    which means that there are states for which our policy is sub-optimal
    with a large gap from the optimal policy but on average it performs quite well!
    For the best case (min value) they perform quite well 
    because we have -10 almost for both.
    
    '''
    render_greedy_policy(env, Q, DISCOUNT) # simulate the system using the policy I just computed
    # render_greedy_policy initializes the pendulum with a random initial state and then
    # simulates it with the policy we computed
    plt.plot( np.cumsum(h_ctg)/range(1,NEPISODES+1) )
    plt.title ("Average cost-to-go")
    plt.show()
    
    # Quality of the policy and the value function is related 
    # on how many episodes we use to run the algorithm, on the learning rate 
    # and the discount factor affect a lot
    # learning rate high ==> no noise basically --> deterministic env
    # discount in theory is not like a tuning parameter for the designer
    # but it's more like the specification of the problem,
    # it changes the problem we are trying to solve, what the optimal policy 
    # is and also the speed of convergence to the optimal policy 
    # Also the exploration probability is important:
    # we need to tune the decay rate of our explor_prob so that towards the end
    # of the # of episodes, eps is very small because at the end we want to be greedy in order to converge 
    # even if at the beginning we want to explore a lot.
    # SO if we change the # of episodes we can also change the decay of eps accordingly
    # to make it slower