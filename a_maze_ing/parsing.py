from typing import Tuple, Optional
from pydantic import BaseModel, Field, validator, ValidationError
from a_maze_ing.Coordinates import Coordinates


class MazeConfig(BaseModel):
    WIDTH: int = Field(..., ge=9, description="Maze width (>= 9)")
    HEIGHT: int = Field(..., ge=7, description="Maze height (>= 7)")
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    OUTPUT_FILE: str = Field("output_maze.txt", description="Output filename")
    PERFECT: bool = False

    @validator("ENTRY", "EXIT")
    def validate_coordinates(cls, coord, values, field):
        if len(coord) != 2:
            raise ValueError(f"{field.name} must be (x, y) tuple")
        
        w = values.get("WIDTH")
        h = values.get("HEIGHT")
        if w is not None and h is not None:
            x, y = coord
            if not (0 <= x < w) or not (0 <= y < h):
                raise ValueError(f"{field.name} {coord} out of limits {w}x{h}")
            if coord in Coordinates.f4ty_2wo_block(w, h):
                raise ValueError(f"{field.name} cannot be in the 42-block")
        
        return coord

    @validator("EXIT")
    def valid_exit_entry_diff(cls, exit_coord, values):
        entry_coord = values.get("ENTRY")
        if entry_coord is not None and exit_coord == entry_coord:
            raise ValueError("ENTRY and EXIT must be different")
        return exit_coord

    @validator("OUTPUT_FILE")
    def valid_output_file(cls, v):
        if v.strip() in {".", "..", "./", "../", "/"} or not v.strip():
            raise ValueError("OUTPUT_FILE must be a valid filename")
        return v


def parsing_config_file(filepath: str) -> Optional[MazeConfig]:
    config: dict = {}
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid line (missing '='): {line}")
                
                key, value = map(str.strip, line.split("=", 1))
                key = key.upper()

                if key in {"WIDTH", "HEIGHT"}:
                    value = int(value)
                elif key in {"ENTRY", "EXIT"}:
                    value = tuple(map(int, value.split(",")))
                elif key == "PERFECT":
                    value = value.lower() == "true"

                config[key] = value

        return MazeConfig(**config)

    except (FileNotFoundError, PermissionError) as e:
        print(f"File error: {e}")
    except (ValueError, ValidationError) as e:
        print(f"Configuration error:\n{e}")

    return None


if __name__ == "__main__":
    config = parsing_config_file("config.txt")
    print(config)
