# Agent-Based Modeling of Collective Emotions: Implementing the Cyberemotions Framework

This repository contains an implementation of the _Cyberemotions_ agent-based modeling framework in Python (version 3.7) that abstracts the emergence of collective emotions and the spread of emotional information in social media.

An extensive report and documentation of the model using the _ODD protocol standard_ (Overview, Design concepts, Details) can be found in `protocol.pdf`.

## How it works

A simulation of the Cyberemotions model can be started by (1.) using `import model` using Python 3 and then calling the `run()` function, or (2.) executing `run.sh`. It runs for a maximum of 150 time steps, or until all agents have dropped out of the simulation.

*Dependencies:* The model requires the pandas and numpy packages to run, and the pyarrow package to save its data (stored in a dataframe) as a feather file.

### 1. Starting the model using run()

The `run()` function of `model.py` takes 2 arguments:

- Number of model runs.
- Number of agents.

Model parameters can be accessed and changed directly after using `import model`.

| Parameter | Short | Value | Constant
|---|---|---|---|
| Valence baseline | b | 0.056 | BASE_V |
| Arousal baseline | d | -0.442 | BASE_A |
| Valence decay | &gamma;<sub>v</sub> | 0.367 | DECAY_V |
| Arousal decay | &gamma;<sub>a</sub> | 0.414 | DECAY_A |
| Amplitudes | A<sub>v</sub> | 0.3 | AMP_V |
|| A<sub>a</sub> | 0.3 | AMP_A |
| Arousal threshold | &tau; | 0 | THRESH_A |
| Down-regulation factor | k<sub>v</sub> | 0.38 | FACTOR_V |
|| k<sub>a</sub> | 0.45 | FACTOR_A |
| Valence coefficients | b<sub>0</sub> | 0.14 | COEFF_B0 |
|| b<sub>1</sub> | 0 | COEFF_B1 |
|| b<sub>2</sub> | 0.057 | COEFF_B2 |
|| b<sub>3</sub> | -0.047 | COEFF_B3 |
| Arousal coefficients | d<sub>0</sub> | 0.178 | COEFF_D0 |
|| d<sub>1</sub> | 0.14469 | COEFF_D1 |
|| d<sub>2</sub> | 0 | COEFF_D2 |
|| d<sub>3</sub> | 0 | COEFF_D3 |
| Field charge | h | 0 | CHARGE_H |
| Field decay | &gamma;<sub>h</sub> | 0.7 | DECAY_H |
| Field impact | s | 0.1 | IMPACT_H |
| Satiation factor | c | 1 | SAT_C

### 2. Starting the model using run.sh

The `run.sh` script for Python 3 takes none, two, three, or four arguments as input, namely (a) number of model runs, (b) number of agents, (c) impact parameter, and (d) satiation factor. If no arguments are provided, the model is run with the standard settings (a = 1, b = 150) and the standard parameters listed above. (Field impact s is calculated using arguments b and d, to scale the impact in regards to the number of agents: s = d / b)

Note: The first argument provided constitutes (a), the second (b), and so on. Therefore it is not possible to change (b) without providing (a), or (d) without (c).

### Saving the model data

Both simulation options will store the collected data in the `\data` folder in seperate feather files with the following filename schema: `cyberemotions-[number of runs]x-agents=[number of agents]-s=[impact parameter]-c=[satiation factor]-[UNIX timestamp].feather`

The feather file contains a dataframe summarizing the model data in the following manner, with each row constituting one time step of a model run:

| Run | Agents | s | c | Step | v | a | A | N | h |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model run | Initial agents | Impact parameter | Satiation parameter | Timestep | Agent valence | Agent arousal | Active agents | Expressions | Field charge |
