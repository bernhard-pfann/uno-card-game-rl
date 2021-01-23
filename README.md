# Tackling the UNO Card Game with Reinforcement Learning
In this project I tried to analytically derive an optimal strategy, for the classic UNO card game. To do so, I split up the workflow into 3 parts:
* Creating a game engine of the UNO card game in Python from scratch
* Obtaining game statistics from simulating a series of 100,000 games
* Implementing basic Reinforcement Learning techniques (Q-Learning & Monte Carlo) in order to discover an optimal game strategy

### UNO Card Engine
In order to train a Reinforcement Learning (RL) agent how to play intelligently, a fully-fledged game environment needs to be in place, capturing all the mechanics and rules of the game. In environment.py class objects for <i>card, deck, player, turn</i> and <i>game</i> are defined.

### Game Statistics from Simulations
Via main.ipynb, simulations can be executed. Thereby the number of simulations and other settings can be selected via dropdown and slider widgets.
<p align="left">
  <img src="https://github.com/bernhard-pfann/uno-card-game_rl/blob/main/assets/img/widgets.PNG">
</p>

The questions that are being answered 


**Python Version:** 3.7  
**Packages:** pandas, numpy, datetime, selenium, webdriver-manager, matplotlib



