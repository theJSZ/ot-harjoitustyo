import unittest
from player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pass

    def test_constructor(self):
        player = Player("Jussi")
        self.assertEqual(player.getName(), "Jussi")