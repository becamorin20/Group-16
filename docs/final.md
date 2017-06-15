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
**Figure 1**: Picture of 10x10 maze environment for Malmo-Minecraft agent. 
Black spots indicate walls. White spots indicate free path. 
Green spot indicates starting position of agent. 
Red spot indicates starting position of zombies.
<br><br>
The challenges of this problem are using the maze to the agents advantage in surviving and accomodating a large state space. 
Without a maze, the agent really only has one general optimal path, that is, to go the corner where there are no zombies, until it gets killed.
The agent is not fast enough to outrun the zombies, so it always gets killed quickly unless it starts immediately running to the safest spot - the corner.
With the maze, the agent has an opportunity to survive for a long time by hiding from the zombies in the maze. 
Zombies only attack when they see the agent, so the agent can use his/her "smarts" to survive longer - this is where we use an AI/ML algorithm.
We use reinforcement learning for this problem, specifically Q-learning. 
<br><br>
We consider this task non-trivial because of its large state space. 
Using a table to keep track of the state-action pairs, we would have to keep track of approximately $$100^4$$ or $$10^8$$ values ($$100 \cdot 100 \cdot 100 \cdot 100$$ for each possible permutation of positions for each entity).
This is too large a number for traditional Q-tabular learning.
Therefore, we approximate the Q-table with a parameterized function. 
We believe this can be considered non-trivial because of the numerous ways we can represent the state via basis functions (BFs).
Some set of basis functions may be better than others.
Creativity and experimenting with different combinations of BFs was required.
<br><br>
Another reason we consider this non-trivial is because it was not one of the examples that Malmo provided nor did we use an off the shelf program. 
We did take away a lot from the examples from Malmo, especially things concerning the environment XML.
But for the most part we coded our own parameters, our own updates, and our own basis functions using mainly books as references.

<br><br>

## Approaches
Use another level-two header called Approaches, In this section, describe both the baselines
and your proposed approach(es). Describe precisely what the advantages and disadvantages of each are,
for example, why one might be more accurate, need less data, take more time, overfit, and so on. Include
enough technical information to be able to (mostly) reproduce your project, in particular, use pseudocode
and equations as much as possible.

### Baseline
We considered two baselines for our project. One was a randomly moving agent and one was an agent moving according to the mob_fun.py algorithm from a Malmo example.

#### Random
Randomly pick an action each time. 
One possible advantage of this is that the agent doesn't have to do a lot of calculations in order to update parameters and pick an action, unlike our RL agent. 
This can allow the agent to possibly move quicker.
However, we consider this advantage marginal.

Obviously a disadvantage of this algorithm is its inability improve or make decisions based on its position and the relative position of zombies.

#### Mob Fun Algorithm
The mob fun agent works by continually moving straight forward and then gradually angling its movement (i.e. turning) using a score to determine the turn angle. 
The turn score is determined using a sum of a weighted cost of turning, cost of entity proximity, and cost of proximity to edges.
We copied directly from the weights used by the Malmo example, where the turn weight was $$0$$, the entity proximity weight was $$-10/(distance$$ $$to$$ $$entity)$$, and the proximity to edge weight was $$-100/(distance$$ $$to$$ $$wall)^4$$ for each wall.

One advantage of this algorithm is its use of continuous actions. 
The agent is constantly moving, never stopping to make calculations. 
The only commands it sends are the angle which to turn by. 
This allows the agent to move faster and survive longer because zombies may have a harder time catching it.

One disadvantage of this algorithm is its inability to improve over time. 
Using the same starting state, the agent always moves in the same initial direction, deviating its path only slightly depending on the movements of the zombies. 

### Markov Decison Process (MDP)
We first describe our Markov Decision Process.

Our **_reward function_** is $$-1000$$ for death. 

Our **_action space_** is ($$\leftarrow$$, $$\uparrow$$, $$\downarrow$$, $$\rightarrow$$). 
In Malmo, this is ('moveeast1', 'movenorth 1', 'movesouth 1', 'movewest 1').

