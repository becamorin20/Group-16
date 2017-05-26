#
#
# Zombie-Maze-Land
# CS 175
# Edison Weik
#
# q_approximation_coarse.py
#
# Implements Q-learning algorithm with function approximation, 9 coarse stationary circular
# basis functions and 9 dynamic basis functions. (See github page for more info.)
# Used by zombie_maze.py for learning algorithm
#



import MalmoPython
import logging
import time
import math
import sys
import json
import random
from datetime import datetime
import numpy as np

####### SET OF ALL BASIS FUNCTIONS ######
def p1( agent, z1, z2, z3 ):
    def in_partition( z ):
        return int(-4.5 < agent[0]-z[0] < -1.5 and 1.5 < agent[1]-z[1] < 4.5)
    return in_partition(z1) + in_partition(z2) + in_partition(z3)   

def p2( agent, z1, z2, z3 ):
    def in_partition( z ):
        return int(-1.5 < agent[0]-z[0] < 1.5 and 1.5 < agent[1]-z[1] < 4.5)
    return in_partition(z1) + in_partition(z2) + in_partition(z3)
    
def p3( agent, z1, z2, z3 ):
    def in_partition( z ):
        return int(1.5 < agent[0]-z[0] < 4.5 and 1.5 < agent[1]-z[1] < 4.5)
    return in_partition(z1) + in_partition(z2) + in_partition(z3) 
    
def p4( agent, z1, z2, z3 ):
    def in_partition( z ):
        return int(-4.5 < agent[0]-z[0] < -1.5 and -1.5 < agent[1]-z[1] < 1.5)
    return in_partition(z1) + in_partition(z2) + in_partition(z3)    

def p5( agent, z1, z2, z3 ):
    def in_partition( z ):
        return int(abs(agent[0]-z[0]) <= 1.5 and abs(agent[1]-z[1]) <= 1.5)
    return in_partition(z1) + in_partition(z2) + in_partition(z3)
    
def p6( agent, z1, z2, z3 ):
    def in_partition( z ):
        return int(1.5 < agent[0]-z[0] < 4.5 and -1.5 < agent[1]-z[1] < 1.5)
    return in_partition(z1) + in_partition(z2) + in_partition(z3)
    
def p7( agent, z1, z2, z3 ):
    def in_partition( z ):
        return int(-4.5 < agent[0]-z[0] < -1.5 and -4.5 < agent[1]-z[1] < -1.5)
    return in_partition(z1) + in_partition(z2) + in_partition(z3) 
    
def p8( agent, z1, z2, z3 ):
    def in_partition( z ):
        return int(-1.5 < agent[0]-z[0] < 1.5 and -4.5 < agent[1]-z[1] < -1.5)
    return in_partition(z1) + in_partition(z2) + in_partition(z3)
    
def p9( agent, z1, z2, z3 ):
    def in_partition( z ):
        return int(1.5 < agent[0]-z[0] < 4.5 and -4.5 < agent[1]-z[1] < -1.5)
    return in_partition(z1) + in_partition(z2) + in_partition(z3) 
    

def a1( agent ):
    ''' Circle with center (-2.5,2.5) and radius 2.5 '''
    x = agent[0]
    z = agent[1]
    return 1 if (-2.5-x)**2 + (2.5-z)**2 < 6.25 else 0
    
def a2( agent ):
    ''' Circle with center (-5.5,2.5) and radius 2.5'''
    x = agent[0]
    z = agent[1]
    return 1 if (-5.5-x)**2 + (2.5-z)**2 < 6.25 else 0
    
def a3( agent ):
    ''' Circle with center (-8.5,2.5) and radius 2.5'''
    x = agent[0]
    z = agent[1]
    return 1 if (-8.5-x)**2 + (2.5-z)**2 < 6.25 else 0

def a4( agent ):
    ''' Circle with center (-2.5,-0.5) and radius 2.5'''
    x = agent[0]
    z = agent[1]
    return 1 if (-2.5-x)**2 + (-.5-z)**2 < 6.25 else 0
    
def a5( agent ):
    ''' Circle with center (-5.5,-0.5) and radius 2.5'''
    x = agent[0]
    z = agent[1]
    return 1 if (-5.5-x)**2 + (-.5-z)**2 < 6.25 else 0

def a6( agent ):
    ''' Circle with center (-8.5,-0.5) and radius 2.5'''
    x = agent[0]
    z = agent[1]
    return 1 if (-8.5-x)**2 + (-.5-z)**2 < 6.25 else 0

def a7( agent ):
    ''' Circle with center (-2.5,-3.5) and radius 2.5'''
    x = agent[0]
    z = agent[1]
    return 1 if (-2.5-x)**2 + (-3.5-z)**2 < 6.25 else 0  
    
