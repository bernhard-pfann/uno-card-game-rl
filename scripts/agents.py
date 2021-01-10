# 1. Libraries
# -------------------------------------------------------------------------

# Custom libraries
import state_action_reward as sar

# Public libraries
import pandas as pd
import numpy as np
import random


# 2. Q-Learning
# -------------------------------------------------------------------------

class QLearningAgent(object):
    
    def agent_init(self, agent_init_info):
        
        # (1) Store the parameters provided in agent_init_info
        self.states      = sar.states()
        self.actions     = sar.actions()
        self.epsilon     = agent_init_info["epsilon"]
        self.step_size   = agent_init_info["step_size"]
        self.gamma       = agent_init_info["gamma"]
        self.q_exist     = agent_init_info["q_exist"]
        
        self.prev_state  = 0
        self.prev_action = 0
        
        self.R = sar.rewards(self.states, self.actions)
        
        # (2) Create Q-table that stores action-value estimates, initialized at zero
        if self.q_exist == False:
            self.q = pd.DataFrame(data    = np.zeros((len(self.states), len(self.actions))), 
                                  columns = self.actions, 
                                  index   = self.states)
            
            self.q_visit = self.q.copy()
            
        else: self.existing_q()

            
    def existing_q(self):
        
        # Import already existing Q-values table
        self.q            = pd.read_csv("02 Extracts/q_table.csv", sep = ";", index_col = "Unnamed: 0")
        self.q.index      = self.q.index.map(lambda x: eval(x))
        self.q["IDX"]     = self.q.index
        self.q            = self.q.set_index("IDX", drop = True)
        self.q.index.name = None
    
        # Import already existing Q-visits table
        self.q_visit            = pd.read_csv("02 Extracts/q_visit.csv", sep = ";", index_col = "Unnamed: 0")
        self.q_visit.index      = self.q_visit.index.map(lambda x: eval(x))
        self.q_visit["IDX"]     = self.q_visit.index
        self.q_visit            = self.q_visit.set_index("IDX", drop = True)
        self.q_visit.index.name = None
    
    
    
    def step(self, state_dict, actions_dict):
        
        # (1) Transform state dictionary into tuple
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        # (2) Choose action using epsilon greedy
        if random.random() < self.epsilon:
            
            actions_possible = [key for key,val in actions_dict.items() if val != 0]         
            action = random.choice(actions_possible)
        
        else:
            actions_possible = [key for key,val in actions_dict.items() if val != 0]
            random.shuffle(actions_possible)
            val_max = 0
            
            for i in actions_possible:
                val = self.q.loc[[state],i][0]
                if val >= val_max: 
                    val_max = val
                    action = i
        
        return action
    
    
    def update(self, state_dict, action):
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        if self.prev_state != 0:
            prev_q = self.q.loc[[self.prev_state], self.prev_action][0]
            this_q = self.q.loc[[state], action][0]
            reward = self.R.loc[[state], action][0]
            
            print ("\n")
            print (f'prev_q: {prev_q}')
            print (f'this_q: {this_q}')
            print (f'prev_state: {self.prev_state}')
            print (f'this_state: {state}')
            print (f'prev_action: {self.prev_action}')
            print (f'this_action: {action}')
            print (f'reward: {reward}')
            
            if reward == 0:
                self.q.loc[[self.prev_state], self.prev_action] = prev_q + self.step_size * (reward + this_q - prev_q) 
            else:
                self.q.loc[[self.prev_state], self.prev_action] = prev_q + self.step_size * (reward - prev_q)
                
            self.q_visit.loc[[self.prev_state], self.prev_action] += 1
            
        # Save and return action/state
        self.prev_state  = state
        self.prev_action = action


# 3. Monte Carlo
# -------------------------------------------------------------------------       
        
class MonteCarloAgent(object):

    def agent_init(self, agent_init_info):
        
        # (1) Store the parameters provided in agent_init_info
        self.states      = sar.states()
        self.actions     = sar.actions()
        self.epsilon     = agent_init_info["epsilon"]
        self.step_size   = agent_init_info["step_size"]
        self.gamma       = agent_init_info["gamma"]
        self.q_exist     = agent_init_info["q_exist"]
        
        self.state_seen = list()
        self.action_seen = list()
        self.q_seen = list()
        self.R = sar.rewards(self.states, self.actions)
        
        # (2) Create Q-table that stores action-value estimates, initialized at zero
        if self.q_exist == False:
            self.q = pd.DataFrame(data    = np.zeros((len(self.states), len(self.actions))), 
                                  columns = self.actions, 
                                  index   = self.states)
            
            self.q_visit = self.q.copy()
            
        else: self.existing_q()
            
            
    def existing_q(self):
        
        # Import already existing Q-values table
        self.q            = pd.read_csv("02 Extracts/q_table.csv", sep = ";", index_col = "Unnamed: 0")
        self.q.index      = self.q.index.map(lambda x: eval(x))
        self.q["IDX"]     = self.q.index
        self.q            = self.q.set_index("IDX", drop = True)
        self.q.index.name = None
    
        # Import already existing Q-visits table
        self.q_visit            = pd.read_csv("02 Extracts/q_visit.csv", sep = ";", index_col = "Unnamed: 0")
        self.q_visit.index      = self.q_visit.index.map(lambda x: eval(x))
        self.q_visit["IDX"]     = self.q_visit.index
        self.q_visit            = self.q_visit.set_index("IDX", drop = True)
        self.q_visit.index.name = None

    
    def step(self, state_dict, actions_dict):
        
        # (1) Transform state dictionary into tuple
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        # (2) Choose action using epsilon greedy
        if random.random() < self.epsilon:
            
            actions_possible = [key for key,val in actions_dict.items() if val != 0]         
            action = random.choice(actions_possible)
        
        else:
            actions_possible = [key for key,val in actions_dict.items() if val != 0]
            random.shuffle(actions_possible)
            val_max = 0
            
            for i in actions_possible:
                val = self.q.loc[[state],i][0]
                if val >= val_max: 
                    val_max = val
                    action = i
        
        
        if ((state),action) not in self.q_seen:
            self.state_seen.append(state)
            self.action_seen.append(action)
        
        self.q_seen.append(((state),action))
        self.q_visit.loc[[state], action] += 1
        
        return action
    
    
    def update(self, state_dict, action):
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        reward = self.R.loc[[state], action][0]
        
        for s,a in zip(self.state_seen, self.action_seen): 
            self.q.loc[[s], a] += self.step_size * (reward - self.q.loc[[s], a])
            print (self.q.loc[[s],a])
        
        self.state_seen, self.action_seen, self.q_seen = list(), list(), list()