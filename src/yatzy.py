import sys
import pygame
import random
from time import sleep
from entities.die import Die
from entities.drawer import Drawer
from entities.result_checker import ResultChecker
from resources.clickable_result_names import CLICKABLE_RESULTS
from resources.y_positions_of_result_boxes import y_positions_upstairs, y_positions_downstairs

DICE_Y_POS = 5
GREEN = (10, 200, 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# RED = (255, 0, 0)
PURPLE = (200, 10, 200)
GRAY = (160, 160, 160)
# DARK_GRAY = (50, 50, 50)
CHECKER_FUNCTIONS = ResultChecker.get_functions()

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Sans Serif', 30)
CLOCK = pygame.time.Clock()


class Yatzy:
    """Luokka joka huolehtii sovelluslogiikasta
    """
    def __init__(self, players):
        self._display = pygame.display.set_mode((377, 760))
        self._dice = [Die() for _ in range(5)]
        self._place_dice()

        self._players = players
        self._number_of_players = len(players)
        self._init_players()
        
        self._checker = ResultChecker()
        self._drawer = Drawer(self)

        self._rolling_in_progress = False
        self._player_in_turn = None
        self._phase = 0

        self._run()


    def _run(self):
        """Pelisilmukka
        """

        game_round = 0
        while game_round < 15:
            game_round += 1

            for player in self._players:
                self.player_turn(player)
                
        sleep(100)
        sys.exit()


    def player_turn(self, player):
        """Käsittelee yhden pelaajan vuoron
        kolmessa eri vaiheessa

        Args:
            player (Player): vuorossa oleva pelaaja
        """
        self._player_in_turn = player
        self._phase = 0
        self.marked = False

        for die in self._dice:
            if die._frozen:
                die.change_freeze_state()

        while self._phase < 3 or not self.marked:
            CLOCK.tick(30)

            if self._phase == 3:
                self.freeze_all()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_clicked_item(mouse_pos)

                self._update_screen()

    def handle_clicked_item(self, mouse_pos: tuple):
        """Kutsuu klikkauksen tarkistavia metodeja
        """
        self.handle_clicked_die(mouse_pos)
        self.handle_clicked_throw_area(mouse_pos)
        self.handle_clicked_upstairs(mouse_pos)
        self.handle_clicked_downstairs(mouse_pos)

    def handle_clicked_downstairs(self, mouse_pos):
        """Tarkistaa onko klikattu alakerrassa
        ja suorittaa tarvittavat

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if self._phase > 0:
            for index, y_pos in enumerate(y_positions_downstairs):
                if mouse_pos[1] in range(y_pos, y_pos+30):
                    target_strings = CLICKABLE_RESULTS[6:]

                    # if not yet marked
                    if self._player_in_turn._results[target_strings[index]] == 0:
                        result = CHECKER_FUNCTIONS[index](self._checker, self._dice)
                        self._player_in_turn.mark_downstairs(target_strings[index], result)
                        self.end_player_turn()

    def handle_clicked_upstairs(self, mouse_pos):
        """Tarkistaa onko klikattu yläkerrassa
        ja suorittaa tarvittavat

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if self._phase > 0:
            for index, y_pos in enumerate(y_positions_upstairs):
                if mouse_pos[1] in range(y_pos, y_pos+30):
                    target_strings = CLICKABLE_RESULTS[:6]

                    # if not yet marked
                    if self._player_in_turn._results[target_strings[index]] == 0:
                        result = self._checker.check_upstairs(index+1, self._dice)
                        self._player_in_turn.mark_upstairs(index+1, result)
                        self.end_player_turn()

    def handle_clicked_die(self, mouse_pos):
        """Tarkistaa onko klikattu jotain nopista

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if self._phase in [1, 2]:
            for die in self._dice:
                if die.in_area(mouse_pos):
                    die.change_freeze_state()

    def handle_clicked_throw_area(self, mouse_pos):
        """Tarkistaa onko klikattu noppien ja tuloslistan välissä

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if mouse_pos[1] in range(74, 124) and self._phase < 3:
            if not self._all_dice_frozen():
                self._rolling_in_progress = True  # to prevent prospective results from flashing
                rolling_times = [random.randint(5,30) for _ in range(5)]
                for time in range(max(rolling_times)):
                    CLOCK.tick(20)
                    self._update_screen()
                    if not self._throw_dice(rolling_times, time):
                        break
                self._phase += 1
                self._rolling_in_progress = False

    def freeze_all(self):
        for die in self._dice:
            if not die._frozen:
                die.change_freeze_state()

    def _all_dice_frozen(self):
        for die in self._dice:
            if not die._frozen:
                return False
        return True

    def _throw_dice(self, rolling_times, time):
        """Kutsuu kaikkien noppien throw()-metodia
        """
        handled = 0

        for die_number, die in enumerate(self._dice):
            if die._frozen:
                handled += 1
                if handled == 5:
                    return False
                continue

            if rolling_times[die_number] > time:
                die.throw()
            else:
                handled += 1
                if handled == 5:
                    return False
        return True

    def end_player_turn(self):
        """Päättää pelaajan vuoron
        """
        self.marked = True
        self._phase = 3

    def _init_players(self):
        """Luo kaikille pelaajille name-parametrista kuvan
        jotta pygame voi piirtää sen
        """
        for index, player in enumerate(self._players):
            name = player._name
            name_img = FONT.render(name, False, BLACK)
            if name_img.get_size()[0] > 44:
                name_img = pygame.transform.scale(name_img, (44, 20))
            player._text = name_img
            name_x_position = 180 + index*47
            player.set_text_pos((name_x_position, 145))

    def _update_screen(self):
        """Piirtää kaiken näytölle
        """
        self._drawer.draw_dice_and_scorecard()
        self._drawer.draw_player_data()
        self._drawer.draw_annotation()

        pygame.display.flip()

    def _place_dice(self):
        """Asettaa nopille oikeat paikat
        """
        for index, die in enumerate(self._dice):
            die.set_position((5 + index*73, DICE_Y_POS))