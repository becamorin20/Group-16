# Sample Code for 10x10 Maze with 2 Zombies
#
# The mission in this code only lasts for 60 sec. But the zombies seem to die randomly without spawning after 15 sec. 
# I'm having trouble getting the zombies to live longer and for them to spawn. 
# Right now the walls of the maze are only 1 block tall - this is to allow me to edit and visualize the space easily from within the
# game. But obviously when we start the learning I would make the walls taller to prevent the zombies from easily jumping over them.
#
#
# the reason why the zombies were catching on fire and dieing after 60 seconds was because they can't survive in the daylight...
# so I made the time of the day be midnight



import MalmoPython
import os
import random
import sys
import time
import json
import errno

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

# More interesting generator string: "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"

#<FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>

# <DrawingDecorator>
#   <DrawCuboid x1="-6" y1="206" z1="-6"  x2="6" y2="226" z2="6" type="stone"/>
#   <DrawCuboid x1="-5" y1="207" z1="-5"  x2="5" y2="226" z2="5" type="air"/>
#   <DrawEntity x="0.5" y="207" z="0.5" type="Zombie"/>
#   <DrawEntity x="9" y="207" z="9" type="Zombie"/>
# </DrawingDecorator>


missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
              </About>
              <ModSettings>
             <MsPerTick> 40 </MsPerTick>
             </ModSettings>

              <ServerSection>
                <ServerInitialConditions>
                  <Time>
                    <StartTime>18000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                  </Time>
                  <Weather>clear</Weather>
                  <AllowSpawning>true</AllowSpawning>
                </ServerInitialConditions>

                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
                  <DrawingDecorator>
                    <DrawCuboid x1="-1" y1="206" z1="-1" x2="10" y2="226" z2="10" type="stone"/>
                    <DrawCuboid x1="0" y1="207" z1="0" x2="9" y2="226" z2="9" type="air"/>
                    <DrawCuboid x1="8" y1="207" z1="1" x2="8" y2="207" z2="3" type="stone"/>
                    <DrawCuboid x1="8" y1="207" z1="5" x2="8" y2="207" z2="8" type="stone"/>
                    <DrawCuboid x1="1" y1="207" z1="8" x2="6" y2="207" z2="8" type="stone"/>
                    <DrawCuboid x1="6" y1="207" z1="3" x2="6" y2="207" z2="6" type="stone"/>
                    <DrawCuboid x1="2" y1="207" z1="6" x2="4" y2="207" z2="6" type="stone"/>
                    <DrawCuboid x1="1" y1="207" z1="4" x2="4" y2="207" z2="4" type="stone"/>
                    <DrawCuboid x1="4" y1="207" z1="3" x2="4" y2="207" z2="3" type="stone"/>
                    <DrawCuboid x1="1" y1="207" z1="2" x2="1" y2="207" z2="2" type="stone"/>
                    <DrawCuboid x1="1" y1="207" z1="1" x2="5" y2="207" z2="1" type="stone"/>
                    <DrawEntity x="0.5" y="207" z="0.5" type="Zombie"/>
                    <DrawEntity x="9" y="207" z="9" type="Zombie"/>
                  </DrawingDecorator>
                  
                  <ServerQuitFromTimeUp timeLimitMs="60000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>Bill Buttlicker</Name>
                <AgentStart>
                    <Placement x="5" y="207.0" z="5" />
                </AgentStart>
                <AgentHandlers>
                    <ContinuousMovementCommands turnSpeedDegs="840">
                      <ModifierList type="deny-list"> <!-- Example deny-list: prevent agent from strafing -->
                          <command>strafe</command>
                      </ModifierList>
                  </ContinuousMovementCommands>
                  <ObservationFromFullStats/>
                  <DiscreteMovementCommands/>
                  <RewardForMissionEnd rewardForDeath="-1000">
                      <Reward description="out_of_time" reward="1000"/>
                  </RewardForMissionEnd>
                  <RewardForSendingCommand reward="1"/>
                </AgentHandlers>
              </AgentSection>

            </Mission>'''

def load_grid(world_state):
    """
    Used the agent observation API to get a 21 X 21 grid box around the agent (the agent is in the middle).

    Args
        world_state:    <object>    current agent world state

    Returns
        grid:   <list>  the world grid blocks represented as a list of blocks (see Tutorial.pdf)
    """
    while world_state.is_mission_running:
        # sys.stdout.write(".")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')

        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            observations = json.loads(msg)
            grid = observations.get(u'floorAll', 0)
            break
    return grid

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
agent_host.addOptionalIntArgument( "speed,s", "Length of tick, in ms.", 50)

try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print "Error starting mission:",e
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission running ",

grid = load_grid(world_state)

# Loop until mission ends:
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"

# Mission has ended.
