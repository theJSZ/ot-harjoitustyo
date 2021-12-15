import unittest
from entities.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Jussi")

    def test_constructor(self):
        self.assertEqual(self.player.name, "Jussi")

    def test_mark_upstairs(self):
        self.player.mark_upstairs("Kakkoset", 0)
        self.assertEqual(self.player.results["Kakkoset"], 'x')
        self.assertEqual(self.player.results["Välisumma"], 0)
        self.assertEqual(self.player.results["Yhteensä"], 0)

        self.player.mark_upstairs("Ykköset", 1)
        self.assertEqual(self.player.results["Ykköset"], 1)
        self.assertEqual(self.player.results["Välisumma"], 1)
        self.assertEqual(self.player.results["Yhteensä"], 1)

        self.player.mark_upstairs("Kolmoset", 6)
        self.assertEqual(self.player.results["Ykköset"], 1)
        self.assertEqual(self.player.results["Välisumma"], 7)
        self.assertEqual(self.player.results["Yhteensä"], 7)

        self.player.mark_upstairs("Kuutoset", 30)
        self.player.mark_upstairs("Viitoset", 25)
        self.player.mark_upstairs("Neloset", 20)
        self.assertEqual(self.player.results["Välisumma"], 132)
        self.assertEqual(self.player.results["Yhteensä"], 132)

    def test_mark_downstairs(self):
        self.player.mark_downstairs("2 paria", 0)
        self.assertEqual(self.player.results["2 paria"], 'x')
        self.assertEqual(self.player.results["Välisumma"], 0)
        self.assertEqual(self.player.results["Yhteensä"], 0)


        self.player.mark_downstairs("1 pari", 12)
        self.assertEqual(self.player.results["1 pari"], 12)
        self.assertEqual(self.player.results["Välisumma"], 0)
        self.assertEqual(self.player.results["Yhteensä"], 12)

        self.player.mark_downstairs("Yatzy", 50)
        self.assertEqual(self.player.results["Yatzy"], 50)
        self.assertEqual(self.player.results["Välisumma"], 0)
        self.assertEqual(self.player.results["Yhteensä"], 62)
