import os
import sys
import time

sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.insert(1, os.path.join(sys.path[0], '../..'))    
import pexpect
import yaml
from constants_br100.constants import CONSOLE
from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                     NetmikoTimeoutException)
from server_stor.model_serv_stor_connect import ConnectStorage

serv_stor = ConnectStorage()

# def connect_help_serv():
#     ssh = pexpect.spawn('ssh user@10.27.193.101')
#     print(ssh.expect("password:"))
#     ssh.sendline("12345678")
#     ssh.expect('~')
#     path_img = serv_stor.get_name_last_FW_path()
#     comand_scp = f"scp storage@git-ci-storage.opk-bulat.ru:~/{path_img} ~/OPT/HelmetOS/BR100"
#     print(comand_scp)
#     ssh.sendline(comand_scp)
#     print(ssh.before.decode('utf-8'))
#     print(ssh.expect(":"))
#     ssh.sendline('storage')
#     print(ssh.before.decode('utf-8'))
#     print(ssh.expect('~'))
#     print(ssh.before.decode('utf-8'))
#     # закрываем соединение
#     ssh.close()


class ConnectSrvHelp():
    """Class represents connect and disconnect actions 
        for server UbuntuNS 10.27.193.101.
    """

    def __init__(self, log=True):
        """Init Connect-class to server UbuntuNS 10.27.193.101."""
        
        try:
            with open("../server_help/constants_connect.yaml") as f2:
                self.VALUE_CONS_CONNECT = yaml.safe_load(f2)
            self.ssh = ConnectHandler(**self.VALUE_CONS_CONNECT)
        except ConnectionRefusedError:
            CONSOLE.print(
                    "*" * 5, "Error connection to :",
                    self.VALUE_CONS_CONNECT['ip'],
                    'port:', self.VALUE_CONS_CONNECT['port'], "*" * 5,
                    "\nConnection refused - Console is busy!",
                    style='fail')
            exit()
    def check_connection(self, log=True):
        """Check connection to Server."""
        if log:
            CONSOLE.print(
                'Пробую подключиться к', self.VALUE_CONS_CONNECT['ip'],
                'порт:', self.VALUE_CONS_CONNECT['port'], "...",
                style="info")
        try:
            CONSOLE.print('Server',
                self.VALUE_CONS_CONNECT['ip'], 'порт:',
                self.VALUE_CONS_CONNECT['port'], "подключен!",
                style='success')
        except (NetmikoAuthenticationException,
                NetmikoTimeoutException):
            CONSOLE.print(
                "*" * 5, "Ошибка подключения к:",
                self.VALUE_CONS_CONNECT['ip'],
                'порт:', self.VALUE_CONS_CONNECT['port'], "*" * 5,
                style='fail')
    
    def get_img_from_store(self):
        """Получить свежую прошивку с сервера прошивок ci-storage.opk-bulat.ru."""
        path_img, img_name = serv_stor.get_name_last_FW_path()
        print(path_img)
        
        comand_scp = f"scp storage@git-ci-storage.opk-bulat.ru:~/{path_img}*EFI.img ~/OPT/HelmetOS/BR100"
        # print("**",comand_scp)
        output_scp = self.ssh.send_command_timing(comand_scp)
        # print(output_scp)
        output = self.ssh.send_command_timing('storage')
        # print(output)

    def up_http_serv(self):
        """Поднять http_serv в директории с прошивкой."""
        output = self.ssh.send_command_timing('cd OPT/HelmetOS/BR100/')
        # print(output)
        output = self.ssh.send_command_timing('sudo python3 -m http.server 80')
        time.sleep(30)
        # print(output)


if __name__=="__main__":
    srv_help = ConnectSrvHelp()
    print(srv_help.up_http_serv())