import sys
import pygame
from database_interface import DatabaseWriter
from database_interface import DatabaseReader
from entities.die import Die
from entities.drawer import Drawer
from entities.click_handler import ClickHandler
from entities.result_checker import ResultChecker

DICE_Y_POS = 5
BLACK = (0, 0, 0)

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Sans Serif', 30)


class Yatzy:
    """Luokka joka huolehtii sovelluslogiikasta
    """
    def __init__(self, players):
        self.display = pygame.display.set_mode((377, 760))
        pygame.display.set_caption('Yatzy')
        self.dice = [Die() for _ in range(5)]
        self._place_dice()

        self.players = players

        self.checker = ResultChecker()
        self.drawer = Drawer(self)
        self.drawer.init_players(self.players)

        self.player_in_turn = None
        self._click_handler = ClickHandler(self)
        self.clock = pygame.time.Clock()

        self.db_writer = DatabaseWriter()
        self.db_reader = DatabaseReader()


    def run(self):
        """Pelisilmukka, suorittaa peliä 15 kierrosta
        jonka jälkeen tallentaa tulokset tietokantaan
        ja näyttää ne tietokannasta
        """

        game_round = 0
        while game_round < 15:
            game_round += 1

            for player in self.players:
                self.player_turn(player)

        self.db_writer.add_game(self.players)
        self.db_reader.show_game()

    def player_turn(self, player):
        """Käsittelee yhden pelaajan vuoron
        kolmessa eri vaiheessa

        Args:
            player (Player): vuorossa oleva pelaaja
        """
        self.player_in_turn = player
        player.phase = 0
        player.marked = False

        self.unfreeze_all_dice()

        while player.phase < 3 or not player.marked:
            self.clock.tick(30)

            if player.phase == 3:
                self.freeze_all_dice()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._click_handler.handle_clicked_item(mouse_pos)

            self.drawer.update_screen()

    def unfreeze_all_dice(self):
        """Vapauttaa kaikki nopat
        """
        for die in self.dice:
            if die.frozen:
                die.change_freeze_state()

    def freeze_all_dice(self):
        """Jäädyttää kaikki nopat
        """
        for die in self.dice:
            if not die.frozen:
                die.change_freeze_state()

    def all_dice_frozen(self):
        """Tarkistaa onko kaikki nopat jäädytetty
        """
        for die in self.dice:
            if not die.frozen:
                return False
        return True

    def throw_dice(self, rolling_times, time):
        """Kutsuu kaikkien noppien throw()-metodia jos
        kaikilla ei vielä ole valmista tulosta
        """
        handled = 0

        for die_number, die in enumerate(self.dice):
            if die.frozen:
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
        self.player_in_turn.marked = True
        self.player_in_turn.phase = 3

    def _place_dice(self):
        """Asettaa nopille oikeat paikat
        """
        for index, die in enumerate(self.dice):
            die.set_position((5 + index*73, DICE_Y_POS))
