import unittest
from yatzy import Yatzy
from entities.player import Player

class TestYatzy(unittest.TestCase):
    def setUp(self):
        self.players = [Player("JSZ")]
        self.game = Yatzy(self.players)

    def test_players(self):
        self.assertEqual(self.game.players[0].name, "JSZ")

    def test_freeze_die(self):
        for die in self.game.dice:
            self.assertEqual(die.frozen, False)
        self.game.freeze_all_dice()
        self.game.freeze_all_dice()
        for die in self.game.dice:
            self.assertEqual(die.frozen, True)
        self.game.unfreeze_all_dice()
        self.game.unfreeze_all_dice()
        for die in self.game.dice:
            self.assertEqual(die.frozen, False)

    def check_all_dice_frozen(self):
        for die in self.game.dice:
            self.assertEqual(die.frozen, False)
        self.assertEqual(self.game.all_dice_frozen(), False)
        self.game.freeze_all_dice()
        self.assertEqual(self.game.all_dice_frozen(), True)

    def test_throw_dice(self):
        self.assertEqual(self.game.throw_dice([1, 1, 1, 1, 1], 1), False)
        self.assertEqual(self.game.throw_dice([1, 1, 1, 1, 1], 0), True)

    def test_end_player_turn(self):
        self.game.player_in_turn = self.game.players[0]
        self.game.end_player_turn()
        self.assertEqual(self.game.player_in_turn.marked, True)
