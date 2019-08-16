#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
field.py
'''

class Field:
    '''
    Each communication field allows the agents of the model to communicate
    with each other by storing their emotional expressions. Fields represent
    discussion threads that forum users can participate in, one at a time, and
    that affect their emotional state. It requires the input of the initial
    emotional charge of the field, its impact on agents, and the decay of this
    impact over time.
    '''
    def __init__(self, Charge, Decay, Impact):
        self.charge = Charge # Field variable storing the emotional
                                   # charge of the field
        self.positivity = None
        self.negativity = None
        self.decay = Decay # Constant decay parameter that determines the
                                 # decrease of the field variable over time
        self.impact = Impact # Parameter determining the impact of the
                                   # field on the agents

    def communication(self, Positive_expressions, Negative_expressions):
        '''
        This methods describes how the field variable changes depending on
        user participation and the emotional information they put in. It takes
        two lists of agent expression variables as input, namely a list of all
        positive expressions and a list of all negative expressions.
        '''
        positive_e = len(Positive_expressions) # Total number of all positive
        negative_e = len(Negative_expressions) # and negative expressions

        self.positivity = self.impact * positive_e - self.decay * self.charge
        self.negativity = self.impact * negative_e - self.decay * self.charge
        self.charge = self.positivity + self.negativity
        # Calculating the new field variable using the total number of agent
        # expressions and the decay and impact parameters
