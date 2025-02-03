from abc import abstractmethod
from typing import Any, Callable, Protocol, Self, TypeVar

T = TypeVar('T')
U = TypeVar('U')

def closest_matches(needles: list[T], haystack: list[U], dist=Callable[[T, U], Any]) -> list[U]:
    if len(haystack) < len(needles):
        raise ValueError('Not enough values to match')

    remaining = dict(enumerate(haystack))
    matches: list[U] = []

    for needle in needles:
        i, matched = min(remaining.items(), key=lambda v: dist(needle, v[1]))
        matches.append(matched)
        del remaining[i]

    return matches
