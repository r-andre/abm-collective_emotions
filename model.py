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
    creating a list of agents and a communication field.
    '''
    def __init__(self, agents): # The Model instance initializes the set
                                # number of agents and one instance of the
                                # communication field
        self.agent_list = [agt.Agent() for agent in range(agents)]
        self.field = fld.Field()

    def run(self, time_steps):
        '''
        This method runs the model instance using the given settings. At every
        step, each agent may or may not communicate its emotions by storing
        them in its field, adjusting its emotional state accordingly.
        '''
        for step in range(time_steps): # For each step in time...
            for agent in self.agent_list: # ...each agent perceives the
                                          # communication field and may
                                          # express its emotions
                agent.perception(self.field.variable)
                exprn = agent.expression()
                if exprn: # If an agent expresses its emotions, it stores
                          # them in the communication field
                    self.field.communication(exprn)
                else:
                    pass
                agent.relaxation() # At the end of each time step the emotions
                                   # of each agent regress towards a baseline
            print(step)
