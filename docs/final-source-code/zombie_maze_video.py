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
#from q_approximation_rbf import *
#from q_approximation_tile import *
#from q_approximation_tile2 import *
#from q_approximation_tile3 import *
#from q_approximation_tile_wall import *
#from q_approximation_coarse import *
#from q_approximation_coarse2 import *
from q_approximation_coarse3 import *
#from q_approximation_coarse_wall import *
#from q_approximation_no_stationary_basis import *
#from q_approximation_no_stationary_basis2 import *
#from q_approximation_no_stationary_basis_wall import *
import matplotlib.pyplot as plt


height = 229
#<ServerQuitFromTimeUp timeLimitMs="1000"/>
missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ModSettings>
                  <MsPerTick>75</MsPerTick>
              </ModSettings>
              
              <ServerSection>
                <ServerInitialConditions>
                  <Time>
                    <StartTime>16000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                  </Time>
                  <Weather>clear</Weather>
                  <AllowSpawning>true</AllowSpawning>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
                  <DrawingDecorator>
                    <DrawCuboid x1="-11" y1="226" z1="-6" x2="0" y2="246" z2="5" type="beacon"/>
                    <DrawCuboid x1="-10" y1="227" z1="-5" x2="-1" y2="246" z2="4" type="air"/>
                    <DrawCuboid x1="-10" y1="235" z1="-5" x2="-1" y2="235" z2="4" type="stained_glass" colour="WHITE"/>
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
                      <MissionQuitCommands quitDescription="give_up"/>
                  </AgentHandlers>
              </AgentSection>
              
              <AgentSection mode="Creative">
                  <Name>TheWatcher</Name>
                  <AgentStart>
                    <Placement x="-4.5" y="236" z="-0.5" pitch="90"/>
                  </AgentStart>
                  <AgentHandlers>
                    <ContinuousMovementCommands turnSpeedDegs="360"/>
                    <MissionQuitCommands quitDescription="give_up"/>
                  </AgentHandlers>
            </AgentSection>
              
            </Mission>'''

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
    my_client_pool = MalmoPython.ClientPool()
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10001))

    # Create default Malmo objects:
    agent_hosts = [MalmoPython.AgentHost(), MalmoPython.AgentHost()]
    try:
        agent_hosts[0].parse( sys.argv )
    except RuntimeError as e:
        print 'ERROR:',e
        print agent_hosts[0].getUsage()
        exit(1)
    if agent_hosts[0].receivedArgument("help"):
        print agent_hosts[0].getUsage()
        exit(0)
    
    # initialize parameter vector and basis functions
    Survivor = Agent()
    times, episodes, commands = [], [], []
    for iRepeat in range(100):
        my_mission = MalmoPython.MissionSpec(missionXML, True)
        my_mission_record = MalmoPython.MissionRecordSpec()

        # Attempt to start a mission:
        for i in range(2):
            for retry in range(3):
                try:
                    agent_hosts[i].startMission( my_mission, my_client_pool,  my_mission_record, i, "Survivor" )
                    break
                except RuntimeError as e:
                    if retry == 2:
                        print "Error starting mission:",e
                        exit(1)
                    else:
                        time.sleep(8)

        # Loop until mission starts:
        world_state = agent_hosts[0].getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_hosts[0].getWorldState()

        # Run episode
        start_time = time.time()
        print "Episode " + str(iRepeat) + ":",
        Survivor.load_parameters("/Users/edisonweik/Desktop/cs175/parameters/q25coarse_4.txt")
        Survivor.episodes = 90
        _, c = Survivor.run( agent_hosts[0] )
        time_alive = time.time() - start_time
        times.append( time_alive )
        commands.append( c )
        episodes.append( iRepeat )
        print "Alive for " + str(c) + " commands and " + str(time_alive) + "seconds"
        # Episode has ended.

        agent_hosts[0].sendCommand( "quit" ) 
        agent_hosts[1].sendCommand( "quit" ) 
        time.sleep(1)
            
    
    
    