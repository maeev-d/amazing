import os
from cells import Cell
from drawing import AsciiRenderer
from blessed import Terminal
from parsing import parsing_config_file
import os
import time

def load_config(file_path="config.txt"):
    config = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                key, val = line.split("=")
                key = key.strip()
                val = val.strip()
                if "," in val:
                    val = tuple(map(int, val.split(",")))
                elif val.isdigit():
                    val = int(val)
                config[key] = val
    return config

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def get_cell(self, x, y):
        return self.grid[y][x]

config = load_config("config.txt")
width = int(config["WIDTH"])
height = int(config["HEIGHT"])
entry = config.get("ENTRY", (0, 0))
exit = config.get("EXIT", (width - 1, height - 1))
term = Terminal()

maze = MazeGenerator(width, height)
renderer = AsciiRenderer(maze, entry, exit)
config = parsing_config_file("config.txt")
os.system('clear')
filename = open("intrro.txt", "r")
col = [
    term.blue,
    term.red,
    term.white,
    term.green,
    term.brown
]
i = 0
for line in filename:
    print(term.red(line.strip()))
    time.sleep(0.1)
os.system('clear')
with term.cbreak():
    while True:
        print(col[i](renderer.render()))
        key = term.inkey()
        if key == "q":
            os.system('clear')
            break
        elif key == "d":
            i = (i + 1) % len(col)
            os.system('clear')
