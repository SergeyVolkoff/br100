import allure
import re
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))

from br100.model_br100 import ConnectBR

br100 = ConnectBR()
br100.check_connection


def check_ver_platform():
    print("Test 1", "Проверка платформы:", sep='\n')
    try:
        with allure.step('Отправка команды на просмотр версии платформы.'):
            temp = br100.ssh.send_command('show version')
        temp1 =  re.search(r'EOS\s(?P<ver_OS>\S+) (?P<ver_HW>\S+)',temp)
        ver_HW=temp1.group('ver_HW')
        
        with allure.step('Сверка версии платформы - ожидается "BR-100-24f6x".'):
            if "BR-100-24f6x" in ver_HW:
                print(f'Platform is {ver_HW}, its - ok! ')
                print("")
                with open("../valueReportTest.txt", 'a') as file:
                    file.write('Test_name:Проверка работы функционала show'+'\n'+f'ver_platform:{ver_HW}'+'\n')
                return True
            else:
                print(f"Version platform wrong - {ver_HW}! ")
                return False
    except ValueError as err:
        return False
    
def check_execute_command(commnds_sh: str, expect_output: str,  timeout: int = 2):
    '''Сравнивает фактический результат выполнения команды с ожидаемым'''
    print("Test 2", "Проверка команды:", sep='\n')
    try:
        with allure.step('Отправка команды'):
            output_cli = br100.get_answerCLI(command=commnds_sh)
            print("###", output_cli)
            reg_output = re.search (expect_output,output_cli)
            print(expect_output)
            print("!!!",reg_output)
            reg_output_gr = reg_output.group()
            print("***",reg_output_gr)
            
        if reg_output_gr in output_cli:
            print("the expectation was justified!")
            return True
        else: 
            print('the expectation was not met')
            return False

    except ValueError as err:
        print(err, "Вызвано исключение при отправке комады")
        return False


if __name__ == "__main__":
    print(check_execute_command('show system uptime', r'up \S+ days'))
    # print(check_execute_command('show system-information cpu', r'System CPU Information'))