As we described earlier, our state consists of 100 blocks and 4 entities (3 zombies + 1 agent). 
Our state space then includes $$10^8$$ values. 
This is too large, so we approximate our **_state space_** with sets of basis functions (BFs) $$\phi$$:

<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/phi.png" width="600"></div>

We tried multiple different basis functions and multiple combinations of them. 
In the evaluation we will see the different BF combinations we used.
In the rest of this section we will go through the different sets of basis functions we experimented with (not combinations of them).

#### 9 Dynamic Basis Functions
9 dynamic basis functions (BFs) that move with the agent so that the agent is always at the center of this sub-space. 
These BFs keep track of how many zombies are in each BF/partition.
They return an integer indicating how many zombies are in that particular region. 
Possible values include $${0,1,2,3}$$.
This allows our agent to know the general position of each zombie relative to him/her. 
They do not keep track of the agents position since the agent is always at the center.

We also modify out middly dynamic BF, _p5_, to add a constant $$0.5$$ if a wall is in it's region. 
This means that the possible values for this BF are $${0,0.5,1,1.5,2,2.5,3,3.5}$$, instead of $${0,1,2,3}$$.
These modifications give our agent another advantage by letting him know if he is getting too close to a wall and boxing him/her self in.

This can be seen in the figure below.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/dynamic_bfs.png" width="600"></div>
**Figure 2**: Images of 9 dynamic partitions as basis functions. Green spot indicates position of agent. Red spots indicate position of zombies.

<br><br>

#### 9 Tile Stationary Basis Functions
We will now examine some the stationary BFs we used. The stationary basis functions only keep track of the agent's position. They do not keep track of zombies. All of our stationary BFs are taken from Sutton and Barto's _Reinforcement Learning: An Introduction_, chapter 8.

An advantage of these BFs is that "the overall number of features that are present at one time is strictly controlled and independent of the input state" (Sutton and Barto).
A disadvantage is that they do not let the agent know precisely where he is, only the general region. 
See the image below:

<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/basis_stationary1.png" width="350"></div>
**Figure 3**: Image of 9 tile stationary basis functions. If the agent is in the region of a particular BF, it returns 1, otherwise 0.

<br><br>

#### 9 Coarse Stationary Basis Functions
These BFs are very similar to the stationary tile BFs. 
They both have essentially the same advantages and disadvantages.
One further advantage the coarse circular BFs may have is that they overlap, which can possibly let the agent know more precisely where he/she is. See the image below:

<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/basis_stationary2.png" width="350"></div>
**Figure 4**: Image of 9 coarse circular stationary basis functions. If the agent is in the region of a particular BF, it returns 1, otherwise 0. The radius of each circle is 2.5 unit blocks.

<br><br>

#### 9 Gaussian Radial Basis Functions (stationary)
This set of BFs is new to our project $$-$$ it was not in our status report. From Sutton and Barto:

"Radial basis functions (RBFs) are the natural generalization of coarse coding to continuous-valued features. 
Rather than each feature being either 0 or 1, it can be anything in the interval [0,1], reflecting various _degrees_ to which the feature is present."

Our features, $$(x,y)-$$Cartesian coordinates, are continuous, so it seems natural to represent them using these Gaussian RBFs. 
At first, we were apprehensive because of the symmetricity of our BFs about its center. 
But we later realized this would be offset by the values of the other BFs $$-$$ that is, if 2 points were symmetric about a particular BF, that BF would return the same value for both, but all the other BFs would return different values (albeit small values) that would in theory help distinguish the 2 points.

We use a Gaussian function for each region, where each function is dependent on the distance between the state _s_ and features prototypical center $$c_i$$, and on the standard deviation $$\sigma$$:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/gaussian3.png" width="400"></div>

An image and description of our Gaussian RBFs can be seen below:

