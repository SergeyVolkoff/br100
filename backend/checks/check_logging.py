import allure
import re
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
from br100.model_br100 import ConnectBR
from cfg_br100.cfg_reset import ConfigReset

br100 = ConnectBR()
br100.check_connection()

def check_logging_file():
    """Проверка логгирования событий в файл.

    Returns:
        _type_: bool
    """
    try:
        with allure.step(f'Отправка команды настройки логгирования в файл'):
            br100.get_answerCLI_conf(command='logging logfile logs 6 size 4096')
            output_cli = br100.get_answerCLI(command='show logging logfile')
            expect_output = r'logging\W+(?P<status_log>.+)\n.+File Name.+(?P<name_log>var\/.+)'
            #  отбираем из вывода в cli нужную строку 2мя группами: status_log и name_log
            print(expect_output)
            reg_output = re.search (expect_output,output_cli)
            print(reg_output)
            status_log = reg_output.group('status_log')
            name_log = reg_output.group('name_log')
        with allure.step(
            f'Проверяем наличие ожидаемых элементом File logging=({status_log}) ,File Name=({name_log}) в ответе в CLI (см ниже stdout) :'
            ):    
            if name_log and status_log in output_cli:
                print(f"The expectation was justified! File logging=({status_log}) ,File Name=({name_log})")
                br100.ssh.disconnect()
                return True
            else: 
                print(f'Еhe expectation was not met!File logging=({status_log}) ,File Name=({name_log})')
                br100.ssh.disconnect()
                return False
        

    except ValueError as err:
        print(err, "Вызвано исключение при отправке комады")
        br100.ssh.disconnect()
        return False
    
    
if __name__ == "__main__":
    print(check_logging_file())