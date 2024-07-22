"""Base class for switches BR100."""

import re
import time
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../'))
# sys.path.append(os.getcwd())
print("***",sys.path)
import yaml
from constants_engine_cfg.constants_br100  import (
    CONSOLE,
    NAME_DEV,
)

from ping3 import ping

class Connect():
    """Class represents connect and disconnect actions for Node."""

    def __init__(self, log=True):
        """Init Connect-class."""
        self.word_ping = "ping ",
        self.ip_inet = "8.8.8.8",
        try:
            with open("file_for_back/constants_trident1.yaml") as f2:
                self.VALUE_CONS_CONNECT = yaml.safe_load(f2)
            self.ssh = ConnectHandler(**self.VALUE_CONS_CONNECT)
        except ConnectionRefusedError:
            CONSOLE.print(
                    "*" * 5, "Error connection to:",
                    self.VALUE_CONS_CONNECT['host'],
                    'port:', self.VALUE_CONS_CONNECT['port'], "*" * 5,
                    "\nConnection refused - Console is busy!",
                    style='fail')
            exit()
    def check_mode(self):
        check_mode_conn = self.ssh.check_config_mode()
        try:
            if check_mode_conn == True:
                self.ssh.exit_config_mode()
        except ConnectionError as err:
            CONSOLE.print(
                    "*" * 5, "Error connection to:",
                    self.VALUE_CONS_CONNECT['host'],
                    'port:', self.VALUE_CONS_CONNECT['port'], "*" * 5,
                    err,
                    style='fail')
            exit()

    def sh_ver(self):
        ""
        self.check_connection(self.VALUE_CONS_CONNECT)
        self.ssh.enable()
        try:
            temp = self.ssh.send_command('show version',read_timeout=2)
            for i in temp:
                print(i)
                with open("file_for_back/process_temp.txt", 'a+') as file:
                     file.write(i)

        except FileNotFoundError:
            print('Файл отсутствует.')
        except ValueError as v_e:
            print(v_e)

if __name__=="__main__":
    tr1 = Connect()
    print(tr1.check_mode())