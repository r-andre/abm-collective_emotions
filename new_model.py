#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
new_model.py
'''

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

############
# SETTINGS #
############

TIME = 20

VALENCE_BASE = 0.2
AROUSAL_BASE = 0.2
AR_THRESHOLD = 0.3

EXPRESSIONS_POSITIVE = 15
EXPRESSIONS_NEGATIVE = 4

##############
# PARAMETERS #
##############

AGENT_DECAY = [0.3, 0.9]
AGENT_AMP = [0.3, 0.3]
DOWN_REG = 0.4
VALENCE_COEFF = [0, 1, 0, -1]
AROUSAL_COEFF = [0.05, 0.5, 0.5, 0.5]

FIELD_CHARGE = 0
FIELD_DECAY = 0.7
FIELD_IMPACT = 0.1

############
# ENTITIES #
############

class Agent:
    def __init__(self):
        self.identity = None
        self.valence = VALENCE_BASE
        self.arousal = AROUSAL_BASE
        self.threshold = AR_THRESHOLD
        self.valence_history = [self.valence]
        self.arousal_history = [self.arousal]

    def perception(self, field):
        v_change = field * (VALENCE_COEFF[0]
                            + VALENCE_COEFF[1] * self.valence
                            + VALENCE_COEFF[2] * self.valence ** 2
                            + VALENCE_COEFF[3] * self.valence ** 3)
        a_change = np.sign(field) * (AROUSAL_COEFF[0]
                                     + AROUSAL_COEFF[1] * self.arousal
                                     + AROUSAL_COEFF[2] * self.arousal ** 2
                                     + AROUSAL_COEFF[3] * self.arousal ** 3)

#        v_stoch = AGENT_AMP[0] * np.random.randint(-100, 100) / 100
#        a_stoch = AGENT_AMP[1] * np.random.randint(-100, 100) / 100

        self.valence = v_change + self.valence# + v_stoch
        self.arousal = a_change + self.arousal# + a_stoch
        # CLARIFY: Possibly remove self.valence/arousal?

    def expression(self):
        if self.arousal >= self.threshold:
            emotion = np.sign(self.valence)
            self.valence = (self.valence - VALENCE_BASE) \
                           * DOWN_REG + VALENCE_BASE
            self.arousal = (self.arousal - AROUSAL_BASE) \
                           * DOWN_REG + AROUSAL_BASE
        else:
            emotion = None

        return emotion

    def relaxation(self):
        v_relax = (-1) * AGENT_DECAY[0] * (self.valence - VALENCE_BASE)
        a_relax = (-1) * AGENT_DECAY[1] * (self.arousal - AROUSAL_BASE)
        self.valence += v_relax
        self.arousal += a_relax

    def data_collection(self):
        self.valence_history.append(round(self.valence, 2))
        self.arousal_history.append(round(self.arousal, 2))

class Field:
    def __init__(self):
        self.charge = FIELD_CHARGE
        self.positive_charge = 0
        self.negative_charge = 0
        self.field_history = [self.charge]

    def communication(self, time):
        if time < 1:
            positive_number = EXPRESSIONS_POSITIVE
            negative_number = EXPRESSIONS_NEGATIVE
        else:
            positive_number = 0
            negative_number = 0

        self.positive_charge = (FIELD_IMPACT * positive_number
                                - FIELD_DECAY * self.positive_charge)
        self.negative_charge = (FIELD_IMPACT * negative_number
                                - FIELD_DECAY * self.negative_charge)
        print(self.positive_charge)
        print(self.negative_charge)
        self.charge = self.positive_charge + self.negative_charge

    def data_collection(self):
        self.field_history.append(round(self.charge, 2))

############
# SCHEDULE #
############

def start_simulation(time):
    agent = Agent()
    field = Field()

    for step in range(time):
        agent.perception(field.charge)
        agent.data_collection()
        agent.relaxation()
        field.communication(step)
        field.data_collection()

    v_list = []
    a_list = []
    f_list = []

    v_list.append(agent.valence_history)
    a_list.append(agent.arousal_history)
    f_list.append(field.field_history)

    valence_data = pd.DataFrame(v_list)
    arousal_data = pd.DataFrame(a_list)
    field_data = pd.DataFrame(f_list)

#    plt.figure()
    valence_plot = valence_data.transpose().plot(color="purple")
    valence_plot.set(xlabel="Time".capitalize())
    valence_plot.legend(["Agent valence"])

    arousal_plot = arousal_data.transpose().plot(color="orange")
    arousal_plot.set(xlabel="Time".capitalize())
    arousal_plot.legend(["Agent arousal"])

    field_plot = field_data.transpose().plot(color="green")
    field_plot.set(xlabel="Time".capitalize())
    field_plot.legend(["Field charge"])
#    valence_data.transpose().plot(color="purple").legend(["Agent valence"])
#    arousal_data.transpose().plot(color="orange").legend(["Agent arousal"])
#    field_data.transpose().plot(color="green").legend(["Field charge"])

start_simulation(TIME)
