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
    that affect their emotional state.
    '''
    def __init__(self):
        self.variable = 1 # Stores the value of the communication field, an
                          # aggregation of all agent expressions

    def communication(self, expression):
        '''
        This methods describes how the field variable changes depending on
        user participation and the emotional information they put in.
        '''
        if expression:
            self.variable += expression # Equation of the field variable
                                        # changing according to the aggregate
                                        # of agent expressions
        else:
            pass
