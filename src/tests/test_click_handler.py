import unittest
from mock import Mock
from entities.click_handler import ClickHandler
from entities.die import Die
from entities.result_checker import ResultChecker
class TestClickHandler(unittest.TestCase):
    def setUp(self):
        self.mock_game = Mock()
        self.mock_game.player_in_turn = Mock()
        self.mock_game.player_in_turn.phase = 0
        self.mock_game.dice = [Die(1)]
        self.mock_game.checker = ResultChecker()
        self.mock_game.dice[0].set_position((0, 0))
        self.click_handler = ClickHandler(self.mock_game)

    def test_handle_clicked_item(self):
        self.click_handler.handle_clicked_item((0, 0))

    def test_handle_clicked_die(self):
        self.mock_game.player_in_turn.phase = 1
        self.click_handler.handle_clicked_item((10, 10))
        self.assertEqual(self.mock_game.dice[0].frozen, True)
        self.click_handler.handle_clicked_item((10, 10))
        self.assertEqual(self.mock_game.dice[0].frozen, False)
        self.click_handler.handle_clicked_item((100, 100))
        self.assertEqual(self.mock_game.dice[0].frozen, False)

    def test_handle_clicked_upstairs_when_allowed(self):
        mock_player = self.mock_game.player_in_turn
        mock_player.phase = 1
        mock_player.results = {"Ykköset": 0}
        self.click_handler.handle_clicked_item((10, 180))
        mock_player.mark_upstairs.assert_called_with("Ykköset", 1)

    def test_handle_clicked_upstairs_when_not_allowed(self):
        mock_player = self.mock_game.player_in_turn
        mock_player.phase = 0
        mock_player.results = {"Ykköset": 0}
        self.click_handler.handle_clicked_item((10, 180))
        mock_player.mark_upstairs.assert_not_called()

    def test_handle_clicked_downstairs_when_not_marked_that_result(self):
        mock_player = self.mock_game.player_in_turn
        self.mock_game.dice = [Die(2), Die(2)]
        mock_player.phase = 1
        mock_player.results = {"1 pari": 0}
        self.click_handler.handle_clicked_item((10, 410))
        mock_player.mark_downstairs.assert_called_with("1 pari", 4)

    def test_handle_clicked_downstairs_when_already_marked_that_result(self):
        mock_player = self.mock_game.player_in_turn
        self.mock_game.dice = [Die(2), Die(2)]
        mock_player.phase = 1
        mock_player.results = {"1 pari": 2}
        self.click_handler.handle_clicked_item((10, 410))
        mock_player.mark_downstairs.assert_not_called()

    def test_handle_clicked_throw_area(self):
        self.mock_game.player_in_turn.phase = 1
        self.mock_game.all_dice_frozen.return_value = False
        self.click_handler.handle_clicked_item((80, 80))
        self.mock_game.throw_dice.assert_called()
