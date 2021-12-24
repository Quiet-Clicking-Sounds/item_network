from __future__ import annotations

import typing
from collections import Counter

from typing import Tuple, Dict, List, Hashable


HashType = typing.NewType('hash', int)


def xor_hash(a: Hashable, b: Hashable) -> HashType:
    return HashType(hash(a) ^ hash(b))


class Container:
    def __init__(self):
        self._items: Dict[HashType, Hashable] = dict()
        self._links: Dict[HashType, Link] = dict()

    def add_link(self, a: Hashable, b: Hashable, count=1):
        """
        Add a link between 2 items\n
        :param a: any hashable item
        :param b: any hashable item
        :param count: default 1 int to increment by
        :return:
        """
        hash_view = xor_hash(a, b)
        try:
            self._links[hash_view] + count
        except KeyError:
            self._links[hash_view] = Link(a, b, count=count)

    def add_multiple_links(self, links: typing.Iterable[Tuple[Hashable, Hashable]]):
        """
        possibly faster than add_link if large number of duplicate links are present this uses `Counter <Counter>`_ \n
        :param links: list of a,b tuples
        """
        for a, c in Counter(links).items():
            self.add_link(*a, count=c)

    def __iter__(self):
        return self._links.values().__iter__()

    def list_links(self) -> List[Link]:
        return list(self._links.values())


class Link:
    _a: Hashable
    _b: Hashable

    def __init__(self, a: Hashable, b: Hashable, count:int=1):
        """
        :param a: any hashable item
        :param b: any hashable item
        :param count: number of items to add
        """
        if a == b:
            raise KeyError('a must not be equal to b:', a, b)
        self._a = a
        self._b = b
        self._hash = xor_hash(a, b)
        self.count = count

    def __call__(self):
        self.count += 1

    def __add__(self, count):
        self.count += count

    def __hash__(self):
        """ xor of the hash will ignore order of _a and _b"""
        return self._hash

    def __eq__(self, other: Link):
        return self._a == other._a and self._b == other._b and self.count == other.count

    def __str__(self):
        return f'{self._a} - {self.count} - {self._b}'
