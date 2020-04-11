# Agent-Based Modeling of Collective Emotions: Implementing the Cyberemotions Framework

This repository contains an implementation of the _Cyberemotions_ agent-based modeling framework in Python (version 3.7) that abstracts the emergence of collective emotions and the spread of emotional information in online discussions, following the formalization of [Garcia et al. (2016)](http://dx.doi.org/10.1098/rsos.160059).

An extensive technical report and documentation of the model using the _ODD_ (overview, design concepts, details) protocol standard for agent-based modeling can be found in `protocol.pdf`.

The `exploration.ipynb` notebook gives a very short overview into the results of the implemented model, but does not constitute a full analysis of the model data. (We used it primarily to experiment with model parameters to find the setting that produces the most realistic results measured in expressions per agent, specifically adjusting impact factor `s` and satiation factor `c`.)

## How it works

A simulation using the Cyberemotions model can be started by running `model.py` directly or by using the bash `run.sh` script to run the model multiple times at different settings. The `run()` function can also be used to start the model after being imported. This model takes either four arguments that are further passed into this function: 1. the number of model runs, 2. the number of agents, 3. the impact factor, and 4. the satiation factor. 
For example, the model can be started from the Windows command line using:
`python model.py number_of_runs number_of_agents impact_factor satiation_factor`
Likewise, it can be imported and run inside Python:
`import model
run(number_of_runs, number_of_agents, impact_factor, satiation_factor)`
If no arguments are provided, the model is run with the standard settings and the standard parameters listed below.

In addition, the model can be run inside a Jupyter environment using `model.ipynb` that allows for a model overview and experimentation with parameters.

### Dependencies
The model requires the pandas and numpy packages to run, and the pyarrow package to save its data (stored in a dataframe) as a feather file.

### Saving the model data

Running `model.py` directly or using the bash script will store the collected data in the `\data` folder in separate feather files for each model setting containing the following information in their filenames: 1. number of runs, 2. number of agents, impact parameter, satiation factor, UNIX timestamp. (For 100 model runs, one file has the approximate size of 600kb, depending on how long the model is running for.)

Each feather file contains a dataframe summarizing the model data in the following manner, with each row constituting one time step of a model run:

| Run | Agents | s | c | Step | v | a | A | N | h |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model run | Initial agents | Impact parameter | Satiation parameter | Timestep | Agent valence | Agent arousal | Active agents | Expressions | Field charge |

Likewise, the `model.run()` function generates the very same dataframe for all runs at a given setting.

## Model parameters

The standard model parameters are hardcoded, unless otherwise specified above, as follows:

| Parameter | Short | Value | Constant
|---|---|---|---|
| Valence baseline | *b* | 0.056 | BASE_V |
| Arousal baseline | *d* | -0.442 | BASE_A |
| Valence decay | *&gamma;<sub>v</sub>* | 0.367 | DECAY_V |
| Arousal decay | *&gamma;<sub>a</sub>* | 0.414 | DECAY_A |
| Amplitudes | *A<sub>v</sub>* | 0.3 | AMP_V |
|| *A<sub>a</sub>* | 0.3 | AMP_A |
| Arousal threshold | *&tau;* | 0 | THRESH_A |
| Down-regulation factor | *k<sub>v</sub>* | 0.38 | FACTOR_V |
|| *k<sub>a</sub>* | 0.45 | FACTOR_A |
| Satiation factor | *c* | 1.0 | SAT_C |
| Valence coefficients | *b<sub>0</sub>* | 0.14 | COEFF_B0 |
|| *b<sub>1</sub>* | 0 | COEFF_B1 |
|| *b<sub>2</sub>* | 0.057 | COEFF_B2 |
|| *b<sub>3</sub>* | -0.047 | COEFF_B3 |
| Arousal coefficients | d<sub>0</sub> | 0.178 | COEFF_D0 |
|| *d<sub>1</sub>* | 0.14469 | COEFF_D1 |
|| *d<sub>2</sub>* | 0 | COEFF_D2 |
|| *d<sub>3</sub>* | 0 | COEFF_D3 |
| Field charge | *h* | 0 | CHARGE_H |
| Field decay | *&gamma;<sub>h</sub>* | 0.7 | DECAY_H |
| Field impact | *s* | 0.1 | IMPACT_H |

At this stage, this model is primarily used to experiment with model parameters to generate realistic results. The key parameters are satiation factor `c` and impact factor `s` that can accordingly be input using arguments. All other parameters constitute hard-coded constants.
