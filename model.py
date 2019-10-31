#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
model.py
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

############
# SETTINGS #
############

TIME = 100 # Maximum number of time steps before the simulation ends
AGENTS = 150 # Number of agents at the start of the simulation

##############
# PARAMETERS #
##############

BASE_V = 0.056 # Valence baseline ... b
BASE_A = -0.442 # Arousal baseline ... d

THRESH_A = 0 # Arousal threshold ... tau

DECAY_V = 0.367 # Valence decay ... gamma_v
DECAY_A = 0.414 # Arousal decay ... gamma_a
AMP_V = 0.3 # Valence amplitude of stochastic shocks ... A_v
AMP_A = 0.3 # Arousal amplitude of stochastic shocks ... A_a
FACTOR_V = 0.38 # Valence down-regulation factor ... k_v
FACTOR_A = 0.45 # Arousal down-regulation factor ... k_a

COEFF_B0 = 0.14 # Valence coefficient ... b_0
COEFF_B1 = 0 # Valence coefficient ... b_1
COEFF_B2 = 0.057 # Valence coefficient ... b_2
COEFF_B3 = -0.047 # Valence coefficient ... b_3

COEFF_D0 = 0.178 # Arousal coefficient ... d_0
COEFF_D1 = 0.14469  # Arousal coefficient ... d_1
COEFF_D2 = 0  # Arousal coefficient ... d_2
COEFF_D3 = 0  # Arousal coefficient ... d_3

CHARGE_H = 0 # Initial charge of the field ... h
DECAY_H = 0.7 # Field decay ... gamma_h
IMPACT_H = 0.1 # Impact of agent expressions on the field ... s
# Note: This standard setting is later overruled by setting the constant to a
# value that scales to the total number of agents in the simulations. Test runs
# showed with s = 0.1 the model only behaves as expected with 150 agents.

############
# ENTITIES #
############

class Agent:
    '''Class describing one agent instance and its state variables.'''
    def __init__(self):
        self.baseline_v = np.random.normal(BASE_V, 0.1)
        self.baseline_a = np.random.normal(BASE_A, 0.1)
        # Note: Spread of the normal distrution should not cause valence or
        # arousal baselines to lie above 1 or below -1
        self.valence = self.baseline_v
        self.arousal = self.baseline_a
        self.threshold = THRESH_A
        self.history_v = []
        self.history_a = []

    def perception(self, field):
        '''Method changing the agent state variables given their perception of
        the field, using its state variable as input and adding stochasticity
        to global change coefficients'''
        self.valence += field.sign_h * (COEFF_B0 +
                                        COEFF_B1 * self.valence +
                                        COEFF_B2 * self.valence ** 2 +
                                        COEFF_B3 * self.valence ** 3)
        self.arousal += field.absolute_h * (COEFF_D0 +
                                            COEFF_D1 * self.arousal +
                                            COEFF_D2 * self.arousal ** 2 +
                                            COEFF_D3 * self.arousal ** 3)
        # Note: Coefficients B3 and D3 sometimes caused the program not to
        # execute during first test runs due to an "result too large" error.

        # Stochastic shocks triggering agent interaction:
        stoch_v = np.random.randint(-100, 100) / 100
        stoch_a = np.random.randint(-100, 100) / 100
        self.valence += AMP_V * stoch_v
        self.arousal += AMP_A * stoch_a

    def expression(self):
        '''Method checking if an agent expresses its emotions, down-regulating
        them using global factors, and returning information whether it is
        a positive or negative emotion, or none at all.'''
        if self.arousal >= self.threshold:
            emotion = np.sign(self.valence) # Variable needed for scheduling!
            self.valence = ((self.valence - self.baseline_v) * FACTOR_V
                            + self.baseline_v)
            self.arousal = ((self.arousal - self.baseline_a) * FACTOR_A
                            + self.baseline_a)
        else:
            emotion = None

        return emotion

    def relaxation(self):
        '''Method relaxing the emotions of an agent towards their respective
        baselines, using the global decay parameter.'''
        self.valence += (-1) * DECAY_V * (self.valence - self.baseline_v)
        self.arousal += (-1) * DECAY_A * (self.arousal - self.baseline_a)

    def satiation(self):
        '''Method checking whether an agent drops out of the simulation given
        the current emotional state and returning a boolean value.'''
        probability = np.absolute(self.arousal ** 2 * 100)
        chance = np.random.randint(0, 100)
        return bool(chance <= probability)

        # Old version of the return statement:
#        if chance <= probability:
#            return True
#        else:
#            return False

    def collect_data(self):
        '''Method collecting the agent state variables in a list.'''
        self.history_v.append(round(self.valence, 2))
        self.history_a.append(round(self.arousal, 2))
        # Missing: What other data could be useful?

