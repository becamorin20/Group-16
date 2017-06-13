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
import copy
import math
from collections import namedtuple

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately


EntityList = []
EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, variation, quantity')
EntityInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "", "", "", 1)
action_trans = {-21: 'movenorth 10', 21: 'movesouth 1', -1: 'movewest 1', 1: 'moveeast 1'}
better_trans = {"north": 'movenorth 1', "south": 'movesouth 1', "west": 'movewest 1', "east": 'moveeast 1'}

Walls = []

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
                    <DrawEntity x="9" y="207" z="9" type="Zombie"/>
                  </DrawingDecorator>
                  
                  <ServerQuitFromTimeUp timeLimitMs="60000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>Bill Buttlicker</Name>
                <AgentStart>
                    <Placement x="5" y="207.0" z="5" yaw="0" pitch ="30" />
                </AgentStart>
                <AgentHandlers>
                <DiscreteMovementCommands/>
                <ContinuousMovementCommands turnSpeedDegs="360"/>
                <AbsoluteMovementCommands/>

                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(40)+'''" yrange="2" zrange="'''+str(40)+'''" />
                </ObservationFromNearbyEntities>
                <ObservationFromFullStats/>

                <ObservationFromGrid>
                      <Grid name="floor3x3">
                        <min x="-10" y="0" z="-10"/>
                        <max x="10" y="0" z="10"/>
                        </Grid>
                      <Grid name="floorAll">
                        <min x="-10" y="-1" z="-10"/>
                        <max x="10" y="-1" z="10"/>
                      </Grid>

                  </ObservationFromGrid>
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



def myeval(zombie,player):
    """Evaluates based on the number of turns survived"""
    distance = math.sqrt( (zombie.x - player.x)*(zombie.x-player.x) + (zombie.z - player.z)*(zombie.z-player.z) ) 
    return distance
def isGameEnd(player, zombies):
    """Returns true if a zombie collides with a player"""
    for zombie in zombies:
        distance = math.sqrt( (zombie.x - player.x)*(zombie.x-player.x) + (zombie.z - player.z)*(zombie.z-player.z) ) 
        if(distance <1): return True
    return False
def getPlayer():
    """Returns the player entity"""
    for ent in EntityList:
        if ent.name == "Zombie":
            continue
        else:
            return ent
def getZombies():
    """Returns a list of the current indexes of all zombies"""
    zombies = []
    for ent in EntityList:
        if ent.name == "Zombie":
            zombies.append(ent)
        else:
            continue
    return zombies
def legalMove(space):
    return Walls[int(space[0]*21) + int(space[1])] !="stone" # observeGrid(50,50,50,50,50,50).y2 >#pass#if(space[0]>=-1 and ):
def flatten(move):
    return (move[0]*21) + move[1]
def getAvailableMoves(entity):
    """Returns all available moves by checking each direction"""
    returnArr = []
    if(legalMove((entity.x+1,entity.z))): returnArr.append((int(entity.x+1),int(entity.z),"east" ))
    if(legalMove((entity.x,entity.z+1))): returnArr.append((int(entity.x),int(entity.z+1),"north"))
    if(legalMove((entity.x-1,entity.z))): returnArr.append((int(entity.x-1),int(entity.z),"west"))
    if(legalMove((entity.x,entity.z-1))): returnArr.append((int(entity.x),int(entity.z-1),"south"))
    return returnArr#pass
def translateMoves(curBlock, nextBlock):
    """Translates the move from the flat list to a malmo usable action"""
    return action_trans[int(nextBlock - curBlock)]

def maxPlay(grid,depth,zombies,player):
    if( isGameEnd(player,zombies) or depth >3):
        if(len(zombies) ==0): return float('inf'), []
        elif(len(zombies) ==1): return myeval(zombies[0],player), []
        else: return myeval(zombies[0],player) + myeval(zombies[1],player),[]
    moves = getAvailableMoves(player)
    moveSequence = []
    maxbest = float('-inf')
    for move in moves:
        player = player._replace(x =move[0],z = move[1])
        score,sequence = minPlay(grid, depth+1,zombies,player)
        if(score>maxbest):
            moveSequence = [move]
            moveSequence += sequence
            maxbest = score
    return maxbest, moveSequence
def minPlay(grid,depth,zombies,player):
    if( isGameEnd(player,zombies) or depth >3):
        if(len(zombies) ==0): return 0,[]
        elif(len(zombies) ==1): return myeval(zombies[0],player),[]
        else: return myeval(zombies[0],player) + myeval(zombies[1],player), []
    minbest = float('inf')
    moveSequence = []
    if(len(zombies)>0):moves1 = getAvailableMoves(zombies[0])
    if(len(zombies)>1):
        moves2 = getAvailableMoves(zombies[1])
        for move in moves1:
            zombies[0] =zombies[0]._replace(x =move[0],z = move[1])
            for move2 in moves2:
                zombies[1] = zombies[1]._replace(x =move2[0],z = move2[1])
                score,sequence = maxPlay(grid,depth+1,zombies,player)
                if(float(score)<minbest):
                    minbest = score 
                    moveSequence = [move]
                    moveSequence += sequence
    elif (len(zombies) ==1):
        if (len(moves1) <=0):return myeval(zombies[0],player), []
        for move in moves1:
            zombies[0] =zombies[0]._replace(x =move[0],z = move[1])
            score,sequence = maxPlay(grid,depth+1,zombies,player)
            if(score<minbest):
                moveSequence = [move]
                moveSequence += sequence
                minbest = score
    return minbest,moveSequence
    #for move in moves:
        
def miniMax(grid_orbs):
    """Simple deterministic policy for evading zombies"""
    
    player = copy.deepcopy(getPlayer())
    moves = getAvailableMoves(player)

    zombies = getZombies()[:]
    best = float('-inf')
    mySequence = []
    if (len(moves) ==0):
        return
    bestMove = moves[0]
    for move in moves:
        player = player._replace(x =move[0],z = move[1])
        newScore,sequence = minPlay(grid,1,zombies,player)
        if(newScore > best):
            bestMove = move
            mySequence = [move]
            mySequence +=sequence
            best = newScore
    return bestMove, mySequence



# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
agent_host.addOptionalIntArgument( "speed,s", "Length of tick, in ms.", 5)

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
builtTheWall = False
while world_state.is_mission_running:
    #sys.stdout.write(".")
    time.sleep(.15)
    if world_state.number_of_observations_since_last_state > 0:
        for error in world_state.errors:
            print "Error:",error.text
        msg = world_state.observations[-1].text
        ob = json.loads(msg)
        if(not builtTheWall):
            Walls = ob.get(u'floor3x3', 0)
            builtTheWall = True
        if "entities" in ob:
            EntityList = [EntityInfo(**k) for k in ob["entities"]]
            #print EntityList
            try:
                bestMove,sequence = miniMax(EntityList)
                print sequence
                agent_host.sendCommand(better_trans[bestMove[2]])
            except Exception as e:
                print e
        #agent_host.sendCommand((translateMoves(flatten((getPlayer().x,getPlayer().z)),flatten(bestMove))))
    world_state = agent_host.getWorldState()

print
print "Mission ended"

# Mission has ended.
