import re
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
# from br100.model_br100 import ConnectBR
# br100 = ConnectBR()
INVALID_INPUT = "Invalid input detected"

class ConnectStorage():
    """Class represents connect and disconnect actions for Node."""

    def __init__(self, log=True):
        """Init Connect-class."""
        
        try:
            with open("../server_stor/constants_connect.yaml") as f2:
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
    
    def get_date_last_FW(self):
        '''Получить на git-ci-storage дату последнего обновления прошивки.'''
        output_data = self.ssh.send_command_timing('ls -a git-ci-storage/BR100-24F6X')
        patern_tar = 'images_BR100-24F6X_(?P<date_fw>\d+\-\d+\-\d+)'
        #  Получаем список прошивок
        date_list = re.findall(patern_tar, output_data)
        maxDate = date_list[0]  # выбирает максимальной первую дату
        for date in date_list:  # по очереди перебираем даты
            if date > maxDate:  # если дата больше, чем записанная в  maxDate
                maxDate = date  # пишем ее в maxDate
        return maxDate

    def get_name_last_FW_path(self):
        '''Получить на git-ci-storage name последнего обновления прошивки.'''
        maxDate = self.get_date_last_FW()
        # Формируем имя нужной прошивки и директории ее хранения
        name_tar = 'images_BR100-24F6X_'+maxDate+'.tar'
        name_dir = 'images_BR100-24F6X_'+maxDate
        self.ssh.send_command_timing(f'mkdir {name_dir}')
        command_unpack = f'tar -xvf git-ci-storage/BR100-24F6X/{name_tar} -C ~/{name_dir}'
        # Распаковываем в новой dir хранилища tar-file
        result_unpack = self.ssh.send_command_timing(command_unpack)
        # Извлекаем список имиджей после распаковки
        output_data = self.ssh.send_command_timing(f'ls -a {name_dir}/output/images')
        pattern_name_efi = '(?P<img_name>\S+(?<=_EFI))'
        reg_output= re.search (pattern_name_efi, output_data)
        # Извлекаем имя нужного нам имиджа
        img_name = reg_output.group('img_name')
        print(img_name)
        # Извлекаем имя path
        path_img = f'{name_dir}/output/images/'
        return path_img, img_name
    
        


if __name__=="__main__":
    str = ConnectStorage()
    # print(str.check_connection())
    
    print(str.get_name_last_FW_path())
