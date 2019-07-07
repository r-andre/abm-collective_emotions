# Agent-Based Modeling of Collective Emotions: Implementing the Cyberemotions Framework

This repository contains an implementation of the _Cyberemotions_ agent-based modeling framework (see [1], [2]) in Python (version 3.7) that abstracts the emergence of collective emotions and the spread of emotional information in social media.

### How to use it

Running `run.py` starts the simulation using the preset variables. The standard settings can be adjusted by changing the following variables in the file:
 * `agents = 1` the number of times the model is run before the simulation ends.
 * `time_steps = 10` the number of time steps each model run goes through.
 * `model_runs = 10` the number of agents (representing discussion participants) in the model.
 * `fields = 1` the number of fields (representing discussion threads) that the agents may use to communicate with each other.
 
 The simulation results are stored in `./data/results.csv`.
Once the model was run and the simulation data was successfully collected, launching `analysis.ipynb` using JupyterLab or Jupyter Notebook provides visualizations of the simulation results.

### Dependencies

The model and its analysis depend on the following packages to run:
* `numpy`
* `pandas`
* `matplotlib`
* `plotly`

## Overview, design concepts, details

Using the _Cyberemotions_ framework, this agent-based model abstracts the dynamics of collective emotions and the spread of emotional information online. Collective emotions are understood as emotional states shared and spread by a group of individuals and may be studied as an emergent phenomenon using a complex systems approach. Following the principle of Brownian agents, agents are described by a set of state variables that may change due to deterministic and stochastic influences. In the model, agents (representing human individuals) communicate their emotional states with each other using a communication field (representing aggregates of social media posts, such as threads in discussion forums). This field, in turn, provides feedback that affects the individual emotional states of the agents. On a group level, this leads to the spread of emotions from one agent to another and the emergence of **collective** emotions.

### 1. Purpose

This implementation of the _Cyberemotions_ modeling framework was designed to investigate the dynamics of collective emotions in online discussion forums, where users may directly respond to the posts of others in the same thread. The model and its results are intended to be used as a hypotheses generator and its predictions may be tested against real-world data.

### 2. Entities and state variables

The two types of entities of the model are (1.) the agents representing forum users, and (2.) the communication field that represents one specific thread in a forum. Both are treated as objects and defined as Python classes, with each instance of the respective class containing its own state variables. All state variables are numerical values that can be either positive or negative, with negative numbers indicating a negative emotional charge and positive numbers a positive emotional charge. As the number gets higher, the emotions it represents become more positive, and as it gets smaller, the more negative they become. A charge of `0`, in that sense, is an emotionally neutral baseline.
1. **Agents**: _Valence_ and _arousal_ are the two variables that represent the emotional state of each agent.
   * Valence quantifies the degree of pleasure associated with an emotion.
   * Arousal quantifies the degree of activity associated with an emotion.
2. **Field**: The communication field contains the _field variable_ that represents the emotional charge of the field.

### 3. Process overview and scheduling

Each model runs for a set number of time steps. For each run, the model initializes a set number of agents and the communication field. Once the initialization phase is over, it goes through the same following processes (abstracted as class methods) for every agent in the model and for every step in time.
1. The agent _perceives_ the communication field and its emotional charge.
2. If the arousal of the agent is strong enough (determined by its individual threshold), the agent creates an _expression_ variable.
3. If an expression was generated, the _communication_ field stores its value in its own field variable.
4. The agent _relaxes_ and its valence and arousal regress towards the baseline.

### 4. Design concepts

The design of the model follows the social interactionist paradigm that highlights communicative interactions between individuals. These interactions may lead to unexpected patterns of behavior on the group level, and emergent phenomena. In this case, agents communicate their emotions (internal state variables) with each other by storing emotionally charged information (expression variables) in a field that is perceived by all agents. This expression of emotions, in turn, is triggered by the emotional charge of the field (field variable) itself. While the individual behavior of the agents follows a set of simple rules, new patterns of group behavior may emerge when emotional information spreads and emotional states are shared by multiple individuals. Both, all agents and the field, are treated as individual objects and instances of their respective class.

### 5. Initialization

The model is treated as an object and initialized as an instance of a model class that takes the basic settings (number of agents and time steps) as input. This allows to easily run multiple instances of the model at various settings. At the beginning of each model run, the set number of agents and the field are initialized by creating instances of their respective class. The initial agent state variables valence and arousal, and their fixed arousal thresholds, are set using a standard normal distribution, while the initial field variable is set randomly.

### 6. Input data

While the model itself takes no input data, every model run stores its results as output data that may be used as input for the visualization.

### 7. Submodels

There are four major submodels that are all described as methods of their respective classes. (1) _Perception_, (2) _expression_, and (3) _relaxation_ are methods of the agent class, while (4) _communication_ is a method of the field class. More detailed descriptions of all four submodels are part of the _Cyberemotions_ framework.
1. **Perception**: This submodel describes how the agent internal state variables valence and arousal are affected by the field variable. It is based on an equation that takes relaxation towards an equilibrium (baseline), unexpected events (random numbers) and deterministic influences (in this case the communication field and the emotional feedback of other agents) into account.
2. **Expression**: This submodel describes how the agent expression variable is created when a certain arousal threshold is reached. It is based on an equation that includes the assumption that agents do not communicate all details about their emotions, but only whether it is a positive or negative emotion. Hence, the agent communicates its valence if its arousal exceeds its threshold.
3. **Relaxation**: WIP
4. **Communication**: This submodel describes how the emotional charge of the field changes when agents express their emotions. It is based on a function that calculates an aggregate of all agent expressions.

## References

[1] Garcia, D., Kappas, A., Küster, D. and Schweitzer, F. (2015) “The Dynamics of Emotions in Online Interaction” in: Royal Society Open Science, Vol.3/8, DOI: 10.1098/rsos.160059

[2] Schweitzer, F. and Garcia, D. (2010) “An Agent-Based Model of Collective Emotions in Online Communities” in: The European Physical Journal B, 77 (2010), pp.533-545, DOI: 10.1140/epjb/e2010-00292-1
