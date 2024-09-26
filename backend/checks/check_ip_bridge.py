import re
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
from br100.model_br100 import ConnectBR
from cfg_br100.cfg_reset import ConfigReset

br100 = ConnectBR()
br100.check_connection()

def check_ip_bridge():
    br100.ssh.enable()
    '''Проверка назначения ip адреса на bridge.'''
    file_commands = "../templates/cfg_br_ip.txt"
    # with open("../templates/cfg_br_ip.txt", 'a') as file:
    #     commands = file.readlines()
    # print(commands)
    br100.ssh.send_config_from_file("../templates/cfg_br_ip.txt")
    output_cli = br100.ssh.send_command_timing('sh interface br3 | begin inet')
    expect_output = r'inet (?P<ip_br>\d+.\d+.\d+.\d+.\d+)'
    try:
        reg_output = re.search (expect_output,output_cli)
        print(expect_output)
        print("!!!",reg_output)
        reg_output_gr = reg_output.group('ip_br')
        print("***",reg_output_gr)
    except AttributeError as err:
                print(err, f"Вызвано исключение при отправке комады:reg_output.group() на вывод cli:{output_cli} ")
                print(f'Ожидания ({reg_output_gr}) и вывод в cli НЕ совпадают..')
                return False
    if reg_output_gr:
        br100.ssh.send_command_timing('no bridge-domain 3 protocol ieee')
        return True
    else:
        return False





if __name__ == "__main__":
    print(check_ip_bridge())