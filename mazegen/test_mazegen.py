from generator import MazeGenerator

maze = MazeGenerator(8, 8, (0, 0), (7, 7))
maze.generate()

path = maze.bfs_solver(maze.grid, maze.entry, maze.exit)
print(path)
maze.draw_maze_with_path(maze.grid, path, maze.entry)
