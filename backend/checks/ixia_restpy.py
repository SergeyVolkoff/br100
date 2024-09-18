from ixnetwork_restpy import SessionAssistant


session_assistant = SessionAssistant(
    IpAddress="10.27.192.176",
    UserName="admin",
    Password="admin",
    LogLevel=SessionAssistant.LOGLEVEL_INFO,
    ClearConfig=True,
)
ixnetwork = session_assistant.Ixnetwork