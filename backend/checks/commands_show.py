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
    
def check_execute_show(command: str, expect_output: str, log_string = "", timeout: int = 5):
    pass
    
if __name__ == "__main__":
    print(check_ver_platform())