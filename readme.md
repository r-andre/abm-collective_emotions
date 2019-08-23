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

Using the _Cyberemotions_ framework, this agent-based model abstracts the dynamics of collective emotions and the spread of emotional information online. Collective emotions are understood as emotional states shared and spread by a group of individuals, As such, they may be studied as an emergent phenomenon using a complex systems approach. Following the principle of Brownian agents, the agents of the Cyberemotions framework are described by a set of state variables that may change due to deterministic and stochastic influences. In the model, agents (representing human individuals) communicate their emotional states with each other using a communication field (representing aggregates of social media posts, such as threads in discussion forums). This field, in turn, provides feedback that affects the individual emotional states of the agents. On a group level, this leads to the spread of emotions from one agent to another and the emergence of **collective** emotions.

### 1. Purpose

This implementation of the _Cyberemotions_ modeling framework was designed to investigate the dynamics of collective emotions in online discussion forums, where users may directly respond to the posts of others in the same thread. The model and its results are intended to be used as a hypotheses generator and its predictions may be tested against real-world data.

### 2. Entities and state variables

The two types of entities of the model are (1.) the agents representing forum users, and (2.) the communication field that represents one specific thread in a forum. Both are treated as objects and defined as Python classes, with each instance of the respective class containing its own state variables. All state variables are numerical values that can be either positive or negative, with negative numbers indicating a negative emotional charge and positive numbers a positive emotional charge. As the number gets higher, the emotions it represents become more positive, and as it gets smaller, the more negative they become. A charge of `0`, in that sense, is emotionally neutral and considered an equilibrium state.
1. **Agents**: _Valence_ and _arousal_ are the two variables that represent the emotional state of each agent.
   * Valence quantifies the degree of pleasure associated with an emotion.
   * Arousal quantifies the degree of activity associated with an emotion.
2. **Field**: The communication field is represented by the _field variable_ that contains the emotional charge of the field.

### 3. Process overview and scheduling

Each model runs for a set number of time steps. For each run, the model initializes a set number of agents and the communication field. Once the initialization phase is over, it goes through the same following processes (abstracted as class methods) for every agent in the model and for every step in time.
1. The agent _perceives_ the communication field and its emotional charge.
2. If the arousal of the agent is strong enough (determined by its individual threshold), the agent creates an _expression_ variable.
3. If an expression was generated, the _communication_ field stores its value in its own field variable.
4. The agent _relaxes_ and its valence and arousal regress towards an individual baseline.

### 4. Design concepts

The design of the model follows the social interactionist paradigm that highlights communicative interactions between individuals. These interactions may lead to unexpected patterns of behavior on the group level, and emergent phenomena. In this case, agents communicate their emotions (internal state variables) with each other by storing emotionally charged information (expression variables) in a field that is perceived by all agents. This expression of emotions, in turn, is triggered by the emotional charge of the field (field variable) itself.

In principle, every agents has individual factors that determine what effect the emotional charge of the field has on its own emotional state (representing personal traits such as empathy or responsiveness), based on the general idea that agents already in a specific state may be more affected by particular emotions of others. For the purpose of this model, it is assumed that the impact of the emotional information that agents perceive  depends on their emotional state in a non-linear manner. For example, the positive emotional state of an agent may become more positive when perceiving positive emotional information from other agents.

While the individual behavior of the agents follows a set of simple rules, new patterns of group behavior may emerge when emotional information spreads and emotional states are shared by multiple individuals. Both, all agents and the field, are treated as individual objects and instances of their respective class.

### 5. Initialization

The model is treated as an object and initialized as an instance of a model class that takes the basic settings (number of agents and time steps) as input. This allows to easily run multiple instances of the model at various settings. At the beginning of each model run, the set number of agents and the field are initialized by creating instances of their respective class. The initial agent state variable baselines of valence and arousal, and their fixed arousal thresholds, are set using a standard normal distribution, while the initial field variable is set randomly.

