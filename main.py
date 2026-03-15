# main.py
import os
import time
from generator import MazeGenerator
from drawing import AsciiRenderer
from parsing import parsing_config_file
from blessed import Terminal

# Load maze configuration
config = parsing_config_file("config.txt")

width = config.WIDTH
height = config.HEIGHT
entry = config.ENTRY
exit_ = config.EXIT
perfect = config.PERFECT

# Initialize terminal
term = Terminal()

# Initialize maze generator
maze = MazeGenerator(width, height, entry, exit_, perfect)
maze.generate()  # Apply the DFS maze generation

# Optional: solve maze for path (if needed)
path = maze.bfs_solver(maze.grid, entry, exit_)

# Initialize renderer
renderer = AsciiRenderer(maze, entry, exit_)

# Clear screen and show intro
os.system("clear")
if os.path.exists("intrro.txt"):
    with open("intrro.txt") as f:
        for line in f:
            print(term.red(line.strip()))
            time.sleep(0.05)
    os.system("clear")

# Render maze
print(term.yellow(renderer.render()))

# Optional: write output file (maze as text)
if hasattr(maze, "write_output_file"):
    maze.write_output_file("output_maze.txt")
