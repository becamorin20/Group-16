---
layout: default
title: Status
---

# (GROUP NAME?) PROJECT STATUS - 5/26/2016

## PROJECT SUMMARY
The goal of this project is to survive for as long as possible in a 10x10 block environment with a maze and three zombies placed somewhere in the maze. The agent starts off in the middle of this environment. The zombies are placed at three pre-chosen spots. The agent must survive for as long as possible. See figure below for visualization:
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/maze.png" width="600"></div>
Figure 1: Picture of 10x10 maze environment for Malmo-Minecraft agent. Black spots indicate walls. White spots indicate free path. Green spot indicates starting position of agent. Red spot indicates starting position of zombies.

## APPROACH
We are using reinforcement learning to learn how to survive in the maze, specifically, we attempt to learn a Q-function to approximate a Q-table. 

In this environment, we start off with 10x10 = 100 grid positions, 4 possible discrete actions (movenorth 1, movesouth 1, movewest 1, moveeast 1), and 4 total entities. 
Using a Q-table, we would have to keep track of possibly 4 x 100<sup>4</sup> possible state-action pairs (4 for each action and 100x100x100x100 for each possible position of each entity). 
This is too large a number for us to expect to keep track of, so we approximate this table with a list of 72 parameters 
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/theta_list.png" width="250"></div>.

To represent the state in our approximation, we use 72 basis functions as features:
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/basis_functions.png" width="600"></div>.

More precisely, we represent our state by breaking it down into 18 partitions: 9 dynamic partitions that move with the agent so that the agent is always at the center of this sub-space, and 9 stationary partitions that allow the agent to know which region of the environment the agent is in.
This is visualized as followed in the figures below, along with reasoning for them at the bottom:
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/basis_dynamic.png" width="250"></div>.
Figure 2: Picture of 9 dynamic partitions as basis functions. Green spot indicates position of agent. Red spots indicate position of zombies.
The basis function for each partiton returns an integer indicating how many zombies are in that particular partition. 
Possible integers include: 0,1,2,3.
<div align="center"><img src="https://github.com/becamorin20/Group-16/blob/master/docs/images/basis_dynamic2.png" width="250"></div>.
Figure 3: Picture of 9 dynamic partitions as basis functions. Green spot indicates position of agent. 
The partitions move with the agent so that the agent is always at its center.  
This allows us to keep track of the proximity of zombies to the agent.


## EVALUATION
(evaluation)

## REMAINING GOALS AND CHALLENGES
(remaining goals and challenges)