def a8( agent ):
    ''' Circle with center (-5.5,-3.5) and radius 2.5'''
    x = agent[0]
    z = agent[1]
    return 1 if (-5.5-x)**2 + (-3.5-z)**2 < 6.25 else 0   
    
def a9( agent ):
    ''' Circle with center (-8.5,-3.5) and radius 2.5'''
    x = agent[0]
    z = agent[1]
    return 1 if (-8.5-x)**2 + (-3.5-z)**2 < 6.25 else 0 



class Agent(object):
    def __init__(self):
        """Constructing an RL agent.
            alpha:  <float>  learning rate      
            gamma:  <float>  value decay rate   
            epsilon:<float>  chance of taking a random action instead of the best
            lambda:<float>   weight of update effect for backups for previously visited states
        """
        self.episodes = 0
        self.epsilon = 0.1
        self.gamma = 0.9
        self.alpha = 0.005
        self.lambda_ = 0.9
        self.theta = [ 0 for i in range(72) ]
        self.basis = [ 0 for i in range(72) ]
        self.e_vector = [ 0 for i in range(72) ]
        self.possible_actions = [ 'movenorth 1', 'movesouth 1', 'movewest 1', 'moveeast 1' ]
        
        
    def update_parameters( self, agent_host, action, reward ):
        '''
        Updates parameters of Q-function with gradient descent TD(lambda).
        '''
        ## Observe new state
        new_agent, new_z1, new_z2, new_z3 = self.observe_state( agent_host )
        
        ## Get max q-estimate for next state-action
        q_estimate = -sys.maxint
        for a in self.possible_actions:
            q_val = self.get_q_approx( new_agent, new_z1, new_z2, new_z2, a )
            if q_val >= q_estimate:
                q_estimate = q_val
        
        ## Get q value and basis vector for current state-action
        current_q = self.get_q_approx( self.agent, self.z1, self.z2, self.z3, action )
        basis = self.get_basis( self.agent, self.z1, self.z2, self.z3, action )

        ## Update parameters
        delta = reward + self.gamma*q_estimate - current_q
        self.e_vector = [ self.gamma * self.lambda_ * e + phi for e, phi in zip(self.e_vector, basis) ]
        self.theta = [ theta + self.alpha*delta*e for theta,e in zip(self.theta, self.e_vector) ]
        

    def update_parameters_from_terminal(self, action, reward):
        '''
        Updates parameters of Q-function from terminal state with gradient descent TD(lambda).
        '''
        ## Get q value, basis vector, and eligibility trace vector for current state-action
        current_q = self.get_q_approx(self.agent, self.z1, self.z2, self.z3, action)
        basis = self.get_basis(self.agent, self.z1, self.z2, self.z3, action)
        e_vector = [ self.gamma*self.lambda_*i + j for i,j in zip(self.e_vector, basis) ]
        
        ## Update parameters
        delta = reward - current_q
        new_theta = [ theta + self.alpha*delta*e  for theta,e in zip(self.theta, e_vector) ]
        self.theta = new_theta

        
    def get_basis( self, agent, z1, z2, z3, action ):
        ''' Get basis vector for q approximation with state-action input.
        72 features represent state-action basis function.
         For 4 actions, 18 state features that represent:
         First 18 represent states for 'movenorth 1'
         Second 18 represent states for 'movesouth 1'
         Third 18 represent states for 'movewest 1'
         Fourth 18 represent states for 'moveeast 1'
        '''
        self.basis = [ 0 for i in range(72) ]
        for i in range(4):
            condition = self.possible_actions[i]==action
            self.basis[0 + i*18] = p1(agent, z1, z2, z3) if condition else 0
            self.basis[1 + i*18] = p2(agent, z1, z2, z3) if condition else 0
            self.basis[2 + i*18] = p3(agent, z1, z2, z3) if condition else 0
            self.basis[3 + i*18] = p4(agent, z1, z2, z3) if condition else 0
            self.basis[4 + i*18] = p5(agent, z1, z2, z3) if condition else 0
            self.basis[5 + i*18] = p6(agent, z1, z2, z3) if condition else 0
            self.basis[6 + i*18] = p7(agent, z1, z2, z3) if condition else 0
            self.basis[7 + i*18] = p8(agent, z1, z2, z3) if condition else 0
            self.basis[8 + i*18] = p9(agent, z1, z2, z3) if condition else 0
            self.basis[9 + i*18] = a1(agent) if condition else 0
            self.basis[10 + i*18] = a2(agent) if condition else 0
            self.basis[11 + i*18] = a3(agent) if condition else 0
            self.basis[12 + i*18] = a4(agent) if condition else 0
            self.basis[13 + i*18] = a5(agent) if condition else 0
            self.basis[14 + i*18] = a6(agent) if condition else 0
            self.basis[15 + i*18] = a7(agent) if condition else 0
            self.basis[16 + i*18] = a8(agent) if condition else 0
            self.basis[17 + i*18] = a9(agent) if condition else 0
        return self.basis
       
        
    def get_q_approx(self, agent, z1, z2, z3, action):
        '''
        Get Q-function approximation value with state-action input
        '''
        basis = self.get_basis(agent, z1, z2, z3, action)
        inner_product = sum( [ i*j for i,j in zip( basis, self.theta ) ] )
        return inner_product
                
    
    def get_action(self):
        '''
        Output:  action chosen with epsilon-greedy probability with current state
        '''
        random.seed(datetime.now())
        rnd = random.random()
        if rnd < self.epsilon:
            a = random.randint(0, 3)
            self.x = self.possible_actions
            return self.possible_actions[a]
        else:
            max_q = -sys.maxint
            actions = []
            for a in self.possible_actions:
                q_val = self.get_q_approx( self.agent, self.z1, self.z2, self.z3, a )
                x[a] = q_val
                if q_val == max_q:
                    actions.append( a )
                    max_q = q_val
                if q_val > max_q:
                    actions = []
                    actions.append( a )
                    max_q = q_val
            y = 0 if len(actions)==1 else random.randint(0, len(actions)-1)
            return actions[y]
    
    
    def check_health(self, health, world_state):
        '''
        Checks health of agent. Exits episode if health falls below 20.0. 
        '''
        if health < 20.0:
            self.alive = False
    
    
    def observe_state( self, agent_host ):
        '''
        Takes in agent_host.
        Observe state.
        Check if health is diminished.
        Return 4 2-tuples of current positions of entities.
        '''
        world_state = agent_host.getWorldState()
        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                observations = json.loads(msg)
                self.check_health( observations[u'Life'], world_state )
                state = observations.get(u'zombies', 0)
                break
        agent = ( state[0][u'x'], state[0][u'z'] )
        z1 = ( state[1][u'x'], state[1][u'z'] )
        z2 = ( state[2][u'x'], state[2][u'z'] )
        z3 = ( state[3][u'x'], state[3][u'z'] )
        return agent, z1, z2, z3


    def act(self, agent_host, current_r):
        '''
        Take 1 action in response to the current world state and update paramters.
        '''
        # Observe current state
        try:
            self.agent, self.z1, self.z2, self.z3 = self.observe_state( agent_host )
        except:
            return 0

        # Act on observation and update parameters
        self.action = self.get_action()
        try:
            agent_host.sendCommand( self.action )
            self.update_parameters( agent_host, self.action, current_r )
        except:
            return 0
            
        return current_r
        
    def update_hyperparameters(self):
        '''
        Update hyperparameters epsilon and alpha of q learner as time progress.
        '''
        self.episodes += 1
        #eps_evolution = { 1:0.1, 100:0.05, 200:0.01, 400:0.005, 450:0.001 }
        #alpha_evolution = { 1:0.005, 100:0.001, 200:0.0005, 300:0.0001 }
        eps_evolution = { 1:0.1, 50:0.05, 75:0.01 }
        alpha_evolution = { 1:0.005, 25:0.001, 50:0.0005, 75:0.0001 }
        if self.episodes in eps_evolution.keys():
            self.epsilon = eps_evolution[ self.episodes ]
        if self.episodes in alpha_evolution.keys():
            self.alpha = alpha_evolution[ self.episodes ]
        

    def run(self, agent_host):
        '''
        Run the agent on the world for 1 episode. 
        '''
        # Observe initial state and set variables for episode
        self.alive = True
        self.update_hyperparameters()
        self.e_vector = [ 0 for i in range(72) ]
        self.reward = 0
        total_reward, total_commands = 0, 0
        self.agent, self.z1, self.z2, self.z3, self.action = None, None, None, None, None
        
        # Take first action
        while True:
            world_state = agent_host.getWorldState()
            if world_state.is_mission_running and len(world_state.observations)>0:
                total_reward += self.act(agent_host, self.reward)
                total_commands += 1
                break
            if not world_state.is_mission_running:
                break
        
        # Loop until mission ends:
        while world_state.is_mission_running and self.alive:
            self.reward = 0
            while True:
                time.sleep(0.1)
                world_state = agent_host.getWorldState()
                for reward in world_state.rewards:
                    self.reward += reward.getValue()
                if world_state.is_mission_running and self.alive and len(world_state.observations)>0 and not world_state.observations[-1].text=="{}":
                    total_reward += self.act(agent_host, self.reward)
                    #print "Action: ", self.action, ", reward: ", self.reward
                    total_commands += 1
                    break
                if not world_state.is_mission_running or not self.alive:
                    break
            
            
        # Process final reward and update parameters
        i = 0
        while (self.reward==0):
            i += 1
            if i == 100:
                self.reward = -1000.
            for reward in world_state.rewards:
                self.reward += reward.getValue()
        total_reward += self.reward
        self.update_parameters_from_terminal( self.action, self.reward )
        return total_reward, total_commands


