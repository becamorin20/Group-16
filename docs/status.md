---
layout: default
title: Status
---

# PROJECT STATUS - 5/26/2017

## Video
<iframe width="500" height="400" src="https://youtu.be/embed/LjnAuq_4ytM" frameborder="0" allowfullscreen></iframe>


## PROJECT SUMMARY
The goal of this project is to have an agent survive for as long as possible in a 10x10 block environment with a maze and three zombies placed somewhere in the maze. The agent starts off in the middle of this environment. The zombies are placed at three pre-chosen spots. The agent must survive for as long as possible. See figure below for visualization:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/maze.png" width="500"></div>
Figure 1: Picture of 10x10 maze environment for Malmo-Minecraft agent. Black spots indicate walls. White spots indicate free path. Green spot indicates starting position of agent. Red spot indicates starting position of zombies.

## APPROACH
We are using reinforcement learning to learn how to survive in the maze, specifically, we attempt to learn a Q-function to approximate a Q-table. 

### Markov Decison Process (MDP)
We first describe our Markov Decision Process.

Our reward function is -1000 for death. 

For our states and actions, we start off with 10x10 = 100 grid positions, 4 possible discrete actions (movenorth 1, movesouth 1, movewest 1, moveeast 1), and 4 total entities. 
Using a Q-table, we would have to keep track of possibly 4 x 100<sup>4</sup> possible state-action pairs (4 for each action and 100x100x100x100 for each possible permutation of positions of each entity). 
This is too large a number for us to expect to keep track of, so we approximate our state-action pairs with a list of 72 parameters 
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/theta_list.png" width="250"></div>

To represent the state in our approximation, we use 72 basis functions as features:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/basis_functions.png" width="600"></div>

More precisely, we represent our state by breaking it down into 18 partitions: 9 dynamic partitions that move with the agent so that the agent is always at the center of this sub-space, and 9 stationary partitions that allow the agent to know which region of the environment the agent is in.
We are currently experimenting with a couple different stationary sets of partitions.
This is all visualized as followed in the figures below, along with descriptions for them:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/basis_dynamic.png" width="350"></div>
Figure 2: Picture of 9 dynamic partitions as basis functions. Green spot indicates position of agent. Red spots indicate position of zombies.
The basis function for each partiton returns an integer indicating how many zombies are in that particular partition. 
Possible integers include: 0,1,2,3.

.

.

<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/basis_dynamic2.png" width="350"></div>
Figure 3: Picture of 9 dynamic partitions as basis functions. Green spot indicates position of agent. 
The partitions move with the agent so that the agent is always at its center.  
This allows us to keep track of the proximity of zombies to the agent.

.

.

<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/basis_stationary1.png" width="350"></div>
Figure 4: Picture of 9 stationary partitions as basis functions. 
These partitions never move. Based off the "tile" basis functions from Sutton and Barto's _Reinforcement Learning: An Introduction_ .
The basis function for each partiton returns an 1 if the agent is in it, 0 otherwise.
They do not keep track of zombie positions.

.

.

<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/basis_stationary2.png" width="350"></div>
Figure 5: Picture of 9 stationary partitions as basis functions. 
These partitions never move.
These circular partitions have radius 2.50 unit blocks. Based off the "coarse" basis function from Sutton and Barto's _Reinforcement Learning: An Introduction_ .
The basis function for each partiton returns an 1 if the agent is in it, 0 otherwise.
They do not keep track of zombie positions.

---------------------------------------------------------------------------------------------------------------------------------------

For each of our 4 actions we allow a set of 18 basis functions, thus giving us 72 total basis functions and 72 total parameters.

So our MDP consists of reward function of -1000 for death and these 72 basis functions and parameters.

### Algorithm
We now show the algorithm we use to learn the parameters for the above function approximation. A full description of the algorithm can be found in Sutton and Barto's _Reinforcement Learning: An Introduction_ chapter 8. One key thing to note is that epsilon and alpha are monotonically decreasing functions of k.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/algorithm3.png" width="500"></div>
Figure 6: An online linear, gradient descent algorithm TD(lambda) for approximating Q(s,a) with eligibility tracing and an epsilon-greedy exploration.

## EVALUATION
We now describe our evaluation process for our project. 
We break this evaluation into two main parts - with a maze and without a maze. 
Within these two parts, we elaborate on the performance of a baseline, non-intelligent agent and an intelligent agent with different basis functions.
All of our individual evaluations are trained on 100 iterations/episodes.
We did this because of time constraints with the deadline, but plan on expanding this number later.

