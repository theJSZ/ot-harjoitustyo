import random
import pygame
from resources.clickable_result_names import CLICKABLE_RESULTS
from resources.y_positions_of_result_boxes import Y_POSITIONS_OF_RESULT_BOXES
from entities.result_checker import ResultChecker
CHECKER_FUNCTIONS = ResultChecker.get_functions()

class ClickHandler:
    def __init__(self, game):
        self.game = game

    def handle_clicked_item(self, mouse_pos: tuple):
        """Kutsuu klikkauksen tarkistavia metodeja
        """
        self.handle_clicked_die(mouse_pos)
        self.handle_clicked_throw_area(mouse_pos)
        self.handle_clicked_results(mouse_pos)

    def handle_clicked_results(self, mouse_pos):
        """Tarkistaa onko klikattu tuloksia
        ja suorittaa tarvittavat

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if self.game.player_in_turn.phase > 0:

            for index, y_pos in enumerate(Y_POSITIONS_OF_RESULT_BOXES):
                if mouse_pos[1] in range(y_pos, y_pos+30):
                    # if not yet marked
                    if self.game.player_in_turn.results[CLICKABLE_RESULTS[index]] == 0:
                        player = self.game.player_in_turn

                        # if clicked upstairs
                        if index < 6:
                            result = self.game.checker.check_upstairs(index+1, self.game.dice)
                            player.mark_upstairs(CLICKABLE_RESULTS[index], result)
                            self.game.end_player_turn()
                            return

                        # if clicked downstairs
                        result = CHECKER_FUNCTIONS[index-6](self.game.checker, self.game.dice)
                        player.mark_downstairs(CLICKABLE_RESULTS[index], result)
                        self.game.end_player_turn()

    def handle_clicked_die(self, mouse_pos):
        """Tarkistaa onko klikattu jotain nopista

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if self.game.player_in_turn.phase in [1, 2]:
            for die in self.game.dice:
                if die.in_area(mouse_pos):
                    die.change_freeze_state()

    def handle_clicked_throw_area(self, mouse_pos):
        """Tarkistaa onko klikattu noppien ja tuloslistan välissä,
        tarvittaessa käynnistää arvonta-animaation

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if mouse_pos[1] in range(74, 124) and self.game.player_in_turn.phase < 3:
            player = self.game.player_in_turn
            if not self.game.all_dice_frozen():  # to prevent losing a throw if all dice are frozen
                player.rolling_in_progress = True  # when True, prospective results are not drawn
                rolling_times = [random.randint(5, 30) for _ in range(5)]

                # the "animation"
                for time in range(max(rolling_times)):
                    self.game.clock.tick(20)
                    self.game.drawer.update_screen()

                    # if all dice are finished, we don't keep waiting
                    if not self.game.throw_dice(rolling_times, time):
                        break

                player.phase += 1
                pygame.event.clear()
                player.rolling_in_progress = False
