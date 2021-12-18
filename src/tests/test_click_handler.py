# import unittest
# from mock import Mock
# from entities.die import Die
# from entities.click_handler import ClickHandler

# class TestClickHandler(unittest.TestCase):
#     def setUp(self):
#         self.game = Mock()
#         self.click_handler = Mock(wraps=ClickHandler(self.game))

#     def test_root_click_handler(self):
#         self.game.player_in_turn.phase = 0
#         self.click_handler.handle_clicked_item((0, 0))
#         # self.click_handler.handle_clicked_die.assert_called_with((0, 0))

#     def test_handle_clicked_die(self):
#         self.game.player_in_turn.phase = 1
#         self.game.dice = [Die() for _ in range(5)]
#         self.game.dice[0].set_position((0, 0))
#         self.click_handler.handle_clicked_die((10, 10))
#         self.assertEqual(self.game.dice[0].frozen, True)
#         self.click_handler.handle_clicked_die((100, 100))
#         self.assertEqual(self.game.dice[0].frozen, True)

#     def test_handle_clicked_throw(self):
#         mouse_pos = (80, 80)
#         self.click_handler.handle_clicked_throw_area(mouse_pos)

    