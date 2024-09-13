import allure
import datetime as dt
import re
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
from br100.model_br100 import ConnectBR
from backend.server_stor.model_serv_stor_connect import ConnectStorage

br100 = ConnectBR()
br100.check_connection()
serv_stor = ConnectStorage()

def compare_FW_srvANDdut():
    dateFW_DUT = br100.get_date_FW()
    print(dateFW_DUT)
    dateFW_stor = serv_stor.get_date_last_FW()
    print(dateFW_stor)
    dateFW_DUT = dt.datetime.strptime(dateFW_DUT,"%d/%m/%Y")
    dateFW_stor = dt.datetime.strptime(dateFW_stor,"%Y-%m-%d")
    result_compare = (dateFW_DUT<dateFW_stor)
    if result_compare:
        name_last_FW = serv_stor.get_name_last_FW_path()
        # result_upgradeFW = 
        
    

if __name__ == "__main__":
    print(compare_FW_srvANDdut())