import allure
import re
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
from br100.model_br100 import ConnectBR
from cfg_br100.cfg_reset import ConfigReset

br100 = ConnectBR()
br100.check_connection()

    
def check_execute_command(commnds_sh: str, expect_output: str,  timeout: int = 2):
    '''Сравнивает фактический результат выполнения команды show с ожидаемым'''
    print("Test 2", "Проверка команды:", sep='\n')
    try:
        with allure.step(f'Отправка команды {commnds_sh} '):
            output_cli = br100.get_answerCLI(command=commnds_sh)
            print("###", output_cli)
            try:
                reg_output = re.search (expect_output,output_cli)
                # print(expect_output)
                # print("!!!",reg_output)
                reg_output_gr = reg_output.group()
                # print("***",reg_output_gr)
            except AttributeError as err:
                print(err, f"Вызвано исключение при отправке комады:reg_output.group() на вывод cli:{output_cli} ")
                print('Еhe expectation was not met..')
                return False
        with allure.step(
            f'Проверяем наличие ожидаемых элементом ({expect_output}) в ответе в CLI (см ниже stdout) :'
            ):    
            if reg_output_gr in output_cli:
                print("The expectation was justified!")
                return True
            else: 
                print('Еhe expectation was not met')
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
                    print("The expectation was justified!")
                    return True
                else:
                    return False
            except AttributeError as err:
                print(err, "Вызвано исключение при отправке комады")
                # Возвращаем имя DUTu
                print('Еhe expectation was not met..')
                return False
        
    except ValueError as err:
        print(err, "Вызвано исключение при отправке комады")
        print('Еhe expectation was not met')
        return False


def check_logging_file():
    '''Проверка логгирования событий в файл.'''
    try:
        with allure.step(f'Отправка команды настройки логгирования в файл'):
            # br100.get_answerCLI_conf(command='no logging logfile')
            br100.get_answerCLI_conf(command='logging logfile logs 6 size 4096')
            output_cli = br100.get_answerCLI(command='show logging logfile')
            expect_output = 'logging\W+(?P<status_log>\w+)'
            #  отбираем из вывода в cli нужную строку 2мя группами: status_log и name_log
            reg_output = re.search (expect_output,output_cli)
            status_log = reg_output.group('status_log')
        with allure.step(
            f'Проверяем наличие ожидаемых элементом ({status_log}) в ответе в CLI (см ниже stdout) :'
            ):    
            if  status_log in output_cli:
                print(f"The expectation was justified! status_loggging = {status_log}")
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
    print(check_change_hostname('Art'))