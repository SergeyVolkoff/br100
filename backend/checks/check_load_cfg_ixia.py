import json, sys, os, traceback

# Import the RestPy module
from ixnetwork_restpy import SessionAssistant, Files


debugMode = True
forceTakePortOwnership = True
chassis_ip = "10.27.192.176"

session_assistant = SessionAssistant(IpAddress=chassis_ip, RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='info', LogFilename='restpy.log')

ixNetwork = session_assistant.Ixnetwork

file = "../cfgs_ixia/test_conn_ixia.ixncfg"
print(ixNetwork.LoadConfig(Files(file)))

portMap = session_assistant.PortMapAssistant()
# portMap.Map(IpAddress=chassis_ip, CardId=2, PortId=5, Name="Port 5",Port=1)
portMap.Map(Port=("10.27.192.176",2,5),Name="Port 1")
portMap.Map(Port=("10.27.192.176",2,6),Name="Port 2")
# portMap.Map(IpAddress=chassis_ip, CardId=2, PortId=6, Name="Port 6",Port=2)
print(portMap.Connect(forceTakePortOwnership))

ixNetwork.info('Starting  protocols')
ixNetwork.StartAllProtocols(Arg1='sync')

ixNetwork.info('Verify protocol sessions')
protocolSummary = session_assistant.StatViewAssistant('Protocols Summary')
protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)

# Get the Traffic Item name for getting Traffic Item statistics.
trafficItem = ixNetwork.Traffic.TrafficItem.find()[0]

trafficItem.Generate()

ixNetwork.info('Applying traffic')
ixNetwork.Traffic.Apply()

ixNetwork.info('Starting traffic')
ixNetwork.Traffic.StartStatelessTrafficBlocking()
