#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
agent.py
'''

class Agent:
    '''
    Each agent represents one forum user and is defined by its emotional state
    that is stored in the valence and arousal variables. Valence indicates
    whether their emotional state is positive or negative, while arousal
    indicates the strength of that emotion.
    '''
    def __init__(self):
        self.valence = 1
        self.arousal = 1
        self.temperament = 1 # Arousal threshold that determines if/when an
                             # agent communicates its emotions

    def perception(self, field):
        '''
        This method describes how agents perceive their field, how the field
        affects their emotional states, and returns the changed emotion
        variable.
        '''
        self.valence = self.valence + field  # Equations of how valence and
        self.arousal = self.arousal + field  # arousal are affected by the
                                             # field variable

    def expression(self):
        '''
        This method describes how agents express their emotions to fields,
        communicating and spreading emotional information to other agents when
        their arousal reaches its threshold value.
        '''
        if self.arousal > self.temperament: # The expression variable only
            expression = self.valence       # returns a value if the arousal
        else:                               # threshold is reached
            expression = None

        return expression # Returning the expression variable or None when the
                          # arousal did not exceed the threshold

    def relaxation(self):
        '''
        This methods describes how the the emotional state of agents returns
        to a baseline after the emotions are expressed to others.
        '''
        self.valence = self.valence - 1 # Equations of how valence and arousal
        self.arousal = self.arousal - 1 # regress over time and/or after the
                                        # expression of emotions
