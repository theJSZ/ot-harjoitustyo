import sys
import pygame
from time import sleep
from entities.die import Die
from entities.drawer import Drawer
from entities.click_handler import ClickHandler
from entities.result_checker import ResultChecker

DICE_Y_POS = 5
GREEN = (10, 200, 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (200, 10, 200)
GRAY = (160, 160, 160)
CHECKER_FUNCTIONS = ResultChecker.get_functions()

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Sans Serif', 30)


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
        self._click_handler = ClickHandler(self)
        self._CLOCK = pygame.time.Clock()

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

        self.unfreeze_all_dice()

        while self._phase < 3 or not self.marked:
            self._CLOCK.tick(30)

            if self._phase == 3:
                self.freeze_all_dice()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._click_handler.handle_clicked_item(mouse_pos)

                self._drawer.update_screen()

    def unfreeze_all_dice(self):
        """Vapauttaa kaikki nopat
        """
        for die in self._dice:
            if die._frozen:
                die.change_freeze_state()


    def freeze_all_dice(self):
        """Jäädyttää kaikki nopat
        """
        for die in self._dice:
            if not die._frozen:
                die.change_freeze_state()

    def _all_dice_frozen(self):
        """Tarkistaa onko kaikki nopat jäädytetty
        """
        for die in self._dice:
            if not die._frozen:
                return False
        return True

    def _throw_dice(self, rolling_times, time):
        """Kutsuu kaikkien noppien throw()-metodia jos
        kaikilla ei vielä ole valmista tulosta
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

    def _place_dice(self):
        """Asettaa nopille oikeat paikat
        """
        for index, die in enumerate(self._dice):
            die.set_position((5 + index*73, DICE_Y_POS))