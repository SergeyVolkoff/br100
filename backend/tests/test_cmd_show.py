""" Тесты проверки поддержки команд show на коммутаторе."""
import os
import sys

import allure
import pytest
import yaml

sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)
from checks.check_commands_show import *


# @pytest.fixture
def generate_cmd_reply():
    '''Фикстура подготовки данных из файла'''
    with open("../templates/shw_cmnd_and_reply.txt") as file:
        data_for_check = []
        lines = file.readlines ()
        for line in lines:
            command, value = line.strip().split(', ')
            # собираем список из команд и ожидаемых ответов
            data_for_check.append((command, value))
    task_ids = ['Test command {[0]}'.format(t)
            # определям параметр ids чтобы сделать идентификаторы testa
            for t in data_for_check
            ]
    return data_for_check, task_ids

data_for_check = generate_cmd_reply()[0]
task_ids = generate_cmd_reply()[1]

@allure.feature ('Тесты проверки поддержки команд show.')
@allure.story('1.проверка команд show.')
@pytest.mark.parametrize('commnd_from_file, expect_output_fr_file', data_for_check, ids=task_ids)
def test_check_execute_command(commnd_from_file, expect_output_fr_file):
        '''Тестирование выполнения команд show из заранее подготовленного файла.
        Цель - убедиться в базовой работоспособности коммутатора после обновления прошивки.
        '''
        print(commnd_from_file)
        assert check_execute_command(  # noqa: E712, F405
        commnds_sh=commnd_from_file, 
        expect_output=expect_output_fr_file)==True,\
        f'**Результат использования команды:f"{commnd_from_file}" не соответствует ожиданиям'


name_host=(
#      'DUT',
#      'DUT_Aggregation_switch_Aggregation_switch_DUT_Aggregation_switc',
#      'DUT_Aggregation_switch_Aggregation_switch_DUT_Aggregation_switch',
#      'DUT_Aggregation_switch_DUT_Aggregation_switch_Aggregation_switch_',
     'DUT1',
#      
)

task_ids = ['Verified name {0}, Name length = {1}'.format(t,len(t))
             # определям параметр ids чтобы сделать идентификаторы для понимания вывода теста
            for t in name_host
            ]

@allure.feature ('Тесты проверки поддержки команд show.')
@allure.story('2.проверка команды смены имени хоста.')
@pytest.mark.parametrize('hostname',name_host,  ids=task_ids)
def test_check_change_hostname(hostname,):
     '''Тестирование  смены имени хоста'''
     assert check_change_hostname (new_hostname=hostname)==True, f'Сменить имя не удалось!'

@allure.feature ('Тесты логгирования событий.')
@allure.story('3.проверка создания файла логгирования.')
def test_check_logging_file():
     '''Тестирование создания файла логгирования.'''
     assert check_logging_file()==True, f'Логиррование не ведется или ведется не в файл logs!'


# if __name__ == "__main__":
#     print(test_check_commands_show())
