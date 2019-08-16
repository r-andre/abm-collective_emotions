#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
agent.py
'''

import numpy as np

class Agent:
    '''
    Each agent represents one forum user and is defined by its emotional state
    that is stored in the valence and arousal variables. Valence indicates
    whether their emotional state is positive or negative, while arousal
    indicates the strength of that emotion.
    '''
    def __init__(self, Baselines, Threshold):
        self.id = None # Stores the agent id number assigned by the model
        self.v_baseline = Baselines[0] # Constant valence baseline
        self.a_baseline = Baselines[1] # Constant arousal baseline
        self.valence = self.v_baseline # Sets the initial valence and arousal
        self.arousal = self.a_baseline # to the baseline values
        self.threshold = np.random.uniform(Threshold[0], # Arousal threshold
                                           Threshold[1]) # determined by an
                                                         # uniform distribution
        self.v_history = []
        self.a_history = []

    def perception(self, Field, V_coefficient, A_coefficient, Amplitude):
        '''
        This method describes how agents perceive their field, how the field
        affects their emotional states, and returns the changed emotion
        variable given the input field variable and a stochastic component
        represented by a random number. The impact of the latter is determined
        by the amplitude parameter of the agent.
        '''
        v_change = Field * (V_coefficient[0]
                            + V_coefficient[1] * self.valence
                            + V_coefficient[2] * self.valence ** 2
                            + V_coefficient[3] * self.valence ** 3)
        a_change = Field * (A_coefficient[0]
                            + A_coefficient[1] * self.arousal
                            + A_coefficient[2] * self.arousal ** 2
                            + A_coefficient[3] * self.arousal ** 3)

        v_stochasticity = np.random.randint(-100, 100) / 100 * Amplitude[0]
        a_stochasticity = np.random.randint(-100, 100) / 100 * Amplitude[1]

        self.valence = v_change + self.valence * v_stochasticity
        self.arousal = a_change + self.arousal * a_stochasticity
        # Equations describing how valence and arousal are affected by the
        # field variable and stochastic factors
        
        self.v_history.append(round(self.valence, 2))
        self.a_history.append(round(self.arousal, 2))

    def expression(self, Down_regulation):
        '''
        This method describes the information agents express to the field and
        when. When their arousal reaches their internal threshold value, they
        communicate the sign of their valence, the information whether they
        are in a positive or negative emotional state. After they communicate
        this by storing the information in the expression variable, their
        valence and arousal are both immediately down-regulated.
        '''
        if self.arousal >= self.threshold:
            expression = np.sign(self.valence)
            self.valence = (self.valence - self.v_baseline) \
                           * Down_regulation + self.v_baseline
            self.arousal = (self.arousal - self.a_baseline) \
                           * Down_regulation + self.a_baseline
            # Equations describing an immediate down-regulation of valence and
            # arousal after an emotional expression
        else:
            expression = None
        # The expression variable only returns a value (the sign of valence)
        # if the arousal threshold is reached

        return expression # Returning the expression variable or None when the
                          # arousal did not exceed the threshold

    def relaxation(self, Decay):
        '''
        This methods describes how the the emotional state of agents relaxes
        towards its baseline over time according to the internal decay
        paramater, independently of whether or not an emotion was expressed.
        '''
        v_regression = (-1) * Decay[0] * (self.valence - self.v_baseline)
        a_regression = (-1) * Decay[1] * (self.arousal - self.a_baseline)
        self.valence = self.valence + v_regression
        self.arousal = self.arousal + a_regression
        # Equations of how valence and arousal regress over time using the
        # decay parameter
