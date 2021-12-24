import random
import unittest

from src.itemnetwork import _container

random.seed(0)
ab_ = [(random.randint(0, 9), random.randint(0, 9)) for _ in range(50)]
ab_ = [(a, b) if a != b else (1,2) for a, b in ab_]


class MyTestCase(unittest.TestCase):
    def test_xor_hash(self):
        a = "somestring"
        b = "otherstring"
        self.assertEqual(_container.xor_hash(a, b),
                         _container.xor_hash(b, a),
                         "Equality check for xor_hash over strings")

    def test_Container_creation(self):
        container_simple = _container.Container()
        for a, b in ab_:
            container_simple.add_link(a, b)
        container_multiple = _container.Container()
        container_multiple.add_multiple_links(ab_)
        self.assertEqual(container_simple.list_links(),
                         container_multiple.list_links(),
                         "check both Container.add_link and Container.add_multiple_links return the same values")


if __name__ == '__main__':
    unittest.main()