class Field:
    '''Class describing the communication field and its state variables'''
    def __init__(self):
        self.absolute_h = CHARGE_H
        self.sign_h = CHARGE_H
        self.history = []
        self.expressions = []

    def communication(self, positive_expressions, negative_expressions):
        '''Method changing the field state variable using positive and
        negative emotional expressions as input, adding decay over time using
        a global parameter.'''
        absolute_expressions = positive_expressions + negative_expressions
        sign_expressions = positive_expressions - negative_expressions

        self.absolute_h += (-1 * DECAY_H * self.absolute_h +
                            IMPACT_H * absolute_expressions)
        self.sign_h += (-1 * DECAY_H * self.sign_h +
                        IMPACT_H * sign_expressions)

    def collect_data(self):
        '''Method collecting the field state variable in a list.'''
        self.history.append(round(self.sign_h, 2))

############
# SCHEDULE #
############

def start_simulation(time, agents):
    '''Function starting the simulation and running the model using the number
    of agents and the maximum number of time steps as arguments. Its output is
    a dictionary using "valence", "arousal", and "field" as key to access
    respective dataframes of the history of agent and field state variables.'''
    global IMPACT_H
    IMPACT_H = 15 / agents
    # Note: Standard impact variable s = 0.1, but this way it scales to the
    # number of agents in the simulation, allowing for collective emotions to
    # emerge at any number of agents.
    agent_list = [Agent() for agent in range(agents)]
    field = Field()
    histories_v = []
    histories_a = []
    history_f = []
    history_n = []
    history_pn = []
    history_nn = []
    history_agents = []

    # The simulation ends when all the agents dropped out, or when the maximum
    # number of time steps was reached:
    step = 0
    while step < time and len(agent_list) >= 1:
        step += 1
        positive_expressions = 0
        negative_expressions = 0

        for agent in agent_list:
#            agent.collect_data() # For exploration purposes, changes data
            agent.perception(field)
            # These if-elif statements force agent state variables to remain
            # below 1 and above -1.
#            if agent.valence > 1: agent.valence = 1
#            elif agent.valence < -1: agent.valence = -1
#            if agent.arousal > 1: agent.arousal = 1
#            elif agent.arousal < -1: agent.arousal = -1
            agent.collect_data()
            # Note: Agent data is collected once per time step and this seems
            # to be the most useful moment, because it captures the emotional
            # high points of the agents.
            emotion = agent.expression()
            if emotion == 1:
                positive_expressions += 1
            elif emotion == -1:
                negative_expressions += 1
#            else:
#                pass
#            agent.collect_data() # For exploration purposes, changes data
            if agent.satiation(): # Need to collect data before dropout
                histories_v.append(agent.history_v)
                histories_a.append(agent.history_a)
                agent_list.remove(agent)
#            else:
#                pass
            agent.relaxation()
            # Making sure the order the agents act in is not the same at every
            # time step by shuffling the agent list:
            np.random.shuffle(agent_list)

        # After all the agents took their actions, the field is now updated:
        field.communication(positive_expressions, negative_expressions)
        field.collect_data()
        history_pn.append(positive_expressions)
        history_nn.append(negative_expressions)
        history_agents.append(len(agent_list))

    # All the individual agent histories are now stored in one large list:
    for agent in agent_list:
        histories_v.append(agent.history_v)
        histories_a.append(agent.history_a)

    history_f.append(field.history)
    history_n.append(history_pn)
    history_n.append(history_nn)

    # Creating a dictionary of agent and field data and respective dataframes:
    data = {"valence": pd.DataFrame(histories_v),
            "arousal": pd.DataFrame(histories_a),
            "field": pd.DataFrame(history_f),
            "expressions": pd.DataFrame(history_n),
            "agents": pd.DataFrame(history_agents)}
    return data

def analyze_data(data):
    '''Function analyzing the input simulation results and producing plots of
    the mean values of the agent state variables and the field state variable
    over time.'''
    valence_plot = data["valence"].mean().transpose().plot(color="#1f77b4")
    valence_plot.set(xlabel="Time".capitalize())
#    valence_plot.legend(["Agent valence"])

    arousal_plot = data["arousal"].mean().transpose().plot(color="#d62728")
#    arousal_plot.set(xlabel="Time".capitalize())
    arousal_plot.legend(["Agent valence", "Agent arousal"])
    # Note: Cannot figure out why in this case both valence and arousal are
    # only part of the same plot when using mean() before transpose().
    plt.figure()

    field_plot = data["field"].transpose().plot(color="#2ca02c")
#    field_plot.set(xlabel="Time".capitalize())
    field_plot.legend(["Field charge"])
    plt.figure()

    n_positive_plot = data["expressions"].loc[0].transpose().plot(color="#1f77b4")
    n_positive_plot.set(xlabel="Time".capitalize())
    n_negative_plot = data["expressions"].loc[1].transpose().plot(color="#d62728")
#    n_negative_plot.set(xlabel="Time".capitalize())
    n_negative_plot.legend(["Positive expressions", "Negative expressions"])
    plt.figure()

    agents_plot = data["agents"].plot(color="#2ca02c")
    agents_plot.legend(["Number of agents"])
    plt.figure()


# Running the model and illustrating its results:
if __name__ == "__main__":
	analyze_data(start_simulation(TIME, AGENTS))
