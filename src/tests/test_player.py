import unittest
from entities.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Jussi")

    def test_constructor(self):
        self.assertEqual(self.player.get_name(), "Jussi")

    def test_mark_upstairs(self):
        self.player.mark_upstairs(2, 0)
        self.assertEqual(self.player.get_results()["Kakkoset"], 'x')
        self.assertEqual(self.player.get_results()["Välisumma"], 0)
        self.assertEqual(self.player.get_results()["Yhteensä"], 0)

        self.player.mark_upstairs(1, 1)
        self.assertEqual(self.player.get_results()["Ykköset"], 1)
        self.assertEqual(self.player.get_results()["Välisumma"], 1)
        self.assertEqual(self.player.get_results()["Yhteensä"], 1)

        self.player.mark_upstairs(1, 5)
        self.assertEqual(self.player.get_results()["Ykköset"], 1)
        self.assertEqual(self.player.get_results()["Välisumma"], 1)
        self.assertEqual(self.player.get_results()["Yhteensä"], 1)

        self.player.mark_upstairs(6, 30)
        self.player.mark_upstairs(5, 25)
        self.player.mark_upstairs(4, 20)
        self.assertEqual(self.player.get_results()["Välisumma"], 126)
        self.assertEqual(self.player.get_results()["Yhteensä"], 126)

    def test_mark_downstairs(self):
        self.player.mark_downstairs("2 paria", 0)
        self.assertEqual(self.player.get_results()["2 paria"], 'x')
        self.assertEqual(self.player.get_results()["Välisumma"], 0)
        self.assertEqual(self.player.get_results()["Yhteensä"], 0)


        self.player.mark_downstairs("1 pari", 12)
        self.assertEqual(self.player.get_results()["1 pari"], 12)
        self.assertEqual(self.player.get_results()["Välisumma"], 0)
        self.assertEqual(self.player.get_results()["Yhteensä"], 12)

        self.player.mark_downstairs("Yatzy", 50)
        self.assertEqual(self.player.get_results()["Yatzy"], 50)
        self.assertEqual(self.player.get_results()["Välisumma"], 0)
        self.assertEqual(self.player.get_results()["Yhteensä"], 62)

        self.player.mark_downstairs("Yatzy", 100)
        self.assertEqual(self.player.get_results()["Yatzy"], 50)
        self.assertEqual(self.player.get_results()["Välisumma"], 0)
        self.assertEqual(self.player.get_results()["Yhteensä"], 62)
