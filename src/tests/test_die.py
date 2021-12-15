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
            face = self.die.face
            result[face] += 1

        for i in range(1, 7):
            self.assertGreater(result[i], 120)

    def test_constructor(self):
        for i in range(1, 7):
            die = Die(i)
            self.assertEqual(die.face, i)

    def test_freeze(self):
        target = self.die.face
        self.die.change_freeze_state()

        self.assertEqual(self.die.frozen, True)

        for _ in range(10):
            self.die.throw()
            self.assertEqual(self.die.face, target)

    def test_comparison(self):
        d_1 = Die(1)
        d_2 = Die(2)
        d_3 = Die(2)

        self.assertEqual(d_1 < d_2, True)
        self.assertEqual(d_1 > d_2, False)
        self.assertEqual(d_1 == d_2, False)
        self.assertEqual(d_2 == d_3, True)