<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/gaussian_rbf2.png" width="500"></div>
**Figure 5**: Image of 9 Gaussian radial basis functions. We use the same centers as we do for the coarse stationary BFs (figure 4). At the center of each BF, that BF will return 1. We set our standard deviation $$\sigma$$ to 1.25 unit blocks. We choose this number so that 2 standard deviations is equal to the radius of the coarse circular stationary BFs we used earlier.

<br><br>

#### 25 Tile Stationary Basis Functions
We will now see extensions of previous BFs we tried. 
These next sets of BFs are designed to smaller and more granular and have the advantage of being more precise in letting the agent know where he/she is. 

Some disadvantages these BFs may have is the extra computation involved and the problem of exploring all the possible states sufficiently.
With more basis functions, it becomes harder to explore every single state multiple times to get good experience, especially since we only train for 100 iterations. 
This brings us to the time problem. 
We couldn't train all of our agents for more than 100 iterations due to the time it took. 
Training 100 iterations with the maze took on average 1 hour.
Training 100 iterations 5 times for each agent would take about 5 hours per agent. 
This was a big constraint which we were not able to resolve.

<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/tile25.png" width="400"></div>
**Figure 6**: Image of 25 tile stationary basis functions. If the agent is in the region of a particular BF, it returns 1, otherwise 0. This is an extension of our original attempt at tile BFs in order to see if more granularity in the state represention would produce better results.

<br><br>

#### 25 Coarse Stationary Basis Functions
This has the same advantages and disadvantes as the 25 tile BFs.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/coarse25.png" width="400"></div>
**Figure 7**: Image of 25 coarse circular stationary basis functions. If the agent is in the region of a particular BF, it returns 1, otherwise 0. The radius of each circle is $$\sqrt{2}$$ unit blocks. This is an extension of our original attempt at coarse BFs in order to see if more granularity in the state represention would produce better results.

<br><br>

### Algorithm
Now that we've seen the many different BFs used - we'll look at the algorithm we use. 
First, we show that we approximate our Q-function with a parametric approximator:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/q_function.png" width="300"></div>

We try many different types of basis functions:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/phi.png" width="600"></div>
and learn many different sets of parameters:
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/theta_final.png" width="350"></div>
For each evaluation, we'll specify how many BFs and parameters we use.

Our algorithm learns the parameters $$\theta$$ for our Q-approximator. 
Notice that we use an eligibility trace vector instead of just the gradient. 
This allows us to incorporate a sense of backtracking when updating states so that when we do reach the terminal state, previous states are also updated in proportion to the how far it's been since they were visited.
A full description of the algorithm can be found in Sutton and Barto's _Reinforcement Learning: An Introduction_, Chapter 8. 
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/alg4.png" width="500"></div>
**Figure 8**: An online linear, gradient descent Q-learning algorithm for approximating Q(s,a) with eligibility tracing and an $$\epsilon -$$greedy exploration.

Currently, we have our hyperparameters set as $$\lambda=0.9$$, $$\epsilon=0.1$$, and $$\alpha=0.05$$. Both $$\epsilon$$ and $$\alpha$$ gradually decrease over time so that they are set to $$0.001$$ and $$0.0001$$, respectively, by the end of training.

<br><br>

## Evaluation
**_How we evaluated our agents_**: To evaluate each agent (both baseline and Q-learner), we ran each agent through 100 episodes five times in order to get an average performance of each agent.
For each different agent, we show the plots of the performances for each of the five iterations, as well as plot of the cumulative data.
For the cumulative data plots, we show the average performance of each agent as well as add error bars that show one standard deviation from the line at that point.
We calculate the standard deviation at each point shown using the sample points near that point (using numpy).
Note that the standard deviation shown is not centered at the mean of the points from which it was sampled - it is centered at the point on the linear fit - so it may look off.

_Note_: Unlike the status report, we only evaluate agents in a maze environment. We don't evaluate any agent in a no-maze setting.

