import time
import requests
import urllib3
import json
from pprint import pprint
class IxNetRestApiException(Exception): pass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ixiaApiServer = "127.0.0.1"
ixiaApiPort = '11009'
ixiaChassis = "10.27.192.3"
ixiaApiAuth = {"username": "admin",
             "password": "admin"}

#root = f"https://{ixiaApiServer}:{ixiaApiPort}"

class IxAPI():
    
    def __init__(self, ixiaApiServer, ixiaApiPort):
        self.ipserver = ixiaApiServer
        self.ipport = ixiaApiPort
        self.root = f"https://{ixiaApiServer}:{ixiaApiPort}"
            
    def __waitForComplete__(self, response='', url='',  silentMode=True, timeout=90):
        """
        Description
            Wait for an operation progress to complete.
        
        Parameters
            response: The POST action response.  Generally, after an /operations action.
                      Such as /operations/startallprotocols, /operations/assignports
            silentMode: True or False. If True, display info messages.
            timeout: The time allowed to wait for success completion in seconds.
        """
        print ('\nwaitForComplete...')
        if response.json() == []:
            raise IxNetRestApiException('waitForComplete: response is empty.')
        if 'errors' in response.json():
            print(response.json()["errors"][0])
            return 1
        print("\tState:",response.json()["state"])
        if response.json()['state'] == "SUCCESS":
            return 0
        if response.json()['state'] == "ERROR":
            print("Error")
            return 1
        if response.json()['state'] == "EXCEPTION":
            print(response.text)
            return 1

        while True:
            if response.json()["state"] == "IN_PROGRESS" or response.json()["state"] == "down":
                if timeout == 0:
                    return 1
                time.sleep(1)
                response = requests.get(url, 
                                        headers={'content-type': 'application/json'},
                                        verify=False)
                print("TestResponse\n"+str(response))
                state = response.json()["state"]
                if timeout > 0 and state == 'SUCCESS':
                    print("\tState: {0}".format(state))
                    break
                elif timeout > 0 and state == 'ERROR':
                    print("Error")
                    return 1
                elif timeout > 0 and state == 'EXCEPTION':
                    print(response.text)
                    return 1
                elif timeout == 0 and state != 'SUCCESS':
                    return 1
                else:
                    print("\tState: {0} {1} seconds remaining".format(state, timeout))
                    timeout = timeout-1
                    continue
            
    def conn_srvr(self):
        try:
            self.response = requests.post(self.root+"/api/v1/sessions",
                         headers={'content-type': 'application/json'}, verify=False)
            if self.response.status_code == 201:
                print(f'Connection to IXAPI server {self.ipserver} is successfull')
        except Exception as error:
            print(error)
            
    def close_conn(self):
        try:
            requests.delete(self.root, 
                            headers={'content-type': 'application/json'}, verify=False)
            print(f'Connection to IXAPI server {self.ipserver} was closed')
        except Exception as error:
            print(error)

    def verif_sessions(self):
        try:
            response = requests.get(self.root+"/api/v1/sessions/1",
                                 headers={'content-type': 'application/json'}, verify=False)
            print(response.json()['state'])
            return response.status_code
        except Exception as error:
            print(error)   

    def new_conf(self):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/operations/newconfig",
                         headers={'content-type': 'application/json'}, verify=False)
            return response.status_code
        except Exception as error:
            print(error)  
            
    def load_conf(self, file):
        try:
            response = requests.post(self.root+f"/api/v1/sessions/1/ixnetwork/operations/loadconfig",
                                     data=json.dumps({'arg1': file}),
                         headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error) 
            
    def list_files(self):
        try:
            response = requests.get(self.root+"/api/v1/sessions/1/ixnetwork/files",
                         headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error)  

    def ver_file(self, file):
        try:
            response = requests.get(self.root+f"/api/v1/sessions/1/ixnetwork/files/{file}",
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.status_code
        except Exception as error:
            print(error)  
            
    def get_vport(self):
        vportList = []
        portList = []
        try:
            response = requests.get(self.root+"/api/v1/sessions/1/ixnetwork/vport",
                         headers={'content-type': 'application/json'}, verify=False)
            for l1 in response.json():
                vportList.append(self.root+"/api/v1/sessions/1/ixnetwork/vport/" + str(l1['id']))
                portList.append({'arg1': l1['assignedTo'].split(':')[0],
                               'arg2': l1['assignedTo'].split(':')[1],
                               'arg3': l1['assignedTo'].split(':')[2]})
        except Exception as error:
            print(error)
        return vportList, portList

    def assign_port(self, vportList, portList):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/operations/assignports",
                                     data=json.dumps({"arg1": portList,
                                                     "arg2": [],
                                                     "arg3": vportList,
                                                     "arg4": True}),
                                     headers={'content-type': 'application/json'}, verify=False)
