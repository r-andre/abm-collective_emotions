#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
run.py
'''

import model as cyberemotions # Module

############
# SETTINGS #
############
'''These variables set a) the number of agents in the model, b) the number of
time steps each model run goes through before the simulation ends, and c) the
the number of times the model is run. Their values must be positive integers,
which may be chosen arbitrarily.'''

# Number of...
agents = 1 # ...agents in the model
time_steps = 10 # ...time steps the each model run goes through
model_runs = 1 # ...model runs

#####################
# RUNNING THE MODEL #
#####################
'''The model runs a set number of times, each run initializing the number of
agents specified in the settings and running for the set number of time
steps before the simulation ends.'''

for model_run in range(model_runs):
    cyberemotions.Model(agents).run(time_steps)
