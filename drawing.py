# drawing.py
from typing import Tuple, Optional, Set, Any, List


class AsciiRenderer:
    """
    Responsible for drawing a maze in ASCII (now with block characters).
    """

    def __init__(self, maze, entry: Tuple[int, int], exit: Tuple[int, int]):
        self.maze = maze
        self.entry = entry
        self.exit = exit

    @staticmethod
    def cells_of_42(wd: int, ht: int) -> List[Tuple[int, int]]:
        cx = wd // 2
        cy = ht // 2

        cells = [
            (cx + 2, cy - 2), (cx + 1, cy - 2), (cx + 3, cy - 2),
            (cx + 3, cy - 1), (cx + 3, cy), (cx + 2, cy),
            (cx + 1, cy), (cx + 1, cy + 1), (cx + 1, cy + 2),
            (cx + 2, cy + 2), (cx + 3, cy + 2),

            (cx - 3, cy - 2), (cx - 3, cy - 1), (cx - 3, cy),
            (cx - 2, cy), (cx - 1, cy),
            (cx - 1, cy + 1), (cx - 1, cy + 2)
        ]

        return [(x, y) for x, y in cells if 0 <= x < wd and 0 <= y < ht]

    def render(
        self,
        player_pos: Optional[Tuple[int, int]] = None,
        visited_trail: Optional[List[Any]] = None,
        path: Optional[Set[Any]] = None,
        show: bool = True
    ) -> str:

        BLOCK = "█"
        width = self.maze.width
        height = self.maze.height
        h_seg = BLOCK * 3

        output = ""

        output += BLOCK + (h_seg + BLOCK) * (width - 1) + h_seg + BLOCK + "\n"

        cell42 = set(self.cells_of_42(width, height))

        for y in range(height):

            row_str = BLOCK

            for x in range(width):

                if (x, y) == self.entry:
                    body = " S "

                elif (x, y) == self.exit or (x, y) in cell42:
                    body = " Dm"

                else:
                    body = "   "

                cell = self.maze.get_cell(x, y)

                wall_char = BLOCK if (cell and cell.walls["E"]) or x == width - 1 else " "

                row_str += body + wall_char

            output += row_str + "\n"

            if y < height - 1:

                row_str = BLOCK

                for x in range(width):

                    cell = self.maze.get_cell(x, y)

                    wall = h_seg if cell and cell.walls["S"] else "   "
                    joint = BLOCK

                    row_str += wall + joint

                output += row_str + "\n"

        output += BLOCK + (h_seg + BLOCK) * (width - 1) + h_seg + BLOCK + "\n"


        return output