# import IxNetwork
from ixnetwork_restpy import SessionAssistant, Files

chassis_ip = "10.27.192.176"
session_assistant = SessionAssistant(
    IpAddress=chassis_ip,
    UserName="admin",
    Password="admin",
    LogLevel=SessionAssistant.LOGLEVEL_INFO,
    ClearConfig=True,
)
ixnetwork = session_assistant.Ixnetwork