### Baseline - Random moving agent
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/random_final.png" width="600"></div>
**Figure 9**: On average, the randomly moving agent survives for $$\sim50$$ time steps in the maze.

### Baseline - Handcode agent (mob fun algorithm)
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/handode_maze_final.png" width="600"></div>
**Figure 10**: On average, the agent moving according to the mob fun algorithm survives for $$\sim115$$ time steps in the maze.

### Q-Approximation - 9 Dynamic BFs + 9 Tile stationary BFs
For this agent, we used 18 total basis functions for each action: 9 dynamic BFs (figure 2) and 9 tile stationary BFs (figure 3). 
In total, for this agent we used 72 BFs and 72 parameters.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/9tile_final.png" width="600"></div>
**Figure 11**: On average, this agent survived for approximately $$87$$ time steps. There also appears to be a lot more variation in the error bars here than in the baseline (this is present in all of our learners).

### Q-Approximation - 9 Dynamic BFs + 9 Coarse stationary BFs
For this agent, we used 18 total basis functions for each action: 9 dynamic BFs (figure 2) and 9 Gaussian stationary BFs (figure 4). 
In total, for this agent we used 72 BFs and 72 parameters.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/9coarse_final.png" width="600"></div>
**Figure 12**:  On average, this agent survived for approximately $$90$$ time steps with a lot of variation.

### Q-Approximation - 9 Dynamic BFs + 9 Gaussian stationary RBFs
For this agent, we used 18 total basis functions for each action: 9 dynamic BFs (figure 2) and 9 Gaussian stationary BFs (figure 5). 
In total, for this agent we used 72 BFs and 72 parameters.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/9gaussian_final.png" width="600"></div>
**Figure 13**: On average, this agent survived for approximately $$109$$ time steps with a lot of variation.

### Q-Approximation - 9 Dynamic BFs + 25 Tile stationary BFs
For this agent, we used 34 total basis functions for each action: 9 dynamic BFs (figure 2) and 25 tile stationary BFs (figure 6). 
In total, for this agent we used 136 BFs and 136 parameters.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/25tile_final.png" width="600"></div>
**Figure 14**: On average, this agent survived for approximately $$76$$ time steps.

### Q-Approximation - 9 Dynamic BFs + 25 Coarse stationary BFs
For this agent, we used 34 total basis functions for each action: 9 dynamic BFs (figure 2) and 25 tile stationary BFs (figure 7). 
In total, for this agent we used 136 BFs and 136 parameters.
<div align="center"><img src="//raw.githubusercontent.com/becamorin20/Zombie-Maze-Land/master/docs/images/25coarse_final.png" width="600"></div>
**Figure 15**: On average, this agent survived for approximately $$136$$ time steps with a lot of variation.

### Average performance of all agents
We now compare the average performances of all the agents

Random: average$$=49.744$$, std deviation$$=16.272$$

Handcode: average$$=114.408$$, std deviation$$=30.580$$

9 Tile: average$$=87.036$$, std deviation$$=36.904$$

9 Coarse: average$$=90.16$$, std deviation$$=35.115$$

9 Gaussian: average$$=109.484$$, std deviation$$=48.092$$

25 Tile: average$$=76.74$$, std deviation$$=28.771$$

25 Coarse: average$$=136.524$$, std deviation$$=44.198$$

<br><br>

## Conclusion
In conclusion, 

## References
Sutton, Richard and Barto, Andrew. [Reinforcement Learning: An Introduction](http://incompleteideas.net/sutton/book/ebook/the-book.html)

Busoniu, Lucian, Babuška, Robert, De Schutter, Bart, and Ernst, Damien. _Reinforcement learning and dynamic programming using function approximators_. Boca Raton, Florida: CRC Press, 2010. Print

[Malmo Github](https://github.com/Microsoft/malmo)

[Malmo API documentation](https://microsoft.github.io/malmo/0.21.0/Documentation/index.html)

All images used in this project were created on the computer of Edison Weik.
