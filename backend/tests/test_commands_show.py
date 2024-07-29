""" Тесты проверки поддержки команд show."""
import pytest
import sys
import os
import allure
sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)
from checks.check_commands_show import *

@allure.feature ('Тесты проверки поддержки команд show.')
@allure.story('проверка 1')

def get_comands_show():
    with open("../templates/show_commands.txt") as file:
       commnds_sh = file.readlines()
        # for lines in file:
        #     print(lines)
    print(commnds_sh)
    return commnds_sh

def get_expect_show():
    with open("../templates/expected_reply_show.txt") as file:
       expected = file.readlines()
        # for lines in file:
        #     print(lines)
    print(expected)
    return expected

commnds_sh = 'show system uptime'
    # ('show system uptime')
    
expect_output = r'up \S+ days'
    # ("r'up \S+ days'")
    


# commnds_sh = ['commnds_sh1({})'.format(t)
#              # определям параметр ids чтобы сделать идентификаторы для понимания вывода теста
#             for t in commnds_sh
#             ]
# print(commnds_sh)
# @pytest.mark.parametrize('expect_output','commnds_sh')

def test_check_commands_show():
    assert check_execute_command(commnds_sh=commnds_sh,expect_output=expect_output)==True,f'**Результат использования команды:f"{commnds_sh}" не соответствует ожиданиям'


if __name__ == "__main__":
    print(get_expect_show())