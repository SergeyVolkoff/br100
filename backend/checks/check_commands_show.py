import allure
import re
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
from br100.model_br100 import ConnectBR

br100 = ConnectBR()
br100.check_connection

    
def check_execute_command(commnds_sh: str, expect_output: str,  timeout: int = 2):
    '''Сравнивает фактический результат выполнения команды с ожидаемым'''
    print("Test 2", "Проверка команды:", sep='\n')
    try:
        with allure.step(f'Отправка команды {commnds_sh} '):
            output_cli = br100.get_answerCLI(command=commnds_sh)
            print("###", output_cli)
            reg_output = re.search (expect_output,output_cli)
            # print(expect_output)
            # print("!!!",reg_output)
            reg_output_gr = reg_output.group()
            # print("***",reg_output_gr)

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


if __name__ == "__main__":
    print(check_execute_command('show system uptime', r'up \S+ days'))
