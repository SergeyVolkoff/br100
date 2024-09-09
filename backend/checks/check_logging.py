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
    '''Проверка логгирования событий в файл.'''
    try:
        with allure.step(f'Отправка команды настройки логгирования в файл'):
            br100.get_answerCLI_conf(command='logging logfile logs 6 size 4096')
            output_cli = br100.get_answerCLI(command='show logging logfile')
            expect_output = 'logging\W+(?P<status_log>enabled)  File Name.+(?P<name_log>logs)'
            #  отбираем из вывода в cli нужную строку 2мя группами: status_log и name_log
            reg_output = re.search (expect_output,output_cli)
            status_log = reg_output.group('status_log')
            name_log = reg_output.group('name_log')
        with allure.step(
            f'Проверяем наличие ожидаемых элементом ({name_log ,name_log}) в ответе в CLI (см ниже stdout) :'
            ):    
            if name_log and status_log in output_cli:
                print("The expectation was justified!")
                br100.ssh.disconnect()
                return True
            else: 
                print('Еhe expectation was not met')
                br100.ssh.disconnect()
                return False
        

    except ValueError as err:
        print(err, "Вызвано исключение при отправке комады")
        br100.ssh.disconnect()
        return False
    
    
if __name__ == "__main__":
    print(check_logging_file())