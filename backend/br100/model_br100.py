"""Base class for switches BR100."""
import datetime as dt
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

from server_stor.model_serv_stor_connect import ConnectStorage
serv_stor = ConnectStorage()

# sys.path.append(os.getcwd())
# print("***",sys.path)
import yaml  # noqa: E402
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
            if check_mode_conn is True:
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
    
    def get_answerCLI_conf(self,command):
        self.check_connection(self.VALUE_CONS_CONNECT)
        self.ssh.enable()
        temp = self.ssh.send_command_timing(command,read_timeout=1)
        self.ssh.exit_config_mode()
        if INVALID_INPUT in temp:
            print(INVALID_INPUT)
        
        return temp
            
    def get_date_FW(self):
        '''Сравниваем текущую дату и дату установленой прошивки
        если тек дата больше - вернет Тру.'''
        output_cli = self.ssh.send_command_timing('show version')
        except_output = 'MSK (?P<date>.+)'
        regex_output = re.search(except_output,output_cli)
        dateFW = regex_output.group('date')
        return(dateFW)
        # date_curent_F = dt.datetime.now()
        # dateFW_F = dt.datetime.strptime(dateFW,"%d/%m/%Y")
        # return(date_curent_F>dateFW_F)
    
    def get_ip_eth0(self):
        self.check_connection(self.VALUE_CONS_CONNECT)
        self.ssh.enable()
        temp = self.ssh.send_command('sh ip interface eth0 brief',read_timeout=1)
        print(temp)
        temp1 = re.search('eth0\s+\*(?P<ip_eth0>\S+)',temp)
        try:
            ip_eth0 = temp1.group('ip_eth0')
        except NetmikoTimeoutException as err:
            print("Не смог получить и обработать ip_eth0 error", err)
        return ip_eth0

    def sendFWfromHelpSRV(self):
        with open("../server_help/constants_connect.yaml") as f2:
                self.VALUE_CONS_CONNECT = yaml.safe_load(f2)
        ip_HelpSRV = (self.VALUE_CONS_CONNECT['ip'])
        path_img, img_name = serv_stor.get_name_last_FW_path()
        cmnd_load_FW = f'copy image {ip_HelpSRV}/{img_name}.img'
        print("***",cmnd_load_FW)
        output = self.ssh.send_command_timing(
            cmnd_load_FW,strip_command=False
            )
        return output


if __name__=="__main__":
    br100 = ConnectBR()
    print(br100.sendFWfromHelpSRV())