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


The challenges of this problem are for the agent to use the maze to its advantage in surviving and accomodating a large state space. 
Without a maze, the agent really only has one general optimal path, that is, to go the corner where there are no zombies, until it gets killed.
The agent is not fast enough to outrun the zombies, so it always gets killed quickly unless it starts immediately running to the safest spot - the corner.
With the maze, the agent has an opportunity to survive for a long time by hiding from the zombies in the maze. 
Zombies only attack when they see the agent, so the agent can use his/her "smarts" to survive longer - this is where we use an AI/ML algorithm.

We consider this task non-trivial because of its large state space. 


## Approaches

## Evaluation

## References
