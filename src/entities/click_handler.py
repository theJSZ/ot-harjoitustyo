import random
import pygame
from resources.clickable_result_names import CLICKABLE_RESULTS
from resources.y_positions_of_result_boxes import Y_POSITIONS_OF_RESULT_BOXES
from entities.result_checker import ResultChecker
CHECKER_FUNCTIONS = ResultChecker.get_functions()

class ClickHandler:
    """Luokka klikkausten käsittelylle
    """
    def __init__(self, game):
        self.game = game

    def handle_clicked_item(self, mouse_pos: tuple):
        """Kutsuu klikkauksen tarkistavia metodeja
        """
        if mouse_pos[1] in range(5, 70):
            self.handle_clicked_die(mouse_pos)
    
        if self.legal_throw(mouse_pos):
            self.handle_clicked_throw_area()
    
        if self.game.player_in_turn.phase == 0:
            return

        for index, y_pos in enumerate(Y_POSITIONS_OF_RESULT_BOXES):
            if self.legal_result(mouse_pos, index, y_pos):
                self.handle_clicked_result(index)

    def legal_result(self, mouse_pos, index, y_pos):
        if not mouse_pos[1] in range(y_pos, y_pos+30):
            return False
        if not self.game.player_in_turn.results[CLICKABLE_RESULTS[index]] == 0:
            return False

        return True

    def legal_throw(self, mouse_pos):
        """Tarkistaa hiiren sijainnin ja kierroksen
        vaiheen mukaan saako heittää noppia

        Args:
            mouse_pos (tuple): hiiren koordinaatit

        Returns:
            True / False
        """
        if mouse_pos[1] not in range(74, 124):
            return False
        if self.game.player_in_turn.phase == 3:
            return False
        if self.game.all_dice_frozen():
            return False

        return True

    def handle_clicked_die(self, mouse_pos):
        """Tarkistaa onko klikattu jotain nopista

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if not self.game.player_in_turn.phase in [1, 2]:  # only hold dice after 1st and 2nd throws
            return

        for die in self.game.dice:
            if die.in_area(mouse_pos):
                die.change_freeze_state()

    def handle_clicked_throw_area(self):
        """Tarkistaa onko klikattu noppien ja tuloslistan välissä,
        tarvittaessa käynnistää arvonta-animaation

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        player = self.game.player_in_turn
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

    def handle_clicked_result(self, index):
        """Tarkistaa mitä ruutua on klikattu ja
        kutsuu tuloksen tarkistajaa, merkkaa tuloksen pelaajalle

        Args:
            index (int): ruudun indeksi
        """
        if index < 6:
            result = self.game.checker.check_upstairs(index+1, self.game.dice)
        else:
            result = CHECKER_FUNCTIONS[index-6](self.game.checker, self.game.dice)
            
        self.game.player_in_turn.mark_result(CLICKABLE_RESULTS[index], result)
        self.game.end_player_turn()
