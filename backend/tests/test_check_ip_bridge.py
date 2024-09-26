""" Тест интерфейса bridge ."""
import os
import sys

import allure
import pytest
import yaml

sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)
from checks.check_ip_bridge import *

@allure.feature ('Тест интерфейса bridge.')
@allure.story('1.проверка назначения ip адреса интерфейсу bridge.')
def test_check_ip_bridge():
     '''назначения ip адреса интерфейсу bridge.'''
     assert check_ip_bridge()==True, f'IP адрес на bridge не назначен!'
