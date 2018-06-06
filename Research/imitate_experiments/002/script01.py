from __future__ import print_function
from builtins import range
import MalmoPython

import time
import malmoutils


# -- set up two agent hosts --
agent_host1 = MalmoPython.AgentHost()
agent_host2 = MalmoPython.AgentHost()

# Use agent_host1 for parsing the command-line options.
# (This is why agent_host1 is passed in to all the subsequent malmoutils calls, even for
# agent 2's setup.)
malmoutils.parse_command_line(agent_host1)

frame_width = 320
frame_height = 320

xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <About>
    <Summary/>
  </About>
  <ServerSection>
    <ServerInitialConditions>
      <Time>
        <StartTime>0</StartTime>
      </Time>
    </ServerInitialConditions>
    <ServerHandlers>
      <FlatWorldGenerator forceReset="true" generatorString="3;7,2*3,2;1;village" seed=""/>
      <ServerQuitFromTimeUp description="" timeLimitMs="10000"/>
      <ServerQuitWhenAnyAgentFinishes description=""/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>Ant</Name>
    <AgentStart>
      <Placement x="-1.5" y="5.0" z="0.5" pitch="30" yaw="0"/>
    </AgentStart>
    <AgentHandlers>
      <DiscreteMovementCommands/>
      <RewardForCollectingItem>
        <Item reward="1" type="dirt"/>
      </RewardForCollectingItem>
      <RewardForDiscardingItem>
        <Item reward="10" type="dirt"/>
      </RewardForDiscardingItem>
      <VideoProducer>
          <Width>''' + str(frame_width) + '''</Width>
          <Height>''' + str(frame_height) + '''</Height>
      </VideoProducer>
    </AgentHandlers>
  </AgentSection>

  <AgentSection mode="Survival">
    <Name>Bee</Name>
    <AgentStart>
      <Placement x="1.5" y="5.0" z="6.5" pitch="30" yaw="180"/>
    </AgentStart>
    <AgentHandlers>
      <DiscreteMovementCommands/>
      <RewardForCollectingItem>
        <Item reward="10" type="dirt"/>
      </RewardForCollectingItem>
      <RewardForDiscardingItem>
        <Item reward="100" type="dirt"/>
      </RewardForDiscardingItem>
      <VideoProducer>
          <Width>''' + str(frame_width) + '''</Width>
          <Height>''' + str(frame_height) + '''</Height>
      </VideoProducer>
    </AgentHandlers>
  </AgentSection>
  
</Mission>'''
my_mission = MalmoPython.MissionSpec(xml,True)

client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )

MalmoPython.setLogging("", MalmoPython.LoggingSeverityLevel.LOG_OFF)

def safeStartMission(agent_host, mission, client_pool, recording, role, experimentId):
    used_attempts = 0
    max_attempts = 5
    print("Calling startMission for role", role)
    while True:
        try:
            agent_host.startMission(mission, client_pool, recording, role, experimentId)
            break
        except MalmoPython.MissionException as e:
            errorCode = e.details.errorCode
            if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                print("Server not quite ready yet - waiting...")
                time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                print("Not enough available Minecraft instances running.")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                print("Server not found - has the mission with role 0 been started yet?")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            else:
                print("Other error:", e.message)
                print("Waiting will not help here - bailing immediately.")
                exit(1)
        if used_attempts == max_attempts:
            print("All chances used up - bailing now.")
            exit(1)
    print("startMission called okay.")

def safeWaitForStart(agent_hosts):
    print("Waiting for the mission to start", end=' ')
    start_flags = [False for a in agent_hosts]
    start_time = time.time()
    time_out = 120  # Allow two minutes for mission to start.
    while not all(start_flags) and time.time() - start_time < time_out:
        states = [a.peekWorldState() for a in agent_hosts]
        start_flags = [w.has_mission_begun for w in states]
        errors = [e for w in states for e in w.errors]
        if len(errors) > 0:
            print("Errors waiting for mission start:")
            for e in errors:
                print(e.text)
            print("Bailing now.")
            exit(1)
        time.sleep(0.1)
        print(".", end=' ')
    print()
    if time.time() - start_time >= time_out:
        print("Timed out waiting for mission to begin. Bailing.")
        exit(1)
    print("Mission has started.")

safeStartMission(agent_host1, my_mission, client_pool, malmoutils.get_default_recording_object(agent_host1, "agent_1_viewpoint_discrete"), 0, '' )
safeStartMission(agent_host2, my_mission, client_pool, malmoutils.get_default_recording_object(agent_host1, "agent_2_viewpoint_discrete"), 1, '' )
safeWaitForStart([agent_host1, agent_host2])

# perform a few actions
time.sleep(1)
agent_host1.sendCommand('attack 1')
agent_host2.sendCommand('attack 1')
time.sleep(2)
agent_host1.sendCommand('attack 0')
agent_host2.sendCommand('attack 0')
agent_host1.sendCommand('move 1')
agent_host2.sendCommand('move 1')
time.sleep(1)
agent_host1.sendCommand('move 0')
agent_host2.sendCommand('move 0')
agent_host1.sendCommand('use 1')
agent_host2.sendCommand('use 1')
time.sleep(1)
agent_host1.sendCommand('use 0')
agent_host2.sendCommand('use 0')
    
# wait for the missions to end    
while agent_host1.peekWorldState().is_mission_running or agent_host2.peekWorldState().is_mission_running:
    time.sleep(1)
