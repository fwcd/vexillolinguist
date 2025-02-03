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
        return Color.from_int(int(hex, base=16))
    
    def distance_to(self, other: Self) -> float:
        return math.sqrt((self.red - other.red) ** 2 + (self.green - other.green) ** 2 + (self.blue - other.blue) ** 2)
