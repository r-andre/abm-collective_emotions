#!/bin/bash

# Agent-Based Modeling of Collective Emotions:
# Implementing the Cyberemotions Framework
# run.sh

# This script starts the cyberemotions model in Python 3 with the settings and
# parameters provided. In depends on the pandas and numpy packages in order to
# run, and the pyarrow package to save the output data as a feather file.
# a = Number of model runs
# b = Number agents
# c = Impact parameter (note: can be divided by the number of agents, s = c/a)
# d = Satiation factor

for a in 100 # Model runs
do for b in 100 # Agents
    do for c in 11 12 13 14 15 16 17 18 19 20 # Impact parameter
        do for d in 0.6 0.7 0.8 0.9 1.0 1.1 1.2 1.3 1.4 1.5 # Satiation factor
            do python3 model.py $a $b $c $d done; done; done; done; done
