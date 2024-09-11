import allure
import datetime as dt
import re
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
from br100.model_br100 import ConnectBR
from cfg_br100.cfg_reset import ConfigReset

br100 = ConnectBR()
br100.check_connection()

def check_verFW_date():
    output_cli = br100.ssh.send_command_timing('show version')
    except_output = 'MSK (?P<date>.+)'
    regex_output = re.search(except_output,output_cli)
    dateFW = regex_output.group('date')
    print(dateFW)
    date_curent_F = dt.datetime.now()
    dateFW_F = dt.datetime.strptime(dateFW,"%d/%m/%Y")
    # Сравниваем текущую дату и дату установленой прошивки
    print(date_curent_F>dateFW_F)
    

if __name__ == "__main__":
    print(check_verFW_date(),)