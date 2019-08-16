#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Agent-Based Modeling of Collective Emotions:
Implementing the Cyberemotions Framework
model.py
'''

import agent as agt
import field as fld

class Model:
    '''
    Each instance of this class describes one model run. It initializes by
    creating a list of agents (and assigning them unique id numbers), and a
    communication field.
    '''
    def __init__(self,
                 Agents,
                 Agent_baseline,
                 Agent_threshold,
                 Field_charge,
                 Field_decay,
                 Field_impact):
        self.agent_list = [agt.Agent(Agent_baseline,
                           Agent_threshold) for agent in range(Agents)]
        self.field = fld.Field(Field_charge, Field_decay, Field_impact)

        agents_all = list(range(0, Agents))
        for agent in self.agent_list:
            agent.id = agents_all.pop(0)
#            print(agent.id)

    def run(self,
            time_steps,
            Valence_coefficient,
            Arousal_coefficient,
            Agent_amplitude,
            Agent_down_regulation,
            Agent_decay):
        '''
        This method runs the model instance using the given settings. At every
        step, each agent may or may not communicate its emotions by expressing
        them and storing them in the field, and then adjusting its emotional
        state accordingly. Afterwards, the field takes action by calculating
        its new emotional charge given previous agent expressions.
        '''

        for step in range(time_steps):
            positive_expressions = []
            negative_expressions = []

            for agent in self.agent_list:
                agent.perception(self.field.charge,
                                 Valence_coefficient,
                                 Arousal_coefficient,
                                 Agent_amplitude)
                agent_emotion = agent.expression(Agent_down_regulation)

                if agent_emotion == 1:
                    positive_expressions.append(agent_emotion)
                elif agent_emotion == -1:
                    negative_expressions.append(agent_emotion)
                else:
                    pass

                agent.relaxation(Agent_decay)

            self.field.communication(positive_expressions, negative_expressions)

            print("Step " + str(step) + " successful!")
        for agent in self.agent_list:
            print("Agent " + str(agent.id) + " history:")
            print(agent.v_history)