#            self.__waitForComplete__(response=response,
#                                     url=self.root+"/api/v1/sessions/1/ixnetwork/operations/assignports",
#                                     timeout=90)
            return response.json()
        except Exception as error:
            print(error) 
            
    def load_topo(self, file):
        try:
            response = requests.post(self.root+f"/api/v1/sessions/1/ixnetwork/operations/import",
                                     data=json.dumps({'arg1': file}),
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error)  
            
    def start_proto(self):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/operations/startallprotocols",
                                     headers={'content-type': 'application/json'}, verify=False)
#            self.__waitForComplete__(response,
#                                     url=self.root+"/api/v1/sessions/1/ixnetwork/operations/startallprotocols",
#                                     timeout=90)
            return response.json()
        except Exception as error:
            print(error) 
            
    def stop_proto(self):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/operations/stopallprotocols",
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error) 
            
    def apply_traffic(self):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/traffic/operations/apply",
                                     data=json.dumps({"arg1": self.root+"/api/v1/sessions/1/ixnetwork/traffic"}),
                                     headers={'content-type': 'application/json'}, verify=False)
#            self.__waitForComplete__(response,
#                                     url=self.root+"/api/v1/sessions/1/ixnetwork/traffic/operations/apply",
#                                     timeout=90)
            return response.json()
        except Exception as error:
            print(error) 
            
    def start_traffic(self):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/traffic/operations/start",
                                     data=json.dumps({"arg1": self.root+"/api/v1/sessions/1/ixnetwork/traffic"}),
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error) 
            
    def stop_traffic(self):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/traffic/operations/stop",
                                     data=json.dumps({"arg1": self.root+"/api/v1/sessions/1/ixnetwork/traffic"}),
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error) 
            
    def get_stats(self, Id):
        try:
            response = requests.get(self.root+f"/api/v1/sessions/1/ixnetwork/statistics/view/{Id}/data",
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error)     

#Argument for method can be allTraffic, controlTraffic, dataTraffic
    def start_capt(self, vport, method):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/vport/capture/operations/start",
                                     data=json.dumps({"arg1": f"/api/v1/sessions/1/ixnetwork/vport/{vport}/capture",
                                                    "arg2": method}),
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error) 
            
#Argument for method can be allTraffic, controlTraffic, dataTraffic
    def stop_capt(self, vport, method):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/vport/capture/operations/stop",
                                     data=json.dumps({"arg1": f"/api/v1/sessions/1/ixnetwork/vport/{vport}/capture",
                                                    "arg2": method}),
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error) 
            
    def save_capt(self, folder):
        try:
            response = requests.post(self.root+"/api/v1/sessions/1/ixnetwork/operations/savecapture",
                                     data=json.dumps({"arg1": folder}),
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error) 
            
    def api_options(self):
        try:
            response = requests.options(self.root+"/api/v1/sessions/1/ixnetwork",
                                     headers={'content-type': 'application/json'}, verify=False)
            return response.json()
        except Exception as error:
            print(error)
