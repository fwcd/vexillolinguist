from abc import abstractmethod
from typing import Any, Callable, Protocol, Self, TypeVar

T = TypeVar('T')
U = TypeVar('U')

def filter_unambiguous(values: list[T], keys: Callable[[T], list[U]]) -> list[T]:
    values_by_key: dict[U, list[T]] = {}

    for value in values:
        for key in keys(value):
            values_by_key[key] = values_by_key.get(key, []) + [value]
    
    return [value for value in values if all(len(values_by_key[key]) == 1 for key in keys(value))]

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