### 6. Input data

While the model itself takes no input data, every model run stores its results as output data that may be used as input for the visualization.

### 7. Submodels

There are four major submodels that are all described as methods of their respective classes. (I.) _Perception_, (II.) _expression_, and (III.) _relaxation_ are methods of the agent class, while (IV.) _communication_ is a method of the field class. More detailed descriptions of all four submodels and an explanation of the equations they are based on are part of the _Cyberemotions_ framework.

#### I. Perception

This submodel describes the rate of change of the agent internal state variables _valence_ and _arousal_ through the effects of the _field variable_. It is based on an equation that takes deterministic influences (the communication field and emotional feedback of other agents) and stochastic factors (unexpected events represented by a random numbers taken at a given point in time from a distribution of stochastic shocks with a mean of `0`) into account.

The field variable _F_ represents a function that describes how perceiving the emotional charge _h_ of the field changes the state variables valence _v_ and arousal _a_ of an agent _i_ at time point _t_. The random number _&xi;_ represent stochastic components affecting _v_ and _a_ and the strength of its influence on an individual is determined by amplitude _A_.

The equation

_v&#775;<sub>i</sub> = r<sub>v<sub>i</sub></sub> + F<sub>v</sub>(h, v<sub>i</sub>(t)) + A<sub>v<sub>i</sub></sub>&xi;<sub>v</sub>(t)_

describes the change of valence _v&#775;<sub>i</sub>_ of an agent _i_ given the emotional charge of the communication field _h_, while

_a&#775;<sub>i</sub> = r<sub>a<sub>i</sub></sub> + F<sub>a</sub>(h, a<sub>i</sub>(t)) + A<sub>a<sub>i</sub></sub>&xi;<sub>v</sub>(t)_

describes the change in arousal _a&#775;<sub>i</sub>_ of the same agent. The perception functions _F<sub>v</sub>_ and _F<sub>a</sub>_ define the changes in _v<sub>i</sub>_ and _a<sub>i</sub>_ that are caused by different values of _h_. Furthermore, the unique stochastic components _A_ and _&xi;_ are added that account for unpredictable factors in emotional changes of individuals (e.g. multiplicative noise).

The functions

_F<sub>v</sub>(h, v<sub>i</sub>(t)) = h &lowast; (b<sub>0</sub> + b<sub>1</sub>v<sub>i</sub>(t) + b<sub>2</sub>v<sub>i</sub>(t)<sup>2</sup> + . . . +  b<sub>n</sub>v<sub>i</sub>(t)<sup>n</sup>)_

and

_F<sub>a</sub>(h, a<sub>i</sub>(t)) = |h| &lowast; (b<sub>0</sub> + b<sub>1</sub>a<sub>i</sub>(t) + b<sub>2</sub>a<sub>i</sub>(t)<sup>2</sup> + . . . + b<sub>n</sub>a<sub>i</sub>(t)<sup>n</sup>)_

define how the state variable _v<sub>i</sub>_ is affected by the the field variable _h_, while _a<sub>i</sub>_ is affected by the sign of the field variable _|h|_.

_v_ ... valence
_a_ ... arousal
_i_ ... agent instance
_r<sub>_ ... relaxation
_F_ ... perception function
_h_ ... field variable
_t_ ... point in time
_A_ ... amplitude
_&xi;_ ... random number

#### II. Expression

Submodel expression describes how agents express the valence of their emotions by creating an _expression variable_ that is a function of the sign of its valence and activated when their arousal surpasses an individual _arousal threshold_. It is based on an equation that includes the assumption that agents do not communicate all details about their emotions, but only whether it is a positive or negative emotion.

Expression variable _s_ of agent _i_ is a function of the sign of its valence _v_, but only stores a positive or negative value (`1` or `-1`) if its arousal _a_ is larger than the arousal threshold _&tau;_.

The equation

_s<sub>i</sub>(t) = |v<sub>i</sub>(t)| &Theta; [a<sub>i</sub>(t) &minus; &tau;<sub>i</sub>]_