For each episode, we measure the number of commands sent by the agent while it is alive. 
We then plot all of these data points for each evaluation onto a scatterplot and fit a 1-degree polynomial (using numpy) to the data.
Be aware that each plot contains a lot of noise.

### No Maze
To start our evaluation, we set our agent in a grid environment without a maze.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/no-maze.png" width="450"></div>
Figure 7: 10x10 maze environment without a maze. 
Green spots indicate starting position of agent. 
Red sports indicate starting position of zombies.

#### Baseline - Random
Our first agent consisted of completely random motions. 
We expected to see no improvement by the random moving agent and after running the program we see that performance slightly declines.
We believe this may just be noise and that running this program with more episodes would show a more constant performance.

From the plots we see that the average number of commands alive each episode by the agent is approximately 23 commands.
This will serve as a baseline to compare our "intelligent" agents with.
The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/no-maze-random-100-2.png" width="400"></div>
Figure 8: Scatter plot of random agent performance in a no maze environment with linear fit. 
We see negative performance in this plot over time.

#### Baseline - Handcode (Mob Fun Algorithm)
The second baseline we used was the algorithm used in mob_fun.py from the Python_Examples folder given by Malmo. 
We expected, again, to see no improvement by the agent since we are updating no parameters or Q-table and after running the program we see that (although, again, with a lot of background).
The agent's moves are a deterministic function of its position and the relative positions of the zombies.

From the plots we see the average performance of this agent is ~22-23 commands alive per episode.
This is, surprisingly, on pace with the random moving agent.
We believe that this may be so because the random moving agent is hard to catch because it moves quickly and randomly and that perhaps the optimal amount of commands any agent can stay alive before being converged on by the zombies is ~22-23 commands.
This will also serve as a baseline to compare to our "intelligent" agent. 
The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/no-maze-handcode.png" width="400"></div>
Figure 9: Scatter plot of handcoded agent performance in a no maze environment with linear fit.
The agent shows no improvement and stays alive for about 22-23 commands per episode on average.


#### Learner - 9 Dynamic BFs + 9 Tile Stationary BFs
The first "intelligent" agent we evaluate is an agent using the Q-learning algorithm (figure 6) with 9 dynamic basis functions (figure 2) and 9 tile stationary basis functions (figure 4).

We expected to see improvement in this agent and hoped to see it meet or exceed the performance of the two baselines.
From the plots, we see that performance did improve marginally as time continues, but the performance never caught up to that of the handcoded or random agent.

The agent stayed alive for ~15-16 commands per episode.
The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/no-maze-tile-100.png" width="400"></div>
Figure 10: Scatter plot with linear fit of Q-learner with tile stationary BFs in no maze environment.
The agents shows marginal improvement and stays alive for ~15-16 commands per episode.

#### Learner - 9 Dynamic BFs + 9 Coarse Stationary BFs (as seen in video)
The second "intelligent" agent we evaluate is an agent using the Q-learning algorithm (figure 6) with 9 dynamic basis functions (figure 2) and 9 coarse stationary basis functions (figure 5).

The performance of this agent did improve more considerably than the learner with the tile stationary BFs, but it still never caught up to the performance of the handcoded or random agent.
We believe the improved performance of this learner over that of the tile learner can be perhaps because of the overlap in the coarse stationary BFs. 
This can possibly give the agent a more precise indication of his/her position and allow him/her to navigate the environment better.

The agent started out with about 17 commands alive per episode at the beginning of training and ended up at about 20 commands alive per episode. 
Looking at the agent in training (and as seen in the video), the agent is able to learn to manuver to the bottom right corner of the environment where the zombies are furthest away.
Once there, it appears to try to avoid the zombies, but does not succeed.
The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/no-maze-coarse-100.png" width="400"></div>
Figure 11: Scatter plot with linear fit of Q-learner with coarse stationary BFs in a no maze environment.
The agents does improvement and manages to stay alive for ~20-21 commands per episode by the end of training.
We again see a lot of noise present in the data.

#### Learner - 9 Dynamic BFs 
The final "intelligent" agent we evaluate is an agent using the Q-learning algorithm (figure 6) with 9 dynamic basis functions (figure 2) and 0 stationary BFs.

