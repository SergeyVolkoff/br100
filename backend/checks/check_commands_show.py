import os
import re
import sys

import allure

sys.path.insert(1, os.path.join(sys.path[0],'..'))
from br100.model_br100 import ConnectBR
from cfg_br100.cfg_reset import ConfigReset

br100 = ConnectBR()
# br100.check_connection()

    
def check_execute_command(commnds_sh: str, expect_output: str,  timeout: int = 2):
    '''Сравнивает фактический результат выполнения команды show с ожидаемым'''
    print("Test 2", f"Проверка команды:{commnds_sh}", sep='\n')
    try:
        with allure.step(f'Отправка команды {commnds_sh} '):
            output_cli = br100.get_answerCLI(command=commnds_sh)
            print("В cli получили:", output_cli)
            try:
                reg_output = re.search (expect_output,output_cli)
                # print(expect_output)
                # print("!!!",reg_output)
                reg_output_gr = reg_output.group()
                # print("***",reg_output_gr)
            except AttributeError as err:
                print(err, f"Вызвано исключение при отправке комады:reg_output.group() на вывод cli:{output_cli} ")
                print(f'Ожидания ({reg_output_gr}) и вывод в cli НЕ совпадают..')
                return False
        with allure.step(
            f'Проверяем наличие ожидаемых элементом ({expect_output}) в ответе в CLI (см ниже stdout) :'
            ):    
            if reg_output_gr in output_cli:
                print(f"Ожидания ({reg_output_gr}) и вывод в cli совпадают!")
                return True
            else: 
                print(f'Ожидания ({reg_output_gr}) и вывод в cli НЕ совпадают!')
                return False

    except ValueError as err:
        print(err, "Вызвано исключение при отправке комады")
        return False

def check_change_hostname(new_hostname):
    '''Проверка смены имени хоста'''
    expected_string = new_hostname
    try:
        with allure.step('Отправка команды на изменения hostname'):
            command = f'hostname {new_hostname}'
            # br100.get_answerCLI_conf(command)
            br100.ssh.send_config_set(command,)
            
            # Меняем имя хоста
            output_cli = br100.ssh.send_command_timing('show hostname',read_timeout=0)
            # Получаем вывод из cli с новым именем хоста
            regex_output = re.search(r'DUT\w+',output_cli)
            # Отбираем новое имя 
            try:
                regex_output_gr = regex_output.group()
                if regex_output_gr == new_hostname:
                    # Сравниваем полученное имя и введенное 
                    print("Ожидания и вывод в cli совпадают!")
                    return True
                else:
                    return False
            except AttributeError as err:
                print(err, "Вызвано исключение при отправке комады")
                # Возвращаем имя DUTu
                print('Ожидания и вывод в cli НЕ совпадают..')
                return False
        
    except ValueError as err:
        print(err, "Вызвано исключение при отправке комады")
        return False

def check_logging_file():
    '''Проверка логгирования событий в файл.'''
    try:
        with allure.step(f'Отправка команды настройки логгирования в файл'):
            # br100.get_answerCLI_conf(command='no logging logfile')
            br100.ssh.enable()
            br100.ssh.config_mode()
            output_cli = br100.ssh.send_command_timing('logging logfile logs 6 size 4096')
            br100.ssh.exit_config_mode()
            output_cli  = br100.ssh.send_command_timing('show logging logfile')
            expect_output = r'logging\W+(?P<status_log>\w+)'
            #  отбираем из вывода в cli нужную строку 2мя группами: status_log и name_log
            reg_output = re.search (expect_output,output_cli)
            status_log = reg_output.group('status_log')
        with allure.step(
            f'Проверяем наличие ожидаемых элементом ({status_log}) в ответе в CLI (см ниже stdout) :'
            ):    
            if  status_log in output_cli:
                print(f"Ожидания ({status_log}) и вывод в cli совпадают! status_loggging = {status_log}")
                # br100.ssh.disconnect()
                return True
            else: 
                print(f'Ожидания ({status_log}) и вывод в cli НЕ совпадают!')
                # br100.ssh.disconnect()
                return False
    except ValueError as err:
        print(err, "Вызвано исключение при отправке комады")
        # br100.ssh.disconnect()
        return False

def check_int_link_speed(interface):
        output_cli = br100.ssh.send_command_timing(f'show interface eth0',read_timeout=1)
        try:
            if 'link-speed' in output_cli:
                regex_output = re.search(r'link-speed (?P<link_speed>.+)',output_cli)
                link_speed = regex_output.group('link_speed')
            else:
                return False
        except AttributeError as err:
            print(err, 
                    f"Вызвано исключение при отправке комады:reg_output.group() на вывод cli:{output_cli} "
                    )
            return False
        print('link_speed -', link_speed)
        return True
    
def check_int_mtu(interface):
    output_cli = br100.ssh.send_command_timing(f'show interface {interface}')
    try:
        if 'mtu' in output_cli:
            regex_output = re.search(r'mtu (?P<mtu_size>\d+)',output_cli)
            mtu_size = regex_output.group('mtu_size')
        else:
            return False
    except AttributeError as err:
        print(err, 
                f"Вызвано исключение при отправке комады:reg_output.group() на вывод cli:{output_cli} "
                )
        return False
    print('mtu_size =', mtu_size)
    return True

def check_int_duplex(interface):
    output_cli = br100.ssh.send_command_timing(f'show interface {interface}')
    try:
        if 'duplex' in output_cli:
            regex_output = re.search(r'duplex(?P<duplex>\S+)',output_cli)
            duplex = regex_output.group('duplex')
        else:
            return False
    except AttributeError as err:
        print(err, 
                f"Вызвано исключение при отправке комады:reg_output.group() на вывод cli:{output_cli} "
                )
        return False
    print('duplex',duplex)
    return True

if __name__ == "__main__":
    print(check_int_mtu('eth0'))