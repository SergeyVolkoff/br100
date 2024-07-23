import json
from rich import print
from rich.theme import Theme
from rich.console import Console
from pprint import pprint

import yaml

my_colors = Theme(
     #добавляет цветовую градацию для rich
    {
        "success":" bold green",
        "fail": "bold red",
        "info": "bold blue"
    }
)
CONSOLE = Console(theme=my_colors)
NAME_DEV = "DUT"