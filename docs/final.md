---
layout: default
title: Final Report
---

# Final Report

## Video


## Project Summary
The goal of this project is to have an agent survive for as long as possible in a 10x10 block environment with a maze and three zombies placed somewhere in the maze. 
The agent starts off in the middle of this environment. 
The zombies are placed at three spots on the perimeter of the environment. 
The agent must survive for as long as possible. 
See figure below for visualization:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/maze.png" width="500"></div>
Figure 1: Picture of 10x10 maze environment for Malmo-Minecraft agent. 
Black spots indicate walls. White spots indicate free path. 
Green spot indicates starting position of agent. 
Red spot indicates starting position of zombies.

.

The challenges of this problem are using the maze to the agents advantage in surviving and accomodating a large state space. 
Without a maze, the agent really only has one general optimal path, that is, to go the corner where there are no zombies, until it gets killed.
The agent is not fast enough to outrun the zombies, so it always gets killed quickly unless it starts immediately running to the safest spot - the corner.
With the maze, the agent has an opportunity to survive for a long time by hiding from the zombies in the maze. 
Zombies only attack when they see the agent, so the agent can use his/her "smarts" to survive longer - this is where we use an AI/ML algorithm.
We use reinforcement learning for this problem, specifically Q-learning. 

.

We consider this task non-trivial because of its large state space. 
Using a table to keep track of the state-action pairs, we would have to keep track of approximately $$100^4$$ or $$10^8$$ values ($$100 \cdot 100 \cdot 100 \cdot 100$$ for each possible permutation of positions for each entity).
This is too large a number for traditional Q-tabular learning.
Therefore, we approximate the Q-table with a parameterized function. 
We believe this can be considered non-trivial because of the numerous ways we can represent the state via basis functions (BFs).
Some set of basis functions may be better than others.
Creativity and experimenting with different combinations of BFs was required.

.

Another reason this may not be considered trivial is because it was not one of the examples that Malmo provided nor did we use an off the shelf program. 
We did take away a lot from the examples from Malmo, especially things concerning the environment XML.
But for the most part we coded our own parameters, our own updates, and our own basis functions using only books as references.


## Approaches
Use another level-two header called Approaches, In this section, describe both the baselines
and your proposed approach(es). Describe precisely what the advantages and disadvantages of each are,
for example, why one might be more accurate, need less data, take more time, overfit, and so on. Include
enough technical information to be able to (mostly) reproduce your project, in particular, use pseudocode
and equations as much as possible.

### Algorithm
We now show the algorithm we use to learn the parameters for the above function approximation. A full description of the algorithm can be found in Sutton and Barto's _Reinforcement Learning: An Introduction_: Chapter 8. One key thing to note is that $$\epsilon$$ and $$\alpha$$ are monotonically decreasing functions of $$k$$.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/alg4.png" width="500"></div>
Figure 6: An online linear, gradient descent Q-learning algorithm for approximating Q(s,a) with eligibility tracing and an $$\epsilon -$$greedy exploration.

## Evaluation

## References
