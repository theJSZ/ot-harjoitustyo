import unittest
from entities.die import Die

class TestDie(unittest.TestCase):
    def setUp(self):
        self.die = Die()

    def test_throw_randomness(self):
        """Heittää noppaa 1000 kertaa ja tarkistaa että
        jokainen tulos on saatu vähintään 120 kertaa
        """
        result = [0 for _ in range(7)]
        for _ in range(1000):
            self.die.throw()
            face = self.die.face
            result[face] += 1

        for i in range(1, 7):
            self.assertGreater(result[i], 120)

    def test_constructor(self):
        """Testaa että nopalle konstruktorissa
        annettu arvo on oikein
        """
        for i in range(1, 7):
            die = Die(i)
            self.assertEqual(die.face, i)

    def test_freeze(self):
        """Testaa että jäädytettyä noppaa
        ei voi heittää ja että status palautetaan oikein
        """
        self.assertEqual(self.die.frozen, False)
        self.assertEqual(self.die.get_freeze_state(), False)

        target = self.die.face
        self.die.change_freeze_state()

        self.assertEqual(self.die.frozen, True)
        self.assertEqual(self.die.get_freeze_state(), True)

        for _ in range(10):
            self.die.throw()
            self.assertEqual(self.die.face, target)

    def test_comparison(self):
        """Testaa että vertailuoperaattorit toimivat nopille
        """
        d_1 = Die(1)
        d_2 = Die(2)
        d_3 = Die(2)

        self.assertEqual(d_1 < d_2, True)
        self.assertEqual(d_1 > d_2, False)
        self.assertEqual(d_1 == d_2, False)
        self.assertEqual(d_2 == d_3, True)

    def test_set_get_position(self):
        self.die.set_position((10, 10))
        self.assertEqual(self.die.get_position(), (10, 10))

    def test_in_area(self):
        self.die.set_position((10, 10))
        self.assertEqual(self.die.in_area((100, 100)), False)
        self.assertEqual(self.die.in_area((50, 50)), True)
        self.assertEqual(self.die.in_area((100, 50)), False)
        self.assertEqual(self.die.in_area((50, 100)), False)



