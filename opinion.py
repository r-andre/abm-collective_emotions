#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
An agent-based model of opinion polarization driven by emotions
opinion.py
'''

import sys
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


MODEL_RUNS = 1  # Number of times the model is run
AGENTS = 100  # Number of agents at the start of the simulation
TIME = 200  # Maximum number of time steps before the simulation ends

BASE_V = 0.0  # Valence baseline ... b
BASE_A = 0.0  # Arousal baseline ... d

THRESH_MIN = 0.1
THRESH_MAX = 1.1

DECAY_V = 0.5  # Valence decay ... gamma_v
DECAY_A = 0.9  # Arousal decay ... gamma_a

AMP_V = 0.3  # Valence amplitude of stochastic shocks ... A_v
AMP_A = 0.3  # Arousal amplitude of stochastic shocks ... A_a
AMP_THETA = 0.05  # Opinion amplitude of stochastic shocks ... A_theta

FACTOR_V = 1.0  # Valence down-regulation factor ... k_v
FACTOR_A = 1.0  # Arousal down-regulation factor ... k_a

COEFF_A2 = 0.0
COEFF_A3 = -2.0

COEFF_B0 = 0  # Valence coefficient ... b_0
COEFF_B1 = 1  # Valence coefficient ... b_1
COEFF_B2 = 0  # Valence coefficient ... b_2
COEFF_B3 = -1  # Valence coefficient ... b_3

COEFF_C0 = 0.1
COEFF_C1 = 1

COEFF_D0 = 0.05  # Arousal coefficient ... d_0
COEFF_D1 = 0.5  # Arousal coefficient ... d_1
COEFF_D2 = 0.1  # Arousal coefficient ... d_2
COEFF_D3 = 0  # Arousal coefficient ... d_3

BASE_H = 0.1  # Initial charge of the field ... h
DECAY_H = 0.7  # Field decay ... gamma_h

IMPACT_H = 0.6  # Impact of agent expressions on the field ... s
SAT_C = 1.0  # Saturation factor ... c
dt = 0.1


class OpinionAgent(object):
    """
    Class describing one agent instance and its state variables.
    """
    def __init__(self):
        self.bsln_v = np.random.normal(0, 0.1)  # Valence baseline
        self.bsln_a = BASE_A  # Arousal baseline
        self.vlnc = self.bsln_v  # Setting initial valence to baseline value
        self.arsl = self.bsln_a  # Setting initial arousal to baseline value
        self.theta = np.random.normal(0.0, 0.09)
        self.thrshld = np.random.uniform(THRESH_MIN, THRESH_MAX)  # Arousal threshold

        self.hstry_v = []  # History of valence values at each time step
        self.hstry_a = []  # History of arousal values at each time step
        self.opinions = []  # History of opinion values at each time step

    def f_v(self, field):
        return field.sgn * (COEFF_B0 +
                            COEFF_B1 * self.vlnc +
                            round((COEFF_B2 * self.vlnc), 9) ** 2 +
                            round((COEFF_B3 * self.vlnc), 9) ** 3)

    def f_a(self, field):
        return field.abslt * (COEFF_D0 +
                              COEFF_D1 * self.arsl +
                              round((COEFF_D2 * self.arsl), 9) ** 2 +
                              round((COEFF_D3 * self.arsl), 9) ** 3)

    @property
    def xi_v(self):
        return np.random.normal(0, 0.5)

    @property
    def xi_a(self):
        return np.random.normal(0, 6)

    def dv(self, field):
        return (COEFF_B1 * field.sgn - DECAY_V) * self.vlnc + COEFF_B3 * field.sgn * round(self.vlnc, 6) ** 3 + AMP_V * self.xi_v

    def da(self, field):
        return (COEFF_D1 * field.abslt - DECAY_A) * self.arsl + field.abslt * (COEFF_D0 + COEFF_D2 * round(self.arsl,6) ** 2) + AMP_A * self.xi_a

    def perception(self, field):
        """
        Method changing the agent state variables given their perception of
        the field, using its state variable as input and adding stochasticity
        to global change coefficients
        """
        self.vlnc += dt * self.dv(field)
        self.arsl += dt * self.da(field)

        self.hstry_v.append(round(self.vlnc, 2))
        self.hstry_a.append(round(self.arsl, 2))

    def opinate(self, field):
        self.theta += dt * (COEFF_C1 * field.abslt * (self.theta - COEFF_C0 ** 2 / COEFF_C1 * field.sgn))
        self.opinions.append(round(self.theta, 2))

    def expression(self):
        """
        Method checking if an agent expresses its emotions, down-regulating
        them using global factors, and returning information whether it is
        a positive or negative emotion, or none at all.
        """
        if self.arsl >= self.thrshld:
            emotion = np.sign(self.vlnc)
            self.arsl = 0
        else:
            emotion = 0

        return emotion

    def satiation(self, sttn):
        """
        Method checking whether an agent drops out of the simulation given
        the current emotional state and returning a boolean value.
        """
        probability = np.absolute(self.arsl ** 2) * sttn
        chance = np.random.uniform(0, 1)
        return bool(chance <= probability)

    def relaxation(self):
        """
        Method relaxing the emotions of an agent towards their respective
        baselines, using the global decay parameter.
        """
        self.vlnc += dt * (-1 * DECAY_V * (self.vlnc - self.bsln_v))
        self.arsl += dt * (-1 * DECAY_A * (self.arsl - self.bsln_a))


class OpinionField(object):
    """
    Class describing the communication field and its state variables.
    """

    def __init__(self):
        self.abslt = 0.0  # Absolute value of the charge of the field
        self.sgn = 0.0  # Sign of the charge of the field
        self.theta = 0.0
        self.hstry_h = [self.abslt]  # History of the field at each time step
        self.opinions = []

    @property
    def xi_theta(self):
        return np.random.normal(0, 1)

    def communication(self, positive_expressions, negative_expressions, impct):
        """
        Method changing the field state variable using positive and
        negative emotional expressions as input, adding decay over time using
        a global parameter.
        """
        absolute_expressions = positive_expressions + negative_expressions
        sign_expressions = positive_expressions - negative_expressions

        self.abslt += dt * (-1 * DECAY_H * self.abslt +
                       impct * absolute_expressions)
        self.sgn += dt * (-1 * DECAY_H * self.sgn +
                     impct * sign_expressions)

        self.theta += dt * (- COEFF_C0 * self.abslt * COEFF_C0 * self.sgn +
                            COEFF_C1 * (self.abslt - BASE_H) * self.theta +
                            round(COEFF_A2 * self.theta, 9) ** 2 +
                            round(COEFF_A3 * self.theta, 9) ** 3 +
                            AMP_THETA * self.xi_theta)

        self.hstry_h.append(round(self.sgn, 2))
        self.opinions.append(round(self.theta, 2))


class Model(object):
    """
    Class describing the initialization of one instance of a model run and
    its schedule.
    """

    def __init__(self, agents):
        self.actv_agnts = [OpinionAgent() for agent in range(agents)]
        self.inctv_agnts = []
        self.field = OpinionField()
        self.hstry_A = [len(self.actv_agnts)]
        self.hstry_N = [0]
        self.tm_stps = [0]

    def schedule(self, timesteps, sttn, impct):
        """
        Method scheduling the agent and field processes, including their
        data collection and returning a data frame.
        """
        # The simulation ends when all the agents dropped out, or when the
        # maximum number of time steps was reached:
        step = 0
        while step < timesteps and len(self.actv_agnts) > 0:
            step += 1
            # Keeping track of the number of expressions during each time step:
            positive_expressions = 0
            negative_expressions = 0

            for agent in self.actv_agnts:
                agent.perception(self.field)
                agent.opinate(self.field)
                # Note: Agent data is collected once per time step and this
                # seems to be the most useful moment, because it captures the
                # emotional high points of the agents.
                emotion = agent.expression()
                if emotion == 1:
                    positive_expressions += 1
                elif emotion == -1:
                    negative_expressions += 1

                # if agent.satiation(sttn):
                #     self.inctv_agnts.append(agent)
                #     self.actv_agnts.remove(agent)

                # agent.relaxation()

            # After all the agents took their actions, the field is now
            # updated:
            self.field.communication(positive_expressions,
                                     negative_expressions,
                                     impct)

            self.hstry_A.append(len(self.actv_agnts))
            self.hstry_N.append(positive_expressions + negative_expressions)
            self.tm_stps.append(step)

            # Making sure the order the agents act in is not the same at every
            # time step by shuffling the agent list:
            # np.random.shuffle(self.actv_agnts)

        for agent in self.actv_agnts:
            self.inctv_agnts.append(agent)
            self.actv_agnts.remove(agent)


if __name__ == "__main__":
    model = Model(agents=AGENTS)
    model.schedule(TIME, IMPACT_H, SAT_C)

    opinions = []
    valences = []
    arousals = []
    for agent in model.inctv_agnts:
        opinions.append(agent.opinions)
        valences.append(agent.hstry_v)
        arousals.append(agent.hstry_a)

    opinions = pd.DataFrame(data=opinions)
    arousals = pd.DataFrame(data=arousals)
    valences = pd.DataFrame(data=valences)

    fig = plt.figure(figsize=(6, 12))
    ax, ax1, ax2 = fig.add_subplot(311), fig.add_subplot(312), fig.add_subplot(313)

    opinions.T.plot(legend=None, title="Opinions {0}".format(r'$\theta_i$'), ax=ax)
    arousals.T.plot(legend=None, title="Arousals {0}".format(r'$a_i$'), ax=ax1)
    valences.T.plot(legend=None, title="Valences {0}".format(r'$v_i$'), ax=ax2)

    plt.show()