describes the relationship between _s<sub>i</sub>_ and the sign of _v<sub>i</sub>_ as a Heaviside step function _&Theta;_. If _a<sub>i</sub>_ is larger that _&tau;<sub>i</sub>_, then _s<sub>i</sub>_ stores a positive value when _v<sub>i</sub>_ is likewise positive, or a negative value when _v<sub>i</sub>_ is negative. Else, no expression is triggered when _a<sub>i</sub>_ does not pass threshold _&tau;<sub>i</sub>_.

_s<sub>i</sub>_ ... expression variable
_&Theta;_ ... Heaviside step function
_&tau;_ ... arousal threshold

#### III. Relaxation

The relaxation submodel describes the individual relaxation of the valence and arousal of agents towards their _baseline_ values using specific _decay parameters_ that are unique to every agent and to its respective state. It is based on an equation that assumes an exponential decay of valence and arousal in agents over time.

The state variables valence _v_ and arousal _a_ of agent _i_ at time _t_ are reduced by a combination of their initial values minus their baseline times the decay parameters _&gamma;_ (which vary for each agent and are different for valence and arousal) that define the time-scale of this decay. This decay represents the relaxation of emotional states to a baseline and an emotional equilibrium.



The equations

_r<sub>v<sub>i</sub></sub> = &minus; &gamma;<sub>v<sub>i</sub></sub>(v<sub>i</sub>(t) &minus; b)_

and

_r<sub>a<sub>i</sub></sub> =  &minus; &gamma;<sub>a<sub>i</sub></sub>(a<sub>i</sub>(t) &minus; d)_

specify the relaxation of valence _v<sub>i</sub>_ and arousal _a<sub>i</sub>_ towards their respective values _b_ and _d_ given the decay parameters _&gamma;_.

_&gamma;_ ... decay parameter

#### IV. Communication

This submodel describes how the emotional charge of the field changes when agents express their emotions. It is based on a function that calculates aggregates of all positive and negative agent expressions.

While _N_ is the total number of agents with an either positive or negative expression variable, _s_ is a fixed amount by which the field variable increases or decreases for every agents that expresses its emotions. In addition to agent expressions, the decay parameter _&gamma;_ represents a decrease in impact of emotional information on agents over time.

Equations

_h&#775;<sub>+</sub> = sN<sub>+</sub>(t) &minus; &gamma;<sub>+</sub>h<sub>+</sub>(t)_

and

_h&#775;<sub>&minus;</sub> = sN<sub>&minus;</sub>(t) &minus; &gamma;<sub>&minus;</sub>h<sub>&minus;</sub>(t)_

calculate the emotional charge of the respective positive or negative field variables _h<sub>+</sub>_ or _h<sub>&minus;</sub>_ using the total number of agents that contribute to the field _N_ in combination with a fixed impact variable _s_. Additionally, the decay parameter _&gamma;<sub>+</sub>_ and _&gamma;<sub>&minus;</sub>_ account for a loss of emotional impact over time. While

_h = h<sub>+</sub>(t) + h<sub>&minus;</sub>(t)_

creates a total of the emotional charge of the field that is either positive or negative, using the field variables _h<sub>+</sub>_ and _h<sub>&minus;</sub>_.

_h<sub>+</sub>_ ... (positive) field variable
_h<sub>&minus;</sub>_ ... (negative) field variable
_s_ ... impact variable

## References

[1] Garcia, D., Kappas, A., Küster, D. and Schweitzer, F. (2015) “The Dynamics of Emotions in Online Interaction” in: Royal Society Open Science, Vol.3/8, DOI: 10.1098/rsos.160059

[2] Schweitzer, F. and Garcia, D. (2010) “An Agent-Based Model of Collective Emotions in Online Communities” in: The European Physical Journal B, 77 (2010), pp.533-545, DOI: 10.1140/epjb/e2010-00292-1
