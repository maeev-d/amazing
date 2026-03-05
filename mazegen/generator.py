import random
from typing import Tuple


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
            raise TypeError("[ERROR]: entry and exit coordinates must be integers.")

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

    def generate(self):
        curent = self.entry
        visited: list[list[bool]] = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]
        stack: list[tuple[int, int]] = []
        x, y = curent
        visited[y][x] = True
        stack.append(curent)
        while len(stack):
            curent = stack.pop()
            neighbors = self._get_unvisited_neighbors(*curent, visited)
            if neighbors:
                stack.append(curent)
                nx, ny = self._rng.choice(neighbors)
                #unvisited_neighb = choose_unvisited(curent, visited)
                _remove_wall(*curent, nx, ny)
                #x, y = unvisited_neighb
                visited[ny][nx] = True
                stack.append((nx, ny))
    def _get_unvisited_neighbors(
        self,
        x: int,
        y: int,
        visited: list[list[bool]]
    ) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
 
        if x + 1 < self.width and not visited[y][x + 1]:
            neighbors.append((x + 1, y))

        if x - 1 >= 0 and not visited[y][x - 1]:
            neighbors.append((x - 1, y))

        if y + 1 < self.height and not visited[y + 1][x]:
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
        pass
