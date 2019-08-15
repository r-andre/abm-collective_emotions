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
    def __init__(self, charge, decay, impact):
        self.fld = charge # Field variable storing the emotional charge
                              # of the field
        self.dcy = decay # Constant decay parameter that determines the
                             # decrease of the field variable over time
        self.impct = impact # Constant determining the impact of the field
                               # on the agents

    def communication(self, positive_expressions, negative_expressions):
        '''
        This methods describes how the field variable changes depending on
        user participation and the emotional information they put in. It takes
        two lists of agent expression variables as input, namely a list of all
        positive expressions and a list of all negative expressions.
        '''
        pos_exp = len(positive_expressions)
        neg_exp = len(negative_expressions)

        pos_fld = self.impct * pos_exp - self.dcy * self.fld
        neg_fld = self.impct * neg_exp - self.dcy * self.fld
        self.fld = pos_fld + neg_fld
        # Calculating the new field variable using the total number of agent
        # expressions and the decay and impact parameters
