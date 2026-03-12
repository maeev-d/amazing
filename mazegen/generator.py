import random
from typing import Tuple

N = 1 << 0  # 0001
E = 1 << 1  # 0010
S = 1 << 2  # 0100
W = 1 << 3  # 1000

# format: direction : (dy, dx, wall_bit)
DIRS = {
    "N": (0, -1, 1),
    "E": (1, 0, 2),
    "S": (0, 1, 4),
    "W": (-1, 0, 8),
}


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool = True,
        seed: int | None = None,
    ):
        # ---- Type validation ----
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("[ERROR]: width and height must be integers.")

        if (
            not isinstance(entry, tuple)
            or not isinstance(exit, tuple)
            or len(entry) != 2
            or len(exit) != 2
        ):
            raise TypeError("[ERROR]: entry and exit must be tuples (x, y).")

        if not all(isinstance(v, int) for v in (*entry, *exit)):
            raise TypeError(
                "[ERROR]: entry and exit coordinates must be integers.")

        # ---- Logical validation ----
        if width < 8 or height < 6:
            raise ValueError("[ERROR]: Maze dimensions too small.")

        if entry == exit:
            raise ValueError(
                "[ERROR]: entry and exit should not be the same point."
            )

        if not self._is_inside_static(width, height, *entry):
            raise ValueError("[ERROR]: Invalid entry point.")

        if not self._is_inside_static(width, height, *exit):
            raise ValueError("[ERROR]: Invalid exit point.")

        # ---- Assign attributes AFTER validation ----
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

        # Isolated random generator (no global seed pollution)
        self._rng = random.Random(seed)

        # Initialize grid (all walls closed: 0b1111)
        self.grid: list[list[int]] = [
            [0b1111 for _ in range(width)]
            for _ in range(height)
        ]

    @staticmethod
    def _is_inside_static(
        width: int, height: int, x: int, y: int
    ) -> bool:
        return 0 <= x < width and 0 <= y < height

    def generate(self) -> None:
        visited: list[list[bool]] = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]
        stack: list[tuple[int, int]] = []
        curent = self.entry
        x, y = curent
        visited[y][x] = True
        stack.append(curent)
        while len(stack):
            curent = stack.pop()
            neighbors = self._get_unvisited_neighbors(*curent, visited)
            if neighbors:
                stack.append(curent)
                nx, ny = self._rng.choice(neighbors)
                self._remove_wall(*curent, nx, ny)
                visited[ny][nx] = True
                stack.append((nx, ny))

    @staticmethod
    def _get_unvisited_neighbors(
        x: int,
        y: int,
        visited: list[list[bool]]
    ) -> list[tuple[int, int]]:
        width = len(visited[0])
        height = len(visited)
        neighbors: list[tuple[int, int]] = []

        if x + 1 < width and not visited[y][x + 1]:
            neighbors.append((x + 1, y))

        if x - 1 >= 0 and not visited[y][x - 1]:
            neighbors.append((x - 1, y))

        if y + 1 < height and not visited[y + 1][x]:
            neighbors.append((x, y + 1))

        if y - 1 >= 0 and not visited[y - 1][x]:
            neighbors.append((x, y - 1))

        return neighbors

    def _remove_wall(
        self,
        x: int,
        y: int,
        nx: int,
        ny: int
    ) -> None:

        if nx == x and ny == y - 1:  # North
            self.grid[y][x] &= ~N
            self.grid[ny][nx] &= ~S

        elif nx == x + 1 and ny == y:  # East
            self.grid[y][x] &= ~E
            self.grid[ny][nx] &= ~W

        elif nx == x and ny == y + 1:  # South
            self.grid[y][x] &= ~S
            self.grid[ny][nx] &= ~N

        elif nx == x - 1 and ny == y:  # West
            self.grid[y][x] &= ~W
            self.grid[ny][nx] &= ~E

    def bfs_solver(
        self,
        maze: list[list[int]],
        entry: Tuple[int, int],
        exit: Tuple[int, int]
    ) -> list[tuple[int, int]]:
        stack = [entry]
        parent = {}
        visited: list[list[bool]] = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]
        x, y = entry
        visited[y][x] = True
        while stack:
            curent = stack.pop()

            if curent == exit:
                break

            for d, nx, ny in self._neighbors(self.grid, *curent):
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    parent[(nx, ny)] = (curent, d)
                    stack.append((nx, ny))
        return self._build_path(entry, exit, parent)

    @staticmethod
    def _neighbors(
        maze: list[list[int]],
        x: int,
        y: int
    ) -> tuple[str, int, int]:
        w = len(maze[0])
        h = len(maze)
        for d, (dx, dy, bit) in DIRS.items():
            if not (maze[y][x] & bit):  # wall open
                ny = y + dy
                nx = x + dx
                if 0 <= ny < h and 0 <= nx < w:
                    yield d, nx, ny

    @staticmethod
    def _build_path(
        entry: tuple[int, int],
        exit: tuple[int, int],
        parent: dict
    ) -> str:
        path = []
        curent = exit

        while curent != entry:
            prev, d = parent[curent]
            path.append(d)
            curent = prev

        return "".join((reversed(path)))

    def draw_maze_with_path(self, maze: list[list[int]], path: str,
                            entry: tuple[int, int]) -> None:
        h = len(maze)
        w = len(maze[0])

        # compute path cells
        x, y = entry
        path_cells = {(x, y)}

        moves = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }

        for step in path:
            dx, dy = moves[step]
            x += dx
            y += dy
            path_cells.add((x, y))

        # top border
        print("+" + "---+" * w)

        for y in range(h):
            line1 = "|"
            line2 = "+"

            for x in range(w):
                cell = maze[y][x]

                # draw path
                if (x, y) in path_cells:
                    line1 += " . "
                else:
                    line1 += "   "

                # east wall
                if cell & 2:
                    line1 += "|"
                else:
                    line1 += " "

                # south wall
                if cell & 4:
                    line2 += "---+"
                else:
                    line2 += "   +"

            print(line1)
            print(line2)
