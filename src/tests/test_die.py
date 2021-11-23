import unittest
from die import Die

class TestDie(unittest.TestCase):
    def setUp(self):
        self.d = Die()

    def test_die(self):
        """Throws die 1000 times then checks 
every result appeared at least 120 times
        """
        result = [0 for _ in range(7)]
        for _ in range(1000):
            self.d.throw()
            face = self.d.getFace()
            result[face] += 1
        
        for i in range(1, 7):
            self.assertGreater(result[i], 120)
