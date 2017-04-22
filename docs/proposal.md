---
layout: default 
title: Proposal
---
## Summary  
##### In this project, we will train our agent (in the video game Minecraft) to learn how to survive as long as possible in it's world. We plan on implementing reinforcement learning for this project. The main objectives would be for the agent to be able to find and collect all the essential materials needed to survive such as food (and learn how to kill for meat) and tools (to be able to protect itself). It should also be able to learn how to navigate in the terrain it is in, such as how to climb mountains/hills, how to swim, and how to go around/ get over obtacles (e.g. trees). At the same time, it will have to learn how to defend itself from zombie attacks (and possibly animal attacks). 
##### Information we expect to use as input include the state/environment, be it the position in the space, velocity, type of ground we're standing on, available tools/resources, threats, etc (we haven't figured out exactly yet all the possible variables). We expect this to produce as output a (state, action) pair, ultimately resulting in an action taken and a new state for which we use as the next input. 
##### Applications could include robotics and how they navigate their environments safely. Examples range from something as simple as trash collectors to something like complex like the Mars rover.

## AI/ML Algorithms 
##### We plan on using reinforcement learning with Q-Learning on the agent to train it to maximize it future rewards. Perhaps extending to or utilizing a functional approximation version should our state space become too large.

## Evaluation Plans 
##### Quantitatively, some metrics to evaluate our agent will be: time it has stayed alive (before time runs out), average Q-value, rewards (point/s) obtained from episodes, performance navigating the environment, number of kills (zombies), material collected. For our baseline we will give the agent a time limit (eg 5 minutes) to collect its performance and improvements. We expect to evaluate our data in a similar manner that we train it - via Minecraft simulations. We're not exactly sure what to expect improvement wise; obviously this will be an improvement in performance over random actions, but how well, we're not sure.
##### Qualitatively, we will visualize the performance of our algorithms with graphs of time-alive as a function of episodes, rewards as a function of episodes, and other metrics as a funciton of episodes. We might even visualize these metrics as a function of steps in an episode as well. Our moonshot really is to get all of this working. We'll start with something essential like navigating safely, then move on to surviving against attacks and collecting resources, and determine where to take it from there.
