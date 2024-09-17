""" Тесты проверки поддержки логгирования."""
import sys
import os
import allure
sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)
from checks.check_logging import *

@allure.feature ('Тесты логгирования событий.')
@allure.story('2.проверка логгирования событий в файл.')
def test_check_logging_file():
     assert check_logging_file()==True, f'Логиррование не ведется или ведется не в файл logs!'  # noqa: E712, F405, F541

