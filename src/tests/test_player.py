import unittest
from entities.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("JSZ")

    def test_constructor(self):
        """Testaa että pelaajalle annettu nimi on oikein
        """
        self.assertEqual(self.player.name, "JSZ")

    def test_played(self):
        self.assertEqual(self.player.played(), False)
        self.player.mark_result("Ykköset", 1)
        self.assertEqual(self.player.played(), True)

    def test_mark_upstairs(self):
        """Testaa että yläkertaan merkatut
        tulokset menevät oikein
        """
        self.player.mark_result("Kakkoset", 0)
        self.assertEqual(self.player.results["Kakkoset"], 'x')
        self.assertEqual(self.player.results["Välisumma"], 0)
        self.assertEqual(self.player.results["Yhteensä"], 0)

        self.player.mark_result("Ykköset", 1)
        self.assertEqual(self.player.results["Ykköset"], 1)
        self.assertEqual(self.player.results["Välisumma"], 1)
        self.assertEqual(self.player.results["Yhteensä"], 1)

        self.player.mark_result("Kolmoset", 6)
        self.assertEqual(self.player.results["Ykköset"], 1)
        self.assertEqual(self.player.results["Välisumma"], 7)
        self.assertEqual(self.player.results["Yhteensä"], 7)

        self.player.mark_result("Kuutoset", 30)
        self.player.mark_result("Viitoset", 25)
        self.player.mark_result("Neloset", 20)
        self.assertEqual(self.player.results["Välisumma"], 132)
        self.assertEqual(self.player.results["Yhteensä"], 132)

    def test_mark_downstairs(self):
        """Testaa että alakertaan merkatut tulokset menevät oikein
        """
        self.player.mark_result("2 paria", 0)
        self.assertEqual(self.player.results["2 paria"], 'x')
        self.assertEqual(self.player.results["Välisumma"], 0)
        self.assertEqual(self.player.results["Yhteensä"], 0)


        self.player.mark_result("1 pari", 12)
        self.assertEqual(self.player.results["1 pari"], 12)
        self.assertEqual(self.player.results["Välisumma"], 0)
        self.assertEqual(self.player.results["Yhteensä"], 12)

        self.player.mark_result("Yatzy", 50)
        self.assertEqual(self.player.results["Yatzy"], 50)
        self.assertEqual(self.player.results["Välisumma"], 0)
        self.assertEqual(self.player.results["Yhteensä"], 62)
