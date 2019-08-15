#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
agent.py
'''

import random
import numpy as np

class Agent:
    '''
    Each agent represents one forum user and is defined by its emotional state
    that is stored in the valence and arousal variables. Valence indicates
    whether their emotional state is positive or negative, while arousal
    indicates the strength of that emotion.
    '''
    def __init__(self, amplitude, threshold, constant, decay):
        self.vbsln = 0.1
        self.absln = 0.1
        self.vlnc = self.vbsln
        self.arsl = self.absln
        self.ampltd = amplitude
        self.thrshld = threshold # Arousal threshold that determines if/when an
                                     # agent communicates its emotions
        self.cnstnt = constant
        self.dcy = decay

    def perception(self, field):
        '''
        This method describes how agents perceive their field, how the field
        affects their emotional states, and returns the changed emotion
        variable given the input field variable and a stochastic component
        represented by a random number. The impact of the latter is determined
        by the amplitude parameter of the agent.
        '''
        x = 1
        y = 1
        Fv = field * (x + x * self.vlnc + x * self.vlnc ** 2 + x * self.vlnc ** 3)
        Fa = field * (y + y * self.arsl + y * self.arsl ** 2 + y * self.arsl ** 3)

        stochasticity = random.randint(-100, 100) / 100

        self.vlnc = Fv + self.ampltd * stochasticity
        self.arsl = Fa + self.ampltd * stochasticity
        # Equations describing how valence and arousal are affect by field
        # variable and stochastic factors

    def expression(self):
        '''
        This method describes the information agents express to the field and
        when. When their arousal reaches their internal threshold value, they
        communicate the sign of their valence, the information whether they
        are in a positive or negative emotional state. After they communicate
        this by storing the information in the expression variable, their
        valence and arousal are both immediately down-regulated.
        '''
        if self.arsl >= self.thrshld:
            expression = np.sign(self.vlnc)
            self.vlnc = (self.vlnc - self.vbsln) * self.cnstnt + self.vbsln
            self.arsl = (self.arsl - self.absln) * self.cnstnt + self.absln
            # Equations describing an immediate down-regulation of valence and
            # arousal after an emotional expression
        else:
            expression = None
        # The expression variable only returns a value (the sign of valence)
        # if the arousal threshold is reached

        return expression # Returning the expression variable or None when the
                          # arousal did not exceed the threshold

    def relaxation(self):
        '''
        This methods describes how the the emotional state of agents relaxes
        towards its baseline over time according to the internal decay
        paramater, independently of whether or not an emotion was expressed.
        '''
        regression_v = (-1) * self.dcy * (self.vlnc - self.vbsln)
        regression_a = (-1) * self.dcy * (self.arsl - self.absln)
        self.vlnc = self.vlnc + regression_v
        self.arsl = self.arsl + regression_a
        # Equations of how valence and arousal regress over time using the
        # decay parameter
