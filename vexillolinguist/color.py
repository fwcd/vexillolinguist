from dataclasses import dataclass
from typing import Self

import math

@dataclass
class Color:
    red: float
    green: float
    blue: float

    @staticmethod
    def from_ints(red: int, green: int, blue: int) -> Self:
        return Color(
            red=red / 255.0,
            green=green / 255.0,
            blue=blue / 255.0,
        )

    @staticmethod
    def from_int(rgb: int) -> Self:
        return Color.from_ints(
            red=(rgb >> 16) & 0xFF,
            green=(rgb >> 8) & 0xFF,
            blue=rgb & 0xFF,
        )

    @staticmethod
    def from_hex(hex: str) -> Self:
        match len(hex):
            case 3:
                return Color.from_hex(''.join(2 * c for c in hex))
            case 6:
                return Color.from_int(int(hex, base=16))
            case _:
                raise ValueError(f'Hex value must be of length 3 or 6: {hex}')
    
    def mix(self, other: Self) -> Self:
        return Color(
            red=(self.red + other.red) / 2,
            green=(self.green + other.green) / 2,
            blue=(self.blue + other.blue) / 2,
        )

    def distance_to(self, other: Self) -> float:
        return math.sqrt((self.red - other.red) ** 2 + (self.green - other.green) ** 2 + (self.blue - other.blue) ** 2)

COLORS = {
    'red': Color(1, 0, 0),
    'green': Color(0, 1, 0),
    'blue': Color(0, 0, 1),
    'yellow': Color(1, 1, 0),
    'orange': Color(1, 0.5, 0),
    'magenta': Color(1, 0, 1),
    'violet': Color(0.5, 0, 1),
    'cyan': Color(0, 1, 1),
    'black': Color(0, 0, 0),
    'gray': Color(0.5, 0.5, 0.5),
    'white': Color(1, 1, 1),
}

def parse_color(raw: str) -> Color:
    if raw.startswith('#'):
        return Color.from_hex(raw[1:])
    elif c := COLORS.get(raw):
        return c
    else:
        raise ValueError(f'Could not parse color: {raw}')
