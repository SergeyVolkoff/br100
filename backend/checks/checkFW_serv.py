import allure
import datetime as dt
import re
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from backend.server_stor.model_serv_stor_connect import ConnectStorage

serv_stor = ConnectStorage()
serv_stor.check_connection()

def checkFW_serv():
    '''Получить на git-ci-storage имя имиджа для обновления прошивки.'''
    output_data = serv_stor.ssh.send_command_timing('ls -a git-ci-storage/BR100-24F6X')
    patern_tar = 'images_BR100-24F6X_(?P<date_fw>\d+\-\d+\-\d+)'
    #  Получаем список прошивок
    date_list = re.findall(patern_tar, output_data)
    maxDate = date_list[0]  # выбирает максимальной первую дату
    for date in date_list:  # по очереди перебираем даты
        if date > maxDate:  # если дата больше, чем записанная в  maxDate
            maxDate = date  # пишем ее в maxDate
    # Формируем имя нужной прошивки и директории ее хранения
    name_tar = 'images_BR100-24F6X_'+maxDate+'.tar'
    name_dir = 'images_BR100-24F6X_'+maxDate
    serv_stor.ssh.send_command_timing(f'mkdir {name_dir}')
    command_unpack = f'tar -xvf git-ci-storage/BR100-24F6X/{name_tar} -C ~/{name_dir}'
    # Распаковываем в новой dir хранилища tar-file
    result_unpack = serv_stor.ssh.send_command_timing(command_unpack)
    # Извлекаем список имиджей после распаковки
    output_data = serv_stor.ssh.send_command_timing(f'ls -a {name_dir}/output/images')
    pattern_name_efi = '(?P<img_name>\S+(?<=_EFI))'
    reg_output= re.search (pattern_name_efi, output_data)
    # Извлекаем имя нужного нам имиджа
    reg_img_name = reg_output.group('img_name')+'.img'
    return reg_img_name


if __name__ == "__main__":
    print(checkFW_serv())