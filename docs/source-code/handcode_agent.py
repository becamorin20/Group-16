#
#
# Zombie-Maze-Land
# CS 175
# Edison Weik
#
# handcode_agent.py
#
# Implements Minecraft environment with the maze and zombies.
# Implements handcoded algorithm used in mob_fun.py example from MalmoPlatform/Python_Examples directory.
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
import math
import matplotlib.pyplot as plt


height = 229
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
                    <DrawEntity x="-0.25" y="227" z="4" type="Zombie"/>
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
                      <ContinuousMovementCommands turnSpeedDegs="360"/>
                      <AbsoluteMovementCommands/>
                      <ObservationFromNearbyEntities>
                          <Range name="zombies" xrange="10" yrange="2" zrange="10" />
                      </ObservationFromNearbyEntities>
                      <RewardForMissionEnd rewardForDeath="-1000">
                          <Reward description="out_of_time" reward="0"/>
                      </RewardForMissionEnd>
                  </AgentHandlers>
              </AgentSection>
            </Mission>'''

def getBestAngle(agent, z1, z2, z3, current_yaw):
    '''Scan through 360 degrees, looking for the best direction in which to take the next step.'''
    scores=[]
    # Normalise current yaw:
    while current_yaw < 0:
        current_yaw += 360
    while current_yaw > 360:
        current_yaw -= 360
        
    # Look for best option
    ARENA_WIDTH = 10
    ARENA_BREADTH = 10
    agent_stepsize = 1
    agent_search_resolution = 30
    agent_edge_weight = -100
    agent_turn_weight = 0
    for i in xrange(agent_search_resolution):
        # Calculate cost of turning:
        ang = 2 * math.pi * (i / float(agent_search_resolution))
        yaw = i * 360.0 / float(agent_search_resolution)
        yawdist = min(abs(yaw-current_yaw), 360-abs(yaw-current_yaw))
        turncost = agent_turn_weight * yawdist
        score = turncost
    
        # Calculate entity proximity cost for new (x,z):
        x = agent[0] + agent_stepsize - math.sin(ang)
        z = agent[0] + agent_stepsize * math.cos(ang)
        for i in [z1, z2, z3]:
            dist = (i[0] - x)*(i[0] - x) + (i[1] - z)*(i[1] - z)
            if (dist == 0):
                continue
            weight = -10
            dist -= 1
            if dist <= 0:
                dist = 0.1
            score += weight / float(dist)
        
        # Calculate cost of proximity to edges:
        distRight = (2+ARENA_WIDTH/2) - x
        distLeft = (-2-ARENA_WIDTH/2) - x
        distTop = (2+ARENA_BREADTH/2) - z
        distBottom = (-2-ARENA_BREADTH/2) - z
        score += agent_edge_weight / float(distRight * distRight * distRight * distRight)
        score += agent_edge_weight / float(distLeft * distLeft * distLeft * distLeft)
        score += agent_edge_weight / float(distTop * distTop * distTop * distTop)
        score += agent_edge_weight / float(distBottom * distBottom * distBottom * distBottom)
        scores.append(score)
    
    # Find best score:
    i = scores.index(max(scores))
    # Return as an angle in degrees:
    return i * 360.0 / float(agent_search_resolution)
    
    
    
class Agent(object):
    def __init__(self):
        """Constructing an RL agent.
        """
        self.episodes = 0

                
    def get_action(self):
        '''
        Output: action chosen by using mob fun algorithm.
        '''
        best_yaw = getBestAngle(self.agent, self.z1, self.z2, self.z3, self.yaw)
        difference = best_yaw - self.yaw;
        while difference < -180:
            difference += 360;
        while difference > 180:
            difference -= 360;
        difference /= 180.0;
        #print difference
        return "turn " + str(difference)

    
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
        Return 4 2-tuples of current positions of entities.
        '''
        world_state = agent_host.getWorldState()
        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                observations = json.loads(msg)
                self.check_health( observations[u'Life'], agent_host )
                if "Yaw" in observations:
                    self.yaw = observations[u'Yaw']
                state = observations.get(u'zombies', 0)
                break
        agent = ( state[0][u'x'], state[0][u'z'] )
        z1 = ( state[1][u'x'], state[1][u'z'] )
        z2 = ( state[2][u'x'], state[2][u'z'] )
        z3 = ( state[3][u'x'], state[3][u'z'] )
        return agent, z1, z2, z3


    def act(self, agent_host, current_r):
        '''
        Observe state, get action, and act.
        '''
        # Observe current state
        try:
            self.agent, self.z1, self.z2, self.z3 = self.observe_state( agent_host ) 
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
        agent_host.sendCommand("move 1")
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
                    #print "Action: ", self.action, ", reward: ", self.reward
                    total_commands += 1
                    break
                if not world_state.is_mission_running or not self.alive:
                    break
                        
        # Process final reward and return results
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
    
    
    current_yaw = 0
    best_yaw = 0
    
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
        
        # Run Mission
        print "Episode " + str(iRepeat) + ":",
        
        # Run episode
        total_reward, total_commands = Survivor.run( agent_host )
        rewards.append( total_reward )
        commands.append( total_commands )
        episodes.append( iRepeat )
        # Episode has ended.
        
        print "Alive for " + str(total_commands) + " commands"
        while world_state.is_mission_running:
            world_state = agent_host.getWorldState()
            pass
        time.sleep(1)
    
    
    # Plot results from learner
    #commands = [ i**2 for i in range(100) ]
    #episodes = [ i for i in range(100) ]
    m, b = np.polyfit(episodes, commands, 1)
    line_fit = [ float(m)*x + float(b) for x in episodes ]
    plt.scatter( episodes, commands, s=1, c='black' )
    plt.plot(episodes, line_fit, '-')
    plt.xlabel( "Episodes" )
    plt.ylabel( "Commands Alive" )
    plt.title( "Maze - Handcode - 100 Episodes" )
    #plt.show()
    plt.savefig("/Users/edisonweik/Desktop/cs175/maze_handcode_100.pdf")


