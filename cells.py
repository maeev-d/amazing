# cells.py

class Cell:
    """
    Represents a single cell in the maze.
    All walls are initially closed.
    """
    def __init__(self) -> None:
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.visited = False
        self.blocked = False