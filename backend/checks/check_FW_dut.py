import datetime as dt
import os
import re
import sys
import time

import allure
import pandas as pd

sys.path.insert(1, os.path.join(sys.path[0],'..'))
from br100.model_br100 import ConnectBR

from backend.server_help.model_serv_help_connect import ConnectSrvHelp
from backend.server_stor.model_serv_stor_connect import ConnectStorage

br100 = ConnectBR()
serv_stor = ConnectStorage()
serv_help = ConnectSrvHelp()

def check_FW_dut():
    '''Возвращает TRUE or FALSE как результат проверки даты прошивки после прошивки.
    Проверяет дату прошивки на DUT.
    Получает на git-ci-storage дату последней прошивки, сравнивая с текущей датой.
    Если есть свежая, распаковывает ее в новую директорию. 
    Получает имя и адрес распакованного имиджа.
    Копирует нужный имидж на UbuntuNS 10.27.193.101, запускает в директории http_serv.
    Копирует на коммутатор новую прошивку и перезапускает его.
    Снова проверяет дату прошивки на коммутаторе и сравнивает с последней на сервере.
    '''

    # Получаем дату прошивки на DUT
    dateFW_DUT = br100.get_date_FW()
    # print("***dateFW_DUT=",dateFW_DUT)
    # br100.ssh.disconnect()

    # Получаем дату прошивки на git-ci-storage
    dateFW_stor = serv_stor.get_date_last_FW()
    print("***dateFW_stor=",dateFW_stor)

    # Приводим даты к виду datetime
    dateFW_DUT_dt = dt.datetime.strptime(dateFW_DUT,"%d/%m/%Y")
    dateFW_DUT_dt = pd.to_datetime(dateFW_DUT_dt)
    print("dateFW_DUT_dt = ", dateFW_DUT_dt)
    dateFW_stor_dt = dt.datetime.strptime(dateFW_stor,"%Y-%m-%d")
    dateFW_stor_dt = pd.to_datetime(dateFW_stor_dt)
    print("dateFW_stor_dt = ", dateFW_stor_dt)

    # Сравниваем даты прошивок на DUT и на git-ci-storage
    # если на DUT дата раньше вернет True
    result_compare = (dateFW_DUT_dt<dateFW_stor_dt)
    if result_compare:
        # Получаем имя прошивки и путь до нее после распаковки архива
        # на git-ci-storage
        print(f'Даты прошивки на DUT и git-ci-storage не совпадают!\n\
              Стартует прошивка!\n\
              Датa прошивки на DUT - {dateFW_DUT}\n\
              Датa прошивки на git-ci-storage - {dateFW_stor}'
                )
        path_img, img_name = serv_stor.get_name_last_FW_path()
        print('path_img, img_name=',path_img, img_name)

        # Копируем прошивку на сервер 10.27.193.101 где будет http сервер
        result_get_img_store = serv_help.get_img_from_store()
        print('result_get_img_store=',result_get_img_store)

        # Поднимаем на 30 сек http сервер в директории с прошивкой
        result_up_http_serv = serv_help.up_http_serv()
        print('result_up_http_serv=',result_up_http_serv)

        #  Копируем прошивку с http сервер на DUT 
        result_sendFWfromHelpSRV = br100.sendFWfromHelpSRV()
        print(result_sendFWfromHelpSRV)

        # Перезагружаем коммутатор, применяя прошивку
        result_reboot = br100.reboot_DUT()
        print('Dut reboot',result_reboot)
        time.sleep(120)
        br100.ssh.send_command_timing('admin')
        br100.ssh.send_command_timing('admin')

        # Снова сравниваем даты прошивок на DUT и на git-ci-storage
        dateFW_DUT1 = br100.get_date_FW()
        print("dateFW_DUT1 = ", dateFW_DUT1)
        dateFW_DUT1_dt = dt.datetime.strptime(dateFW_DUT1,"%d/%m/%Y")
        print("dateFW_DUT1_dt = ",dateFW_DUT1_dt)
        dateFW_DUT1_dt = pd.to_datetime(dateFW_DUT1_dt)
        print("dateFW_stor_dt = ", dateFW_stor_dt)

        # Если даты совпали - завершаем
        if dateFW_DUT1_dt == dateFW_stor_dt:
            print(f"Даты прошивки на DUT и git-ci-storage совпадают!\n\
              Датa прошивки на DUT - {dateFW_DUT1}\n\
              Датa прошивки на git-ci-storage = {dateFW_stor}'")
            return True
        else: 
            print(f'Даты прошивки на DUT и git-ci-storage не совпали,\n\
                но коммутатор не пролился!\n\
              Датa прошивки на DUT - {dateFW_DUT1} \n\
              Датa прошивки на git-ci-storage - {dateFW_stor}')
            return False
    # Если до начала прошивки даты FW совпали - завершаем  
    if dateFW_DUT_dt == dateFW_stor_dt:
        print(f'Даты прошивки на DUT и git-ci-storage совпадают!\n\
            Датa прошивки на DUT - {dateFW_DUT} \n\
            Датa прошивки на git-ci-storage - {dateFW_stor}')
        return True
    else: 
        # Если до начала прошивки дата FW свежее (чудом!) - завершаем
        print(f'Прошивка на DUT свежее, чем на сервер! \n\
        Датa прошивки на DUT - {dateFW_DUT}\n\
        Датa прошивки на git-ci-storage - {dateFW_stor}')
        return True

if __name__ == "__main__":
    print(check_FW_dut())