from mazegen.generator import MazeGenerator
from parsing import parsing_config_file

parsed = parsing_config_file("config.txt")
w = parsed.WIDTH
h = parsed.HEIGHT
s = parsed.ENTRY
e = parsed.EXIT

maze = MazeGenerator(w, h, s, e)
maze.generate()


path = maze.bfs_solver(maze.grid, maze.entry, maze.exit)
print(path)
maze.draw_maze_with_path(maze.grid, path, maze.entry)
