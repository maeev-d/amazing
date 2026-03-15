# parsing.py
from typing import Tuple, Optional
from pydantic import BaseModel, Field, validator, root_validator, ValidationError
from drawing import AsciiRenderer


class MazeConfig(BaseModel):
    WIDTH: int = Field(..., ge=9, description="Maze width (>=9)")
    HEIGHT: int = Field(..., ge=7, description="Maze height (>=7)")
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    PERFECT: bool = False  # <-- default False

    @validator("ENTRY")
    def validate_entry(cls, coord, values):
        w = values.get("WIDTH")
        h = values.get("HEIGHT")
        if len(coord) != 2:
            raise ValueError("ENTRY must be (x, y)")
        if w is not None and h is not None:
            x, y = coord
            if not (0 <= x < w and 0 <= y < h):
                raise ValueError(f"ENTRY {coord} outside maze {w}x{h}")
            if coord in AsciiRenderer.cells_of_42(w, h):
                raise ValueError("ENTRY cannot be in the 42-block")
        return coord

    @validator("EXIT")
    def validate_exit(cls, coord, values):
        w = values.get("WIDTH")
        h = values.get("HEIGHT")
        if len(coord) != 2:
            raise ValueError("EXIT must be (x, y)")
        if w is not None and h is not None:
            x, y = coord
            if not (0 <= x < w and 0 <= y < h):
                raise ValueError(f"EXIT {coord} outside maze {w}x{h}")
            if coord in AsciiRenderer.cells_of_42(w, h):
                raise ValueError("EXIT cannot be in the 42-block")
        return coord

    @root_validator
    def validate_entry_exit_different(cls, values):
        entry = values.get("ENTRY")
        exit_ = values.get("EXIT")
        if entry and exit_ and entry == exit_:
            raise ValueError("ENTRY and EXIT must be different")
        return values


def parsing_config_file(filepath: str) -> Optional[MazeConfig]:
    config: dict = {}

    try:
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid line: {line}")

                key, value = map(str.strip, line.split("=", 1))
                key = key.upper()

                if key in {"WIDTH", "HEIGHT"}:
                    value = int(value)
                elif key in {"ENTRY", "EXIT"}:
                    x, y = map(int, value.split(","))
                    value = (x, y)
                elif key == "PERFECT":
                    value = value.lower() in {"true", "1", "yes"}
                
                config[key] = value

        return MazeConfig(**config)

    except FileNotFoundError:
        print("Config file not found")
        exit(1)
    except PermissionError:
        print("Permission denied while reading file")
        exit(1)
    except (ValueError, ValidationError) as e:
        print(f"Configuration error:\n{e}")
        exit(1)

    return None

