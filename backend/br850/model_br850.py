"""Base class for switches BR100."""
import datetime as dt
import os
import re
import sys
import time
from string import Template

import pandas as pd
from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                     NetmikoTimeoutException)

sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from br100.model_br100 import ConnectBR

class ConnectBR850(ConnectBR):
    pass


if __name__=="__main__":
    br850 = ConnectBR850()
    print(br850.get_date_FW())