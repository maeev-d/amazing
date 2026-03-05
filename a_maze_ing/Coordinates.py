from typing import List, Tuple


class Coordinates:
    @staticmethod
    def f4ty_2wo_block(width: int, height: int) -> List[Tuple[int, int]]:
        cx, cy = width // 2, height // 2
        cells = []

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cells.append((cx + dx, cy + dy))
        for i in range(1, 3):
            cells.append((cx + i, cy))
            cells.append((cx - i, cy))
            cells.append((cx, cy + i))
            cells.append((cx, cy - i))

        return cells
