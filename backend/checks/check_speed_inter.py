import re
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
from br100.model_br100 import ConnectBR
from cfg_br100.cfg_reset import ConfigReset

br100 = ConnectBR()
br100.check_connection()


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