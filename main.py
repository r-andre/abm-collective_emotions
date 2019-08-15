#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
main.py
'''

#import random
#import numpy
import model
#import settings
#import agent as agt
#import field as fld

############
# SETTINGS #
############

N_AGENTS = 1 # Number of agents in the model
#N_FIELDS = 1 # Number of communication fields in the model
T_STEPS = 10 # Number of time steps the model goes through
M_RUNS = 1   # Number of model runs

##################
# INITIALIZATION #
##################

#def initialize_agents(number_agents, number_fields):
#    '''
#    This function sets up the model by creating the specified number of agents
#    and returns a list of instances of the Agent class.
#    '''
#    agent_list = [agt.Agent() for agent in range(number_agents)]
#    field_list = [fld.Field() for field in range(number_fields)]

#A_LIST = [agt.Agent() for agent in range(N_AGENTS)] # Creating a list of the
                                                    # set number of agents
                                                    # (instances of the Agent
                                                    # class)
#FIELD = fld.Field() # Creating the field

#####################
# RUNNING THE MODEL #
#####################

#def run_model(time_steps, agents, field):
#    '''
#    This function runs the model using the above settings. Each model run
#    creates a list of agents that go through the set number of time steps. At
#    every step, each agent may or may not communicate its emotions by changing
#    its field and adjusts its emotional state accordingly.
#    '''
#    for step in range(time_steps):
#        for agent in agents:
#            exp = agent.expression()
#            if exp:
#                field.communication(exp)
#            else:
#                pass
#            agent.relaxation()
#        print(step)

#run_model(T_STEPS, A_LIST, FIELD)
for run in range(M_RUNS):
    model.Model(N_AGENTS).run(T_STEPS)
