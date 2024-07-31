""" Тесты проверки поддержки команд show."""
import pytest
import yaml
import sys
import os
import allure
sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)
from checks.check_commands_show import *


@allure.feature ('Тесты проверки поддержки команд show.')
@allure.story('проверка 1')


def test_check_commands_show(commnd_from_file, expect_output_fr_file):
    print(commnd_from_file)
    assert check_execute_command(
        commnds_sh=commnd_from_file, 
        expect_output=expect_output_fr_file)==True,\
        f'**Результат использования команды:f"{commnd_from_file}" не соответствует ожиданиям'

if __name__ == "__main__":
    print(check())