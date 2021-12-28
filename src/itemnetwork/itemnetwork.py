from __future__ import annotations

import typing
from collections import Counter
from typing import Tuple, Dict, List, Hashable, ItemsView

HashType = typing.NewType('hash', int)


def xor_hash(a: Hashable, b: Hashable) -> HashType:
    return HashType(hash(a) ^ hash(b))


def ext_hash(a: Hashable, b: Hashable) -> HashType:
    return HashType(hash((a, b)))


class LinkedNetwork:
    """
        Usage::\n
        | ...my_network = LinkedNetwork()
        | ...my_network.add_link('a', 'b')
        | ...my_network.add_multiple_links([('a', 'b'), ('b', 'c'), ('c', 'd')])
        | ...# print items
        | ...my_network.print_links()
        | >>> a b 2
        | >>> b c 1
        | >>> c d 1
    """
    _items: Dict[Hashable, list[Link]]
    _links: Dict[HashType, Link]

    def __init__(self, keep_order=False, ignore_key_equality_error=False):
        """
        :param ignore_key_equality_error: if true all Links where a==b will be silently dropped before being added
        """
        self._items = dict()
        self._links = dict()
        if not ignore_key_equality_error:
            self.key_equality_check = lambda a, b: False

        if keep_order:
            self._hash_method = ext_hash
        else:
            self._hash_method = xor_hash

    def add_link(self, a: Hashable, b: Hashable, count=1):
        """
        Add a link between 2 items\n
        :param a: any hashable item
        :param b: any hashable item
        :param count: number of links between a & b to add
        :return:
        """
        hash_view = xor_hash(a, b)
        try:
            self._links[hash_view](count)
        except KeyError:
            if self.key_equality_check(a, b):
                return
            link_item = Link(a, b, count=count)
            self._links[hash_view] = link_item
            self._add_item_(a, link_item)
            self._add_item_(b, link_item)

    def _add_item_(self, item: Hashable, link):
        """ update _item to include its Link"""
        try:
            self._items[item].append(link)
        except  KeyError:
            self._items[item] = [link]

    def get_link(self, a: Hashable, b: Hashable) -> Link | None:
        """ Return the link that represents **a** and **b** or None"""
        try:
            return self._links[xor_hash(a, b)]
        except KeyError:
            return None

    def add_multiple_links(self, links: typing.Iterable[Tuple[Hashable, Hashable]]):
        """
        possibly faster than add_link if large number of duplicate links are present this uses `Counter <Counter>`_ \n
        :param links: list of a,b tuples
        """
        for a, c in Counter(links).items():
            self.add_link(*a, count=c)

    def __iter__(self):
        return self._links.values().__iter__()

    def link_items(self) -> ItemsView[Hashable, Link]:
        return self._links.items()

    def list_links(self) -> List[Link]:
        """ :return: all links as a list"""
        return list(self._links.values())

    def print_links(self):
        """prints all current links in the format: " **a b 4** " """
        for val in self._links.values():
            print(val)

    @staticmethod
    def key_equality_check(a: Hashable, b: Hashable) -> bool:
        """key_equality_check(**a**, **b**) equal to hash(**a**) == hash(**b**)\n\n:return: True if hashes match"""
        return hash(a) == hash(b)

    def get_links_containing(self, item: Hashable) -> List[Link]:
        """
        return a list of Link items which contain item in either position \n
        :param item: hashable object
        :return: list of Link objects
        """
        _hash_ = hash(item)
        return [i for i in self._links.values() if i.has_hash(_hash_)]

    def get_item_link_count_dict(self) -> dict[Hashable, Tuple[int, int]]:
        """:return: dict of item: (count, sum)"""
        return {item: (len(links), sum(links)) for item, links in self._items.items()}


class Link:
    _a: Hashable
    _b: Hashable
    _hash = HashType
    count: int

    def __init__(self, a: Hashable, b: Hashable, count: int = 1):
        """
        :param a: any hashable item
        :param b: any hashable item
        :param count: number of items to add
        """
        self._a = a
        self._b = b
        self._hash = xor_hash(a, b)
        self.count = count

        if self._hash == 0:
            raise ValueError('Hashes for a and b must not match', a, b)

    def __call__(self, count: int = 1):
        """ Increment counter \n
        :param count: amount to increment count by """
        self.count += count

    def __hash__(self) -> int:
        """ xor of the hash will ignore order of _a and _b"""
        return self._hash

    def __eq__(self, other: Link) -> bool:
        return self._a == other._a and self._b == other._b and self.count == other.count

    def __gt__(self, other: Link) -> bool:
        return self.count > other.count

    def __str__(self) -> str:
        """format: "**a b 4**" """
        return f'{self._a} {self._b} {self.count}'

    def has_hash(self, _hash_: int) -> bool:
        """
        :param _hash_: hash to check for equality against **_a** and **_b**
        :return:
        """
        return _hash_ == hash(self._a) or _hash_ == hash(self._b)

    def __contains__(self, item: Hashable) -> bool:
        """check if **item** is a part of the link"""
        return self.has_hash(hash(item))

    def __getitem__(self, item: int):
        """
        :param item: 0 or 1 to access items
        :return: Hashable
        """
        if item == 0:
            return self._a
        elif item == 1:
            return self._b
        else:
            raise IndexError("Index out of range 0,1:", item)

    def __add__(self, other):
        return self.count + other

    __radd__ = __add__

    def a(self) -> Hashable:
        return self._a

    def b(self) -> Hashable:
        return self._b

    def hash(self) -> HashType:
        return self._hash
