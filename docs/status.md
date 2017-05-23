---
layout: default
title: Status
---

# (GROUP NAME?) PROJECT STATUS - 5/26/2016

## PROJECT SUMMARY
The goal of this project is to survive for as long as possible in a 10x10 block environment with a maze and three zombies placed somewhere in the maze. The agent starts off in the middle of this environment. The zombies are placed at three pre-chosen spots. The agent must survive for as long as possible. See figure below for visualization:
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/maze.png" width="500"></div>
Figure 1: Picture of 10x10 maze environment for Malmo-Minecraft agent. Black spots indicate walls. White spots indicate free path. Green spot indicates starting position of agent. Red spot indicates starting position of zombies.

## APPROACH
We are using reinforcement learning to learn how to survive in the maze, specifically, we attempt to learn a Q-function to approximate a Q-table. 

### Markov Decison Process (MDP)
We first describe our Markov Decision Process.

Our reward function is -1000 for death. 

For our states and actions, we start off with 10x10 = 100 grid positions, 4 possible discrete actions (movenorth 1, movesouth 1, movewest 1, moveeast 1), and 4 total entities. 
Using a Q-table, we would have to keep track of possibly 4 x 100<sup>4</sup> possible state-action pairs (4 for each action and 100x100x100x100 for each possible position of each entity). 
This is too large a number for us to expect to keep track of, so we approximate our state-action pairs with a list of 72 parameters 
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/theta_list.png" width="250"></div>

To represent the state in our approximation, we use 72 basis functions as features:
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/basis_functions.png" width="600"></div>

More precisely, we represent our state by breaking it down into 18 partitions: 9 dynamic partitions that move with the agent so that the agent is always at the center of this sub-space, and 9 stationary partitions that allow the agent to know which region of the environment the agent is in.
We are currently experimenting with a couple different stationary sets of partitions.
This is all visualized as followed in the figures below, along with descriptions for them:
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/basis_dynamic.png" width="350"></div>
Figure 2: Picture of 9 dynamic partitions as basis functions. Green spot indicates position of agent. Red spots indicate position of zombies.
The basis function for each partiton returns an integer indicating how many zombies are in that particular partition. 
Possible integers include: 0,1,2,3.

.

.

<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/basis_dynamic2.png" width="350"></div>
Figure 3: Picture of 9 dynamic partitions as basis functions. Green spot indicates position of agent. 
The partitions move with the agent so that the agent is always at its center.  
This allows us to keep track of the proximity of zombies to the agent.

.

.

<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/basis_stationary1.png" width="350"></div>
Figure 4: Picture of 9 stationary partitions as basis functions. 
These partitions never move.  
Based off the "tile" basis functions from Sutton and Barto's _Reinforcement Learning: An Introduction_.
The basis function for each partiton returns an 1 if the agent is in it, 0 otherwise.
They do not keep track of zombie positions.

.

.

<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/basis_stationary2.png" width="350"></div>
Figure 5: Picture of 9 stationary partitions as basis functions. 
These partitions never move.
These circular partitions have radius 2.50 unit blocks.  
Based off the "coarse" basis function from Sutton and Barto's _Reinforcement Learning: An Introduction_.
The basis function for each partiton returns an 1 if the agent is in it, 0 otherwise.
They do not keep track of zombie positions.

---------------------------------------------------------------------------------------------------------------------------------------

For each of our 4 actions we allow a set of 18 basis functions, thus giving us 72 total basis functions and 72 total parameters.

So our MDP consists of reward function of -1000 for death and these 72 basis functions and parameters.

### Algorithm
We now describe the algorithm we use to learn the parameters for the above function approximation.
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/algorithm2.png" width="500"></div>
Figure 6: An online linear, gradient descent algorithm TD(lambda) for approximating Q(s,a). 

## EVALUATION
We now describe our evaluation process for our project. 
We break this evaluation into two main parts - with a maze and without a maze. 
Within these two parts, we elaborate on the performance of a baseline, non-intelligent agent and an intelligent agent with different basis functions.

### No Maze

#### Baseline - Random
(baseline random)

#### Baseline - Handcode
(baseline handcode)

#### Learner - 9 Dynamic BFs + 9 Tile Stationary BFs
(description)

#### Learner - 9 Dynamic BFs + 9 Coarse Stationary BFs
(description)

#### Learner - 9 Dynamic BFs 
(description)

### Maze

#### Baseline - Random
(baseline random)

#### Baseline - Handcode
(baseline handcode)

#### Learner - 9 Dynamic BFs + 9 Tile Stationary BFs
(description)

#### Learner - 9 Dynamic BFs + 9 Coarse Stationary BFs
(description)

#### Learner - 9 Dynamic BFs 
(description)


## REMAINING GOALS AND CHALLENGES
(remaining goals and challenges)
