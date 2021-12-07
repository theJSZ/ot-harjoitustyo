import unittest
from entities.player import Player
from entities.die import Die

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
        self.assertEqual(self.player.get_results()["Välisumma"], 76)
        self.assertEqual(self.player.get_results()["Bonus"], 50)
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

    # def test_mark_pair(self):
    #     self.dice[0] = Die(6)
    #     self.dice[1] = Die(6)
    #     self.player.mark_pair(self.dice)
    #     self.assertEqual(self.player.get_results()["1 pari"], 12)

    # def test_mark_two_pair(self):
    #     self.dice[0] = Die(6)
    #     self.dice[1] = Die(6)
    #     self.dice[2] = Die(5)
    #     self.dice[3] = Die(5)
    #     self.player.mark_two_pair(self.dice)
    #     self.assertEqual(self.player.get_results()["2 paria"], 22)

    # def test_mark_three_of_a_kind(self):
    #     self.dice[0] = Die(6)
    #     self.dice[1] = Die(6)
    #     self.dice[2] = Die(6)
    #     self.player.mark_three_kind(self.dice)
    #     self.assertEqual(self.player.get_results()["3 samaa"], 18)
        
    # def test_mark_four_of_a_kind(self):
    #     self.dice[0] = Die(6)
    #     self.dice[1] = Die(6)
    #     self.dice[2] = Die(6)
    #     self.dice[3] = Die(6)
    #     self.player.mark_four_kind(self.dice)
    #     self.assertEqual(self.player.get_results()["4 samaa"], 24)

    # def test_mark_small_straight(self):
    #     self.dice[0] = Die(1)
    #     self.dice[1] = Die(2)
    #     self.dice[2] = Die(4)
    #     self.dice[3] = Die(5)
    #     self.dice[4] = Die(3)
    #     self.player.mark_small_straight(self.dice)
    #     self.assertEqual(self.player.get_results()["Pieni suora"], 15)

    # def test_mark_large_straight(self):
    #     self.dice[0] = Die(6)
    #     self.dice[1] = Die(2)
    #     self.dice[2] = Die(4)
    #     self.dice[3] = Die(5)
    #     self.dice[4] = Die(3)
    #     self.player.mark_large_straight(self.dice)
    #     self.assertEqual(self.player.get_results()["Suuri suora"], 20)

    # def test_mark_full_house(self):
    #     self.dice[0] = Die(6)
    #     self.dice[1] = Die(6)
    #     self.dice[2] = Die(6)
    #     self.dice[3] = Die(5)
    #     self.dice[4] = Die(5)
    #     self.player.mark_full_house(self.dice)
    #     self.assertEqual(self.player.get_results()["Täyskäsi"], 28)

    # def test_chance(self):
    #     total = 0
    #     for die in self.dice:
    #         total += die.get_face()
    #     self.player.mark_chance(self.dice)
    #     self.assertEqual(self.player.get_results()["Sattuma"], total)

    # def test_yatzy(self):
    #     for die in self.dice:
    #         die.set_face(1)
    #     self.player.mark_yatzy(self.dice)
    #     self.assertEqual(self.player.get_results()["Yatzy"], 50)
    

