import unittest
from entities.die import Die

class TestDie(unittest.TestCase):
    def setUp(self):
        self.die = Die()

    def test_throw_randomness(self):
        """Throws die 1000 times then checks
every result appeared at least 120 times
        """
        result = [0 for _ in range(7)]
        for _ in range(1000):
            self.die.throw()
            face = self.die.get_face()
            result[face] += 1

        for i in range(1, 7):
            self.assertGreater(result[i], 120)

    def test_constructor(self):
        for i in range(1, 7):
            die = Die(i)
            self.assertEqual(die.get_face(), i)

    def test_freeze(self):
        target = self.die.get_face()
        self.die.change_freeze_state()

        self.assertEqual(self.die.get_freeze_state(), True)

        for i in range(10):
            self.die.throw()
            self.assertEqual(self.die.get_face(), target)

    def test_comparison(self):
        d1 = Die(1)
        d2 = Die(2)
        d3 = Die(2)

        self.assertEqual(d1 < d2, True)
        self.assertEqual(d1 > d2, False)
        self.assertEqual(d1 == d2, False)
        self.assertEqual(d2 == d3, True)

