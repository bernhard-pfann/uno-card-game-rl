# Tackling the UNO Card Game with Reinforcement Learning
In this project I tried to analytically derive an optimal strategy, for the classic UNO card game. To do so, I structured my work as follows:
1. Creating a game engine of the UNO card game in Python from scratch
2. Obtaining game statistics from simulating a series of 100,000 games
3. Implementing basic Reinforcement Learning techniques (Q-Learning & Monte Carlo) in order to discover an optimal game strategy

### 1. UNO Card Engine
In order to train a Reinforcement Learning (RL) agent how to play intelligently, a fully-fledged game environment needs to be in place, capturing all the mechanics and rules of the game. In environment.py class objects for <i>card, deck, player, turn</i> and <i>game</i> are defined. In main.ipynb, the classes are imported as module, to run simulations.

### 2. Statistics from Simulations
By running multiple simulations of the game, the following questions are being tackled:
* How many turns do games last?
* How big is the advantage of the player making the first turn?
* What are the most likely situations in the course of a game?

<p align="center"><img src="https://github.com/bernhard-pfann/uno-card-game_rl/blob/main/assets/img/turns.png", width = "600"></p>
<p align="center"><img src="https://github.com/bernhard-pfann/uno-card-game_rl/blob/main/assets/img/starting-advantage.png", width = "600"></p>

### 3. Application of Reinforcement Learning
In agent.py, I defined the algorithm for a Q-Learning and Monte-Carlo agent, both working with a discrete state-action matrix. Via widgets in main.ipynb, the preferred algorithm can be selected together with its main tuning parameters. 
<p align="left"><img src="https://github.com/bernhard-pfann/uno-card-game_rl/blob/main/assets/img/widgets.PNG"></p>

Finally the results after training the RL-model are being analyzed in terms to cumulative win-rate and obtained Q-values.

<p align="center"><img src="https://github.com/bernhard-pfann/uno-card-game_rl/blob/main/assets/img/win-rate.png", width = "600"></p>
<p align="center"><img src="https://github.com/bernhard-pfann/uno-card-game_rl/blob/main/assets/img/q-curve.png", width = "600"></p>

**Python Version:** 3.7  
**Packages:** pandas, numpy, random, itertools, time, tqdm, sys, os, matplotlib, seaborn, ipywidgets



