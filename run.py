#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
run.py
'''

import model as cyberemotions # Module

####################
# PRIMARY SETTINGS #
####################
'''These variables set a) the number of agents in the model, b) the number of
time steps each model run goes through before the simulation ends, and c) the
the number of times the model is run. Their values must be positive integers,
which may be chosen arbitrarily.'''

# Number of...
Agents = 10 # ...agents in the model
Model_runs = 1 # ...model runs
Time_steps = 10 # ...time steps that each model run goes through

####################
# MODEL PARAMETERS #
####################

Agent_baseline = [0, 0]
Agent_threshold = [0.1, 1.1]
Agent_decay = [0.5, 0.9]
Agent_amplitude = [0.3, 0.3]
Agent_down_regulation = 0.4

Field_charge = 0.5
Field_decay = 0.7
Field_impact = 0.1

Valence_coefficient = [0, 1, 0, -1]
Arousal_coefficient = [0.05, 0.5, 0, 0]


#####################
# RUNNING THE MODEL #
#####################
'''The model runs a set number of times, each run initializing the number of
agents specified in the settings and running for the set number of time
steps before the simulation ends.'''

for model_run in range(Model_runs):
    cyberemotions.Model(Agents,
                        Agent_baseline,
                        Agent_threshold,
                        Field_charge,
                        Field_decay,
                        Field_impact).run(Time_steps,
                                          Valence_coefficient,
                                          Arousal_coefficient,
                                          Agent_amplitude,
                                          Agent_down_regulation,
                                          Agent_decay,)
