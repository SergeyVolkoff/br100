from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)

import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
import yaml
from constants_br100.constants import (
    CONSOLE,
)
# Constants

INVALID_INPUT = "Invalid input detected"

class ConnectStorage():
    """Class represents connect and disconnect actions for Node."""

    def __init__(self, log=True):
        """Init Connect-class."""
        
        try:
            with open("constants_connect.yaml") as f2:
                self.VALUE_CONS_CONNECT = yaml.safe_load(f2)
                print(self.VALUE_CONS_CONNECT)
            self.ssh = ConnectHandler(**self.VALUE_CONS_CONNECT)
        except ConnectionRefusedError:
            CONSOLE.print(
                    "*" * 5, "Error connection to :",
                    self.VALUE_CONS_CONNECT['host'],
                    'port:', self.VALUE_CONS_CONNECT['port'], "*" * 5,
                    "\nConnection refused - Console is busy!",
                    style='fail')
            exit()
    def check_connection(self, log=True):
        """Check connection to Server."""
        if log:
            CONSOLE.print(
                'Пробую подключиться к', self.VALUE_CONS_CONNECT['host'],
                'порт:', self.VALUE_CONS_CONNECT['port'], "...",
                style="info")
        try:
            CONSOLE.print('Коммутатор',
                self.VALUE_CONS_CONNECT['host'], 'порт:',
                self.VALUE_CONS_CONNECT['port'], "подключен!",
                style='success')
        except (NetmikoAuthenticationException,
                NetmikoTimeoutException):
            CONSOLE.print(
                "*" * 5, "Ошибка подключения к:",
                self.VALUE_CONS_CONNECT['host'],
                'порт:', self.VALUE_CONS_CONNECT['port'], "*" * 5,
                style='fail')
            
if __name__=="__main__":
    str = ConnectStorage()
    print(str.check_connection())