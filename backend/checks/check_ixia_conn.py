
import IxNetwork

ixNet = IxNetwork.IxNet()

host = '10.27.192.176'
ixNet = IxNetwork.IxNet()

# authenticate to the server and get an api key to be used for subsequent
apiKey = ixNet.getApiKey(host, 'admin', 'admin', './api.key')

# # create a new session
ixNet.connect(host, '-version', '9.12', '-apiKey', apiKey)

# # connect to an existing session
# ixNet.connect(host, '-version', '9.12', '-apiKey', apiKey, '-sessionId', 59)

# get information about the currently connected session
print(ixNet.getSessionInfo())

file = "../cfgs_ixia/test_conn_ixia.ixncfg"
temp = ixNet.readFrom(file)
print("*",temp)
temp = ixNet.execute('loadConfig', temp)
print("**",temp)
