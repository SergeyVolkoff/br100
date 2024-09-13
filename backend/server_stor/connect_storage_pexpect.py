import re
import sys
import os
import pexpect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

'''
Проверяем на сервере наличие последней прошивки, выделяем ее имя, распаковываем.
Все работает через класс pexpect!
'''

# Подключаемся к серверу
ssh = pexpect.spawn('ssh storage@git-ci-storage.opk-bulat.ru')
print(ssh.expect("storage@git-ci-storage.opk-bulat.ru's password:"))
ssh.sendline("storage")
ssh.expect('~')
# Смотрим имена архивов прошивок 
ssh.sendline('ls -a git-ci-storage/BR100-24F6X')
ssh.expect('~')
output_data = ssh.before.decode('utf-8')
patern = 'images_BR100-24F6X_(?P<date_fw>\d+\-\d+\-\d+)'
#  Получаем список прошивок
date_list = re.findall(patern, output_data)
maxDate = date_list[0]  # выбирает максимальной первую дату
for date in date_list:  # по очереди перебираем даты
    if date > maxDate:  # если дата больше, чем записанная в  maxDate
        maxDate = date  # пишем ее в maxDate
# Формируем имя нужной прошивки
name_tar = 'images_BR100-24F6X_'+maxDate+'.tar'
# Распаовываем в корне хранилища
command_unpack = f'tar -xvf git-ci-storage/BR100-24F6X/{name_tar}'
ssh.sendline(command_unpack)
ssh.expect('~')

# закрываем соединение
ssh.close()