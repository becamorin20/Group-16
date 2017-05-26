#
# Zombie-Maze-Land
# CS 175
# Edison Weik
#
# zombie_maze.py
#
# Implements Minecraft environment with the maze and zombies.
# Imports and works with learning algorithm .py file.
# Can try different learning algorithms by (un)commenting q_approximation* file.
# Plots results from Q-learner and saves figure.
#

from __future__ import division
import numpy as np
import MalmoPython
import os
import sys
import time
import json
import random
#from q_approximation_coarse import *
#from q_approximation_tile import *
from q_approximation_no_stationary_basis import *
import matplotlib.pyplot as plt


height = 229
#<ServerQuitFromTimeUp timeLimitMs="1000"/>
missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ModSettings>
                  <MsPerTick>100</MsPerTick>
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
                    <DrawCuboid x1="-11" y1="226" z1="-6" x2="0" y2="246" z2="5" type="stone"/>
                    <DrawCuboid x1="-10" y1="227" z1="-5" x2="-1" y2="246" z2="4" type="air"/>
                    <DrawCuboid x1="-2" y1="227" z1="-4" x2="-2" y2="'''+str(height)+'''" z2="-2" type="stone"/>
                    <DrawCuboid x1="-2" y1="227" z1="0" x2="-2" y2="'''+str(height)+'''" z2="3" type="stone"/>
                    <DrawCuboid x1="-9" y1="227" z1="3" x2="-8" y2="'''+str(height)+'''" z2="3" type="stone"/>
                    <DrawCuboid x1="-6" y1="227" z1="3" x2="-4" y2="'''+str(height)+'''" z2="3" type="stone"/>
                    <DrawCuboid x1="-4" y1="227" z1="-2" x2="-4" y2="'''+str(height)+'''" z2="-4" type="stone"/>
                    <DrawCuboid x1="-4" y1="227" z1="0" x2="-4" y2="'''+str(height)+'''" z2="1" type="stone"/>
                    <DrawCuboid x1="-8" y1="227" z1="1" x2="-6" y2="'''+str(height)+'''" z2="1" type="stone"/>
                    <DrawCuboid x1="-9" y1="227" z1="-1" x2="-7" y2="'''+str(height)+'''" z2="-1" type="stone"/>
                    <DrawCuboid x1="-7" y1="227" z1="-2" x2="-7" y2="'''+str(height)+'''" z2="-2" type="stone"/>
                    <DrawCuboid x1="-9" y1="227" z1="-3" x2="-9" y2="'''+str(height)+'''" z2="-3" type="stone"/>
                    <DrawCuboid x1="-9" y1="227" z1="-4" x2="-6" y2="'''+str(height)+'''" z2="-4" type="stone"/>
                    <DrawEntity x="-3" y="227" z="-4.5" type="Zombie"/>
                    <DrawEntity x="-0.5" y="227" z="4" type="Zombie"/>
                    <DrawEntity x="-9.5" y="227" z="4" type="Zombie"/>
                  </DrawingDecorator>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                  <Name>Survivor</Name>
                  <AgentStart>
                      <Placement x="-4.5" y="227.0" z="-0.5" yaw="0"/>
                      <Inventory>
                      </Inventory>
                  </AgentStart>
                  <AgentHandlers>
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
    rewards, episodes, commands = [], [], []
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
        
        # Run episode
        print "Episode " + str(iRepeat) + ":",
        total_reward, total_commands = Survivor.run( agent_host )
        rewards.append( total_reward )
        commands.append( total_commands )
        episodes.append( iRepeat )
        print "Alive for " + str(total_commands) + " commands"
        # Episode has ended.
        
       
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
    plt.ylabel( "Commands Alive" )
    plt.title( "Maze - Q-Approximation No Stationary Basis - 100 Episodes" )
    #plt.show()
    plt.savefig("/Users/edisonweik/Desktop/cs175/maze_q_no_stationary_100.pdf")
    
    
    
    