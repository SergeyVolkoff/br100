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
        # print(self.list_labs)
        self.name_lab = name_lab

    def get_all_proj (self):

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
        CONSOLE.print(f"*** ALL nodes in {lab.name} lab ***",style='success')
        return  lab.nodes_summary()
        
    
    def start_all_nodes_project(self):
        
        """Старт всех устройств в лабе"""

        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        lab.open() # open lab
        lab.start_nodes(poll_wait_time=5)
        CONSOLE.print(f"*** ALL nodes in {lab.name} lab ***",style='success')
        return  lab.nodes_summary()
    
    def get_lab_status(self):

        """ Вернет lab_id, статус моей лабы """

        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        #lab.close()
        print(lab.project_id)
        return f"GNS3 lab_name: {lab.name}, lab_id:{lab.project_id}, lab status: {lab.status}"
    
    def start_node_name(self, node_name):

        """ Запуск 2go узла в проекте"""
        
        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        lab.open() # open lab
        r2 = Node(
            project_id=lab.project_id, 
            name=node_name,
            connector=self.connector
            ) # создаем экз-р устр-ва
        
        r2.get()
        r2.start()
        CONSOLE.print (f'Node {r2.name} {r2.status}',style='success')
    
    def stop_node_name(self,node_name):
        """ Запуск 2go узла в проекте"""
        
        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        lab.open() # open lab
        r1 = Node(
            project_id=lab.project_id, 
            name=node_name,
            connector=self.connector
            ) # создаем экз-р устр-ва
        r1.get()
        r1.stop()
        CONSOLE.print (f'Node {r1.name} {r1.status}',style='success')
        
        
        # link_r1_DUT.get()
        # link_r1_DUT.delete()

    def get_links_node(self,node_name):
        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        r1 = Node(
            project_id=lab.project_id, 
            name=node_name,
            connector=self.connector
            ) # создаем экз-р устр-ва
        r1.get()
        link_r1_sw3 = r1.links[1].nodes # получаем 1й линк r1_sw3
        # Извлекаем из словаря имена линков списком
        texts = [item['label']['text'] for item in link_r1_sw3]
        for text in texts:
            print(texts)  #  Получим свой лдинк и линк на другой стороне

        
      

    
if __name__=="__main__":
    name_lab = 'SSV_auto_Tr_GRE'
    gns = ConnectGNS(name_lab = 'SSV_auto_Tr_GRE')
    node_name = 'R1'
    name_lab = 'SSV_auto_Tr_GRE'

    print(gns.get_links_node(node_name),'\n')
