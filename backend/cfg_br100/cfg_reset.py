"""Class for reset, cfg switch BR100."""

import time
import yaml
from ping3 import ping
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# print(sys.path)
from constants_br100.constants import (
    CONSOLE,
)
from br100.model_br100 import ConnectBR


class ConfigReset(ConnectBR):
    """Class for reset BR100 and config from template."""

    def cfg_from_file(self, path_cfg):
        """
        Function for configuration DUT from template.
        """

        self.check_connection(self.VALUE_CONS_CONNECT)
        self.disable_config_mode()
        self.ssh.enable()
        output = self.ssh.send_config_from_file(path_cfg )
        output += self.ssh.send_command("wr mem", expect_string="Building configuration...") 
        print(output)
    

    def reset_cfg_reboot(self):
        """
        reset cfg
        """

        self.check_connection(self.VALUE_CONS_CONNECT)
        self.disable_config_mode()
        self.ssh.enable()
        self.ssh.send_command("copy empty-config startup-config")
        CONSOLE.print(
            "В коммутатор записан базовый конфиг.",
            style="success")
        cmd_list = [
            ["reload","The system has unsaved changes."],
            ["n", "Configuration Not Saved!"],
            ["y",""]
        ]
        output = self.ssh.send_multiline(cmd_list)
        CONSOLE.print(
            output,
            "Коммутатор перезагружается, время ожидания около 70 сек.",
            style="success")
    

if __name__ == "__main__":
    br100 = ConfigReset()
    # br100.check_connection()
    # br100.ssh.enable()
    path_cfg = '../templates/hostname.txt'
    # with open (path_cfg,'r') as commands:
    #     commands_template = commands.read()

    print(br100.cfg_from_file(path_cfg))
    # print(br100.reset_cfg_reboot())