This was an interesting case because here the agent would only know the relative positions of zombies.
It would have no knowledge of its own position in the environment.

The performance of this agent was poor and actually worsened over time.
As we see in the plots, the agent starts off with ~17 commands per episode before death.
But over time, the agents learns a set of parameters that lead it to ~14-15 commands per episode.

The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/no-maze-no-stationary-100.png" width="400"></div>
Figure 12: Scatter plot with linear fit of Q-learner with no stationary BFs in a no maze environment.
The agent shows regressing performance and manages to stay alive for only ~14-15 commands per episode by the end of training.


### Maze
We now evaluate our agent in a maze.
See figure 1 for the exact representation of the maze. 

#### Baseline - Random
The first baseline with a maze is a randomly moving agent. 

The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/maze-random-100.png" width="400"></div>
Figure 13: Scatter plot with linear fit of random agent in maze environment. The agents performs near a constant 80-70 commands per episode.

#### Baseline - Handcode (Mob Fun Algorithm)
The second baseline with a maze is an agent moving according to the mob_fun.py algorithm.

The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/maze-handcode-100.png" width="400"></div>
Figure 13: Scatter plot with linear fit of agent with mob fun algorithm in maze environment. The agents performs at a constant ~210 commands per episode.

#### Learner - 9 Dynamic BFs + 9 Tile Stationary BFs
The first "intelligent" agent we evaluate is one trained with 9 dynamic BFs (figure 2) and 9 stationary tile BFs (figure 4).

This agent showed little to no improvement over the course of training. 
Based on this agent's performance in the no-maze model, we expected something similar to what we saw.
This agent still outperformed the random moving agent, unlike in the no maze model.
The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/maze-q-tile-100.png" width="400"></div>
Figure 15: Scatter plot with linear fit of Q-learner with 9 dynamic BFs and 9 stationary tile BFs. The plot shows marginal improvement during training.


#### Learner - 9 Dynamic BFs + 9 Coarse Stationary BFs (as seen in video)
The second "intelligent" agent we evaluate is one trained with 9 dynamic BFs (figure 2) and 9 stationary coarse circular BFs (figure 5).

This agent showed nice improvement over training as it nearly doubled its performance. 
By the end of training, it was even able to catch up to the performance of the mob fun handcoded agent. 

The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/maze-q-coarse-100.png" width="400"></div>
Figure 16: Scatter plot with linear fit of Q-learner with 9 dynamic BFs and 9 stationary coarse circular BFs. The agent shows improvement and is able to go from 100 commands alive per episode to nearly 200 commands alive per episode by the end of training 100 iterations.

#### Learner - 9 Dynamic BFs 
The final "intelligent" agent we evaluate is one trained with 9 dynamic BFs (figure 2) and 0 stationary BFs.

This agent, surprisingly, showed nice improvement, considering this agent's performance in the no maze environment. 
While it ultimately did not perform as well as the other agents, this agent did improve its performance by nearly doubling the average amount of commands alive per episode over training.
It surpassed the performance of the random moving agent and nearly caught up to the performance of the tile agent.

The results can be seen in the figure below:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/maze-q-no-stationary-100.png" width="400"></div>
Figure 17: Scatter plot with linear fit of Q-learner with 9 dynamic BFs and 0 stationary BFs. The agent shows improvement and is able to go from 50 commands alive per episode to 100 commands alive per episode by the end of training 100 iterations.


## REMAINING GOALS AND CHALLENGES
### Goals
Over the next few weeks we hope to experiment with different types of basis functions and increase our parameter/BF set in order to represent more knowledge about the state. 
Currently, our model is limited in its granularity of approximating the state and in its inability recognize walls/boundaries and how they can box in the agent. 
We hope that adding some extra features will be able to solve these issues and improve performance.

Also, we hope to increase our training to go from 100 iterations to 500 iterations. 
This will hopefully give us a better indication of the average performance and improvement of each agent over time and will hopefully produce clearer plots.

Another thing we may want to try is to add another unique baseline agent. Although this is low on our priority list.

### Challenges
One of the challenges we face as the final deadline approaches include dealing with time. 
Each episode take somewhere between 10 to 60 or more seconds, thus training 100 iterations can often take more than an hour. 
Trying new combinations of basis functions and training for 500 iterations will be time costly.
This will likely limit our ability to try the many different basis functions we can think of.
Right now no obvious solution to this exists other than running our code constantly.

