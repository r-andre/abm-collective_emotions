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
Time_steps = 15 # ...time steps that each model run goes through

####################
# MODEL PARAMETERS #
####################

Agent_baseline = [0.1, 0.8] # First value is valence baseline, second value
                            # is the arousal baseline of each agent
Agent_threshold = [0.1, 1.1] # Agent thresholds will be calculated as a random
                             # float value between the two entered values using
                             # a uniform distribution
Agent_decay = [0.5, 0.9] # First value sets the valence decay, second value
                         # sets the arousal decay of the agents
Agent_amplitude = [0.3, 0.3] # First value is the amplitude of the
                             # stochasticity for valence, second for arousal
Agent_down_regulation = 0.4 # Sets the coefficient used to down-regulate
                            # valence and arousal after emotional expressions

Field_charge = 0 # Sets the initial emotional charge of the field
Field_decay = 0.7 # Decay of the field charge over time
Field_impact = 0.1 # Impact of the field on the emotional states of agents

Valence_coefficient = [0, 1, 0, -1]     # Coefficients 1, 2, 3, and 4 that
Arousal_coefficient = [0.05, 0.5, 0, 0] # determine how valence/arousal change
                                        # after agents perceive the field 

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
                                          Agent_decay)
