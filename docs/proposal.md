---
layout: default 
title: Proposal
---
## Summary  
#### In this project, we will train our agent (in the video game Minecraft) to learn how to survive as long as possible in it's world. We plan on implementing reinforcement learning so that it is able to meet its goal. The main objectives to complete the latter would be for the agent to be able to find and collect all the essential materials needed to survive such as food (and learn how to kill for meat) and tools (to be able to protect itself). Concurently, it should be able to learn how to navigate in the terrain it is in, such as how to climb mountains/hills, how to swim, and how to go around/ get over obtacles (eg trees). At the same time as it is learning the latter, it will have to learn how to defend itself from zombie attacks (and possibly animal attacks if it is killing). Once it is has leared how to do this will ease it's next priority will be to create a world for itself (such as building for shelter). 
#### We will create the reinforcement learning tasks as a Mark Decision Process. The agent will take in it's interactions with the environment through observations and actions and depending on the outcomes it will have a reward system. With each action the agent does the state will change based on the reward system (if the interaction was positive or negative) thus changing the way it will interact/act the next time.

## AI/ML Algorithms 
#### We plan on using reinforcement learning with Q-Learning on the agent to train it to maximize it future rewards.

## Evaluation Plans 
#### Our metrics to evaluate our agent will be: time it has stayed alive (before time runs out), average Q-value, rewards (point/s) obtained from episodes, performance navigating the environment, number of kills (zombies), material collected. For our baseline we will give the agent a time limit (eg 5 minutes ) to collect its performance and improvements. 
