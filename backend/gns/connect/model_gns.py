import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from gns3fy import Gns3Connector, Project, Node, Link
from tabulate import tabulate

from rich import print
from rich.theme import Theme
from rich.console import Console
from constants_br100.constants import (
    CONSOLE,
)

class ConnectGNS():

    def __init__(self,name_lab):

        """ Определение коннектора(connector) и проекта (lab) """

        self.server_url = "http://10.27.193.245:3080"
        self.connector = Gns3Connector(url=self.server_url)
        self.list_labs = (tabulate(self.connector.projects_summary(is_print=False), headers=["Project Name"]))
        print(self.list_labs)
        self.name_lab = name_lab

    def all_proj (self):

        """ Возвращает перечень всех лаб в ГНС"""

        return tabulate(
            self.connector.projects_summary(is_print=False),
            headers=["Project Name", "Project ID", "Total Nodes", "Total Links", "Status"],
        )
    
    def get_nodes(self):

        """ Вернет все узлы в лабе"""

        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        lab.open() # open lab
        lab.start_nodes(poll_wait_time=5)
        CONSOLE.print(f"*** ALL nodes in {lab.name} lab ***",style='success')
        return  lab.nodes_summary()
    
    def start_nodes_from_project(self):
        
        """Старт всех устройств в лабе"""

        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        lab.open() # open lab
        lab.start_nodes(poll_wait_time=5)
        CONSOLE.print(f"*** ALL nodes in {lab.name} lab ***",style='success')
        return  lab.nodes_summary()
    
if __name__=="__main__":
    name_lab = 'SSV_auto_Tr_GRE'
    gns = ConnectGNS(name_lab = 'SSV_auto_Tr_GRE')
    
    # print (gns.get_ver_gns(),'\n')
    # print(gns.all_proj(),'\n')
    name_lab = 'SSV_auto_Tr_GRE'
    print(gns.get_nodes(),'\n')

    # print(gns.start_node())
    # print(gns.start_nodes_from_project())
    # print( gns.get_nodes(),'\n')