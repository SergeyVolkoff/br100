""" Тесты вывода данных по интерфейсу на коммутаторе."""
import os
import sys

import allure
import pytest
import yaml

sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)
from checks.check_speed_inter import *

@allure.feature ('Тест интерфейса.')
@allure.story('1.проверка вывода скорости линка по интерфейсу.')
def test_check_int_link_speed():
     '''Тестирование вывода скорости линка по интерфейсу eth0.'''
     assert check_int_link_speed('eth0')==True, f'В выводе в командную строку нет нужных данных.'

@allure.feature ('Тест интерфейса.')
@allure.story('2.проверка вывода duplex по интерфейсу.')
def test_check_int_duplex():
     '''Тестирование вывода duplex по интерфейсу eth0.'''
     assert check_int_duplex('eth0')==True, f'В выводе в командную строку нет нужных данных.'

@allure.feature ('Тест интерфейса.')
@allure.story('3.проверка вывода mtu по интерфейсу.')
def test_check_int_mtu():
     '''Тестирование вывода mtu по интерфейсу eth0.'''
     assert check_int_mtu('eth0')==True, f'В выводе в командную строку нет нужных данных.'
