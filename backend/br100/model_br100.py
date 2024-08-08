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
sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
# sys.path.append(os.getcwd())
# print("***",sys.path)
import yaml
from constants_br100.constants import (
    CONSOLE,
)

# Constants

INVALID_INPUT = "Invalid input detected"

from ping3 import ping

class ConnectBR():
    """Class represents connect and disconnect actions for Node."""

    def __init__(self, log=True):
        """Init Connect-class."""
        
        try:
            with open("../constants_br100/constants_connect.yaml") as f2:
                self.VALUE_CONS_CONNECT = yaml.safe_load(f2)
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
        """Check connection to DUT."""
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

    def disable_config_mode(self):
        "Check mode. if mode config return true - exit from config"
        # self.ssh.enable()
        # self.ssh.config_mode()
        check_mode_conn = self.ssh.check_config_mode()
        
        try:
            if check_mode_conn == True:
                self.ssh.exit_config_mode() 
                CONSOLE.print('Configure mode exit!', style='success')
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
            print(temp)
            for i in temp:
                with open("../temps/process_wr_read.txt", 'a+') as file:
                     file.write(i)

        except FileNotFoundError:
            print('Файл отсутствует.')
        except ValueError as val_er:
            print(val_er)
        with open("../temps/process_wr_read.txt", 'w') as file:
            pass    # не удалять! - очищает файл

    def get_answerCLI(self,command):
        self.check_connection(self.VALUE_CONS_CONNECT)
        self.ssh.enable()
        temp = self.ssh.send_command(command,read_timeout=1)
        if INVALID_INPUT in temp:
            print(INVALID_INPUT)
        return(temp)
    
    def get_answerCLI_conf(self,command,expcted_string):
        self.check_connection(self.VALUE_CONS_CONNECT)
        self.ssh.enable()
        temp_conf=self.ssh.config_mode()
        temp = self.ssh.send_command(command,read_timeout=1,expect_string=expcted_string)
        if INVALID_INPUT in temp:
            print(INVALID_INPUT)
        self.ssh.exit_config_mode()
        return(temp)


if __name__=="__main__":
    br100 = ConnectBR()
    print(br100.get_answerCLI('sh var'))