""" Тест проверки прошивки."""
import os
import sys

import pytest

sys.path.insert(1, os.path.join(sys.path[0],'..'))
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
# print(sys.path)
from checks.check_FW_dut import check_FW_dut


def test_check_FW_dut():
    '''Тест проверки свежей версии прошивки на коммутаторе.'''
    assert check_FW_dut() == True, f'Даты прошивки на DUT и git-ci-storage не совпали!!' 