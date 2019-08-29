#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
model.py
'''

import pandas as pd
import numpy as np

##############
# PARAMETERS #
##############

VALENCE_B = 0.056 # b
AROUSAL_B = -0.442 # d

VALENCE_START = VALENCE_B
AROUSAL_START = AROUSAL_B

AR_THRESHOLD = 0 # tau

VALENCE_DECAY = 0.367 # gamma_v
AROUSAL_DECAY = 0.414 # gamma_a
VALENCE_AMP = 0.3 # A_v
AROUSAL_AMP = 0.3 # A_a
VALENCE_K = 0.38 # k_v
AROUSAL_K = 0.45 # k_a

COEFF_B0 = 0.14    # b_0
COEFF_B1 = 0    # b_1
COEFF_B2 = 0.057    # b_2
COEFF_B3 = -0.047   # b_3

COEFF_D0 = 0.178 # d_0
COEFF_D1 = 0.14469  # d_1
COEFF_D2 = 0  # d_2
COEFF_D3 = 0  # d_3

FIELD_H = 0   # h
FIELD_DECAY = 0.7  # gamma_h
FIELD_IMPACT = 0.1 # s

############
# ENTITIES #
############

class Agent:
    '''
    Each agent represents one forum user and is defined by its emotional state
    that is stored in the valence and arousal variables. Valence indicates
    whether their emotional state is positive or negative, while arousal
    indicates the strength of that emotion.
    '''
    def __init__(self):
        self.identity = None
        self.valence = VALENCE_START
        self.arousal = AROUSAL_START
        self.threshold = AR_THRESHOLD
        self.valence_history = []
        self.arousal_history = []

    def perception(self, field, stochastic):
        '''
        This method describes how agents perceive their field, how the field
        affects their emotional states, and returns the changed emotion
        variable given the input field variable and a stochastic component
        represented by a random number. The impact of the latter is determined
        by the amplitude parameter of the agent.
        '''
        v_change = field * (COEFF_B0 + COEFF_B1 * self.valence
                            + COEFF_B2 * self.valence ** 2
                            + COEFF_B3 * self.valence ** 3)

        a_change = np.absolute(field) * (COEFF_D0 + COEFF_D1 * self.arousal
                                         + COEFF_D2 * self.arousal ** 2
                                         + COEFF_D3 * self.arousal ** 3)
        if stochastic:
            v_stoch = VALENCE_AMP * np.random.randint(-100, 100) / 100
            a_stoch = AROUSAL_AMP * np.random.randint(-100, 100) / 100
#            v_stoch = VALENCE_AMP * np.random.normal(0,0.3, 1)[0]
#            a_stoch = AROUSAL_AMP * np.random.normal(0,0.3, 1)[0]

            self.valence += v_change + v_stoch
            self.arousal += a_change + a_stoch

        else:
            self.valence += v_change
            self.arousal += a_change

#        print(self.valence)
#        print(self.arousal)

    def expression(self):
        '''
        This method describes the information agents express to the field and
        when. When their arousal reaches their internal threshold value, they
        communicate the sign of their valence, the information whether they
        are in a positive or negative emotional state. After they communicate
        this by storing the information in the expression variable, their
        valence and arousal are both immediately down-regulated.
        '''
        if self.arousal >= self.threshold:
            emotion = np.sign(self.valence)
            self.valence = ((self.valence - VALENCE_B) * VALENCE_K + VALENCE_B)
            self.arousal = ((self.arousal - AROUSAL_B) * AROUSAL_K + AROUSAL_B)
        else:
            emotion = None

        return emotion

    def relaxation(self):
        '''
        This methods describes how the the emotional state of agents relaxes
        towards its baseline over time according to the internal decay
        paramater, independently of whether or not an emotion was expressed.
        '''
        v_relax = (-1) * VALENCE_DECAY * (self.valence - VALENCE_B)
        a_relax = (-1) * AROUSAL_DECAY * (self.arousal - AROUSAL_B)
        self.valence += v_relax
        self.arousal += a_relax

    def data_collection(self):
        self.valence_history.append(round(self.valence, 2))
        self.arousal_history.append(round(self.arousal, 2))

class Field:
    '''
    Each communication field allows the agents of the model to communicate
    with each other by storing their emotional expressions. Fields represent
    discussion threads that forum users can participate in, one at a time, and
    that affect their emotional state. It requires the input of the initial
    emotional charge of the field, its impact on agents, and the decay of this
    impact over time.
    '''
    def __init__(self):
        self.charge = FIELD_H
        self.positive_charge = 0
        self.negative_charge = 0
        self.field_history = [self.charge]

    def communication(self, time, emotions0, emotions1, positive_expressions, negative_expressions):
        '''
        This methods describes how the field variable changes depending on
        user participation and the emotional information they put in. It takes
        two lists of agent expression variables as input, namely a list of all
        positive expressions and a list of all negative expressions.
        '''
        if time == 0 and emotions0:
            pos_e = emotions0[0]
            neg_e = emotions0[1]
        elif time == 15 and emotions1:
            pos_e = emotions1[0]
            neg_e = emotions1[1]
        else:
            pos_e = len(positive_expressions)
            neg_e = len(negative_expressions)
        self.positive_charge += (FIELD_IMPACT * pos_e
                                 - FIELD_DECAY * self.positive_charge)
        self.negative_charge += (FIELD_IMPACT * neg_e
                                 - FIELD_DECAY * self.negative_charge)
        self.charge = self.positive_charge - self.negative_charge
#        print(pos_e)
#        print(neg_e)

    def data_collection(self):
        self.field_history.append(round(self.charge, 2))

############
# SCHEDULE #
############

def start_simulation(time, expressing, stochastic, emotions0, emotions1):
    '''
    This function runs the model using the given settings. At every time step,
    each agent may or may not communicate its emotions by expressing them and
    storing them in the field, and then adjusting its emotional state
    accordingly. Afterwards, the field takes action by calculating its new
    emotional charge given previous agent expressions. The output of the
    function is a list of dataframes containing the individual valence and
    arousal histories of the agents and the field charge history.
    '''
    agent = Agent()
    field = Field()

    for step in range(time):
#        print("Step " + str(step))
        agent.perception(field.charge, stochastic)
        agent.data_collection()
        positive_expressions = []
        negative_expressions = []
        if expressing:
            emotion = agent.expression()
            if emotion == 1:
                positive_expressions.append(emotion)
            elif emotion == -1:
                negative_expressions.append(emotion)
            else:
                pass
        else:
            pass
        agent.relaxation()
        field.communication(step, emotions0, emotions1, positive_expressions, negative_expressions)
        field.data_collection()

    v_list = []
    a_list = []
    f_list = []

    v_list.append(agent.valence_history)
    a_list.append(agent.arousal_history)
    f_list.append(field.field_history)

    v_data = pd.DataFrame(v_list)
    a_data = pd.DataFrame(a_list)
    f_data = pd.DataFrame(f_list)

    data = {"valence": v_data, "arousal": a_data, "field": f_data}

    valence_plot = data["valence"].transpose().plot(color="#1f77b4")
    valence_plot.set(xlabel="Time".capitalize())
    valence_plot.legend(["Agent valence"])

    arousal_plot = data["arousal"].transpose().plot(color="#d62728")
    arousal_plot.set(xlabel="Time".capitalize())
    arousal_plot.legend(["Agent arousal"])

    field_plot = data["field"].transpose().plot(color="#2ca02c")
    field_plot.set(xlabel="Time".capitalize())
    field_plot.legend(["Field charge"])
