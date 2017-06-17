#
#
# Zombie-Maze-Land
# CS 175
# Edison Weik
#
# random.py
#
# Implements Minecraft environment with the maze and zombies.
# Implements random moving agent.
# Plots results and saves figure.
#


from __future__ import division
import numpy as np
import MalmoPython
import os
import sys
import time
import json
import random
import uuid
import math
import matplotlib.pyplot as plt


height = 229
missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ModSettings>
                  <MsPerTick>75</MsPerTick>
                  <PrioritiseOffscreenRendering>true</PrioritiseOffscreenRendering>
              </ModSettings>
              
              <ServerSection>
                <ServerInitialConditions>
                  <Time>
                    <StartTime>16000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                  </Time>
                  <Weather>clear</Weather>
                  <AllowSpawning>false</AllowSpawning>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
                  <DrawingDecorator>
                    <DrawCuboid x1="-11" y1="226" z1="-6" x2="0" y2="246" z2="5" type="beacon"/>
                    <DrawCuboid x1="-10" y1="227" z1="-5" x2="-1" y2="246" z2="4" type="air"/>
                    <DrawCuboid x1="-2" y1="227" z1="-4" x2="-2" y2="'''+str(height)+'''" z2="-2" type="emerald_block"/>
                    <DrawCuboid x1="-2" y1="227" z1="0" x2="-2" y2="'''+str(height)+'''" z2="3" type="emerald_block"/>
                    <DrawCuboid x1="-9" y1="227" z1="3" x2="-8" y2="'''+str(height)+'''" z2="3" type="emerald_block"/>
                    <DrawCuboid x1="-6" y1="227" z1="3" x2="-4" y2="'''+str(height)+'''" z2="3" type="emerald_block"/>
                    <DrawCuboid x1="-4" y1="227" z1="-2" x2="-4" y2="'''+str(height)+'''" z2="-4" type="emerald_block"/>
                    <DrawCuboid x1="-4" y1="227" z1="0" x2="-4" y2="'''+str(height)+'''" z2="1" type="emerald_block"/>
                    <DrawCuboid x1="-8" y1="227" z1="1" x2="-6" y2="'''+str(height)+'''" z2="1" type="emerald_block"/>
                    <DrawCuboid x1="-9" y1="227" z1="-1" x2="-7" y2="'''+str(height)+'''" z2="-1" type="emerald_block"/>
                    <DrawCuboid x1="-7" y1="227" z1="-2" x2="-7" y2="'''+str(height)+'''" z2="-2" type="emerald_block"/>
                    <DrawCuboid x1="-9" y1="227" z1="-3" x2="-9" y2="'''+str(height)+'''" z2="-3" type="emerald_block"/>
                    <DrawCuboid x1="-9" y1="227" z1="-4" x2="-6" y2="'''+str(height)+'''" z2="-4" type="emerald_block"/>
                    <DrawEntity x="-2" y="227" z="-4.5" type="Zombie" yaw="0"/>
                    <DrawEntity x="-0.75" y="227" z="4" type="Zombie" yaw="180"/>
                    <DrawEntity x="-9.5" y="227" z="4" type="Zombie" yaw="180"/>
                  </DrawingDecorator>
                  <ServerQuitWhenAnyAgentFinishes/>
                  <ServerQuitFromTimeUp timeLimitMs="1000000"/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                  <Name>Survivor</Name>
                  <AgentStart>
                      <Placement x="-4.5" y="227.0" z="-0.5" yaw="0"/>
                  </AgentStart>
                  <AgentHandlers>
                      <MissionQuitCommands quitDescription="give_up"/>
                      <ObservationFromFullStats/>
                      <DiscreteMovementCommands/>
                      <ObservationFromNearbyEntities>
                          <Range name="zombies" xrange="10" yrange="2" zrange="10" />
                      </ObservationFromNearbyEntities>
                      <RewardForMissionEnd rewardForDeath="-1000">
                          <Reward description="out_of_time" reward="0"/>
                      </RewardForMissionEnd>
                  </AgentHandlers>
              </AgentSection>
            </Mission>'''
    
    
class Agent(object):
    def __init__(self):
        """Constructing an RL agent.
        """
        self.episodes = 0
        self.possible_actions = [ 'movenorth 1', 'movesouth 1', 'movewest 1', 'moveeast 1' ]
     
                
    def get_action(self):
        '''
        Output:  action chosen by taking average position of zombies relative to agent
        and going in opposite direction
        '''
        a = random.randint(0, 3)
        return self.possible_actions[a]

    
    def check_health(self, health, agent_host):
        '''
        Checks health of agent. Exits episode if health falls below 20.0. 
        '''
        if health < 20.0:
            self.alive = False
            agent_host.sendCommand( 'move 0' )
            
    
    def observe_state( self, agent_host ):
        '''
        Takes in agent_host.
        Observe state.
        Check if health is diminished.
        '''
        world_state = agent_host.getWorldState()
        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                observations = json.loads(msg)
                self.check_health( observations[u'Life'], agent_host )
                break
        return 


    def act(self, agent_host, current_r):
        '''
        Take 1 action in response to the current world state.
        '''
        # Observe current state to check health
        try:
            self.observe_state( agent_host ) 
        except: 
            return 0
               
        # Act on observation 
        self.action = self.get_action()
        try:
            agent_host.sendCommand( self.action )
        except:
            return 0
            
        return current_r
        
        

    def run(self, agent_host):
        '''
        Run the agent on the world for 1 episode. 
        '''
        # Observe initial state and set variables for episode
        self.alive = True
        self.reward = 0
        total_reward, total_commands = 0, 0
        self.agent, self.z1, self.z2, self.z3, self.action = None, None, None, None, None

        
        # Take first action
        while True:
            world_state = agent_host.getWorldState()
            if world_state.is_mission_running and len(world_state.observations)>0:
                total_reward += self.act(agent_host, self.reward)
                total_commands += 1
                break
            if not world_state.is_mission_running:
                break
        
        # Loop until mission ends:
        while world_state.is_mission_running and self.alive:
            self.reward = 0
            while True:
                time.sleep(0.1)
                world_state = agent_host.getWorldState()
                for reward in world_state.rewards:
                    self.reward += reward.getValue()
                if world_state.is_mission_running and self.alive and len(world_state.observations)>0 and not world_state.observations[-1].text=="{}":
                    total_reward += self.act(agent_host, self.reward)
                    #print "  Action: ", self.action
                    total_commands += 1
                    break
                if not world_state.is_mission_running or not self.alive:
                    break
                        
        # Process final reward and update parameters
        total_reward += self.reward
        return total_reward, total_commands


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
    my_client_pool = MalmoPython.ClientPool()
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))

    # Create default Malmo objects:
    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse( sys.argv )
    except RuntimeError as e:
        print 'ERROR:',e
        print agent_host.getUsage()
        exit(1)
    if agent_host.receivedArgument("help"):
        print agent_host.getUsage()
        exit(0)
    
    
    # initialize parameter vector and basis functions
    Survivor = Agent()
    total_commands, total_episodes = list(), list()
    # Repeat 10 times to get averages
    for iteration in range(5):
        print "Iteration "+str(iteration+1)
        times, episodes, commands = [], [], []
        for iRepeat in range(100):
            my_mission = MalmoPython.MissionSpec(missionXML, True)
            my_mission_record = MalmoPython.MissionRecordSpec()
        
            # Attempt to start a mission:
            max_retries = 3
            for retry in range(max_retries):
                try:
                    agent_host.startMission( my_mission, my_client_pool,  my_mission_record, 0, "Survivor" )
                    break
                except RuntimeError as e:
                    if retry == max_retries - 1:
                        print "Error starting mission:",e
                        exit(1)
                    else:
                        time.sleep(2)

            # Loop until mission starts:
            world_state = agent_host.getWorldState()
            while not world_state.has_mission_begun:
                time.sleep(0.1)
                world_state = agent_host.getWorldState()
        
            # Run Mission
            print "Episode " + str(iRepeat) + ":",
        
            # Run episode
            start_time = time.time()
            _, c = Survivor.run( agent_host )
            time_alive = time.time() - start_time
            times.append( time_alive )
            commands.append( c )
            episodes.append( iRepeat )
            # Episode has ended.
            
            print "Alive for " + str(c) + " commands and " + str(time_alive) + " seconds"
            agent_host.sendCommand( "quit" ) 
            while world_state.is_mission_running:
                world_state = agent_host.getWorldState()
                pass
            time.sleep(1)
    
    
        # Plot results from learner
        m, b = np.polyfit(episodes, commands, 1)
        line_fit = [ float(m)*x + float(b) for x in episodes ]
        plt.scatter( episodes, commands, s=1, c='black' )
        plt.plot(episodes, line_fit, '-')
        plt.xlabel( "Episodes" )
        plt.ylabel( "Time Steps" )
        plt.title( "Random" )
        plt.savefig("/Users/edisonweik/Desktop/cs175/maze_plots/baseline-random/maze_random" + str(iteration) + ".pdf")
        plt.close()
        
        total_commands.extend(commands)
        total_episodes.extend(episodes)
    
    m, b = np.polyfit(total_episodes, total_commands, 1)
    average = float( sum(total_commands) ) / len(total_commands)
    line_fit = [ float(m)*x + float(b) for x in episodes ]
    plt.scatter( total_episodes, total_commands, s=1, c='black', label="Avg="+str(average) )
    plt.plot(episodes, line_fit, '-', color='b')
    
    ## Plot with error bars
    x_error = np.array([0,10,20,30,40,50,60,70,80,90])
    y_error = np.array( [ float(m)*x + float(b) for x in x_error ] )
    bins = [ [] for i in range(10) ]
    for i,time_steps in zip(total_episodes, total_commands):
        for j in [0,10,20,30,40,50,60,70,80,90]:
            if j in [i, i-1, i+1]:
                bins[int(round(j/10))].append(time_steps)
    error = np.array( [ np.std(a) for a in bins ] )
    plt.errorbar(x_error, y_error, yerr=error,  ecolor='b', elinewidth=0.75)
    
    plt.legend()
    plt.xlabel( "Episodes" )
    plt.ylabel( "Time Steps" )
    plt.title( "Random - Total" )
    plt.savefig("/Users/edisonweik/Desktop/cs175/maze_plots/baseline-random/maze_random_total.pdf")
    
    
    
    
    
   