import pytest
import yaml
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)



def pytest_generate_tests(metafunc):
   with open("../templates/shw_cmnd_and_reply.txt") as file:
        data_for_check = []
        lines = file.readlines ()
        print(lines,type(lines))
        for line in lines:
            command, value = line.strip().split(', ')
            data_for_check.append((command, value))
   print(data_for_check)
   task_ids = ['Test command {[0]}'.format(t)
             # определям параметр ids чтобы сделать идентификаторы testa
            for t in data_for_check
            ]
   return metafunc.parametrize('commnd_from_file,expect_output_fr_file',data_for_check,ids=task_ids )