import sys
import pygame
from entities.die import Die
from entities.player import Player
from entities.scorecard import Scorecard
from entities.result_checker import ResultChecker
from resources.coordinates import COORDINATES
from resources.clickable_result_names import CLICKABLE_RESULTS
from resources.y_positions_of_result_boxes import y_positions_upstairs, y_positions_downstairs

DICE_Y_POS = 5
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (200, 0, 200)
GRAY = (180, 180, 180)
# pygame.mixer.init()

CHECKER_FUNCTIONS = [ResultChecker.check_pair,
                     ResultChecker.check_two_pair,
                     ResultChecker.check_three_kind,
                     ResultChecker.check_four_kind,
                     ResultChecker.check_small_straight,
                     ResultChecker.check_large_straight,
                     ResultChecker.check_full_house,
                     ResultChecker.check_chance,
                     ResultChecker.check_yatzy]

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Sans Serif', 30)
CLOCK = pygame.time.Clock()


class Yatzy:
    """Luokka joka huolehtii sovelluslogiikasta
    """
    def __init__(self, players):
        self._display = pygame.display.set_mode((377, 760))
        self._d_images = [None]
        self._load_images()
        self._players = players
        self._number_of_players = len(players)
        self._init_players()
        self._dice = [Die() for _ in range(5)]
        self._checker = ResultChecker()
        self._turn_started = False
        self._rolling_in_progress = False
        self.player_in_turn = None
        self.phase = 0

        for index, die in enumerate(self._dice):
            die.set_position((5 + index*73, DICE_Y_POS))
        self._scorecard = Scorecard(self._players)
        self._run()


    def _run(self):
        """Pelisilmukka
        """

        game_round = 0
        while game_round < 15:
            game_round += 1

            for player in self._players:
                self.player_turn(player)
                
        sys.exit()


    def player_turn(self, player):
        """Käsittelee yhden pelaajan vuoron
        kolmessa eri vaiheessa

        Args:
            player (Player): vuorossa oleva pelaaja
        """
        self.player_in_turn = player
        self.phase = 0
        self.marked = False

        for die in self._dice:
            if die.get_freeze_state():
                die.change_freeze_state()

        while self.phase < 3 or not self.marked:
            CLOCK.tick(30)

            if self.phase == 3:
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
        if self.phase > 0:
            for index, y_pos in enumerate(y_positions_downstairs):
                if mouse_pos[1] in range(y_pos, y_pos+30):
                    target_strings = CLICKABLE_RESULTS[6:]

                    # if not yet marked
                    if self.player_in_turn.get_results()[target_strings[index]] == 0:
                        result = CHECKER_FUNCTIONS[index](self._checker, self._dice)
                        self.player_in_turn.mark_downstairs(target_strings[index], result)
                        self.end_player_turn()

    def handle_clicked_upstairs(self, mouse_pos):
        """Tarkistaa onko klikattu yläkerrassa
        ja suorittaa tarvittavat

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if self.phase > 0:
            for index, y_pos in enumerate(y_positions_upstairs):
                if mouse_pos[1] in range(y_pos, y_pos+30):
                    target_strings = CLICKABLE_RESULTS[:6]

                    # if not yet marked
                    if self.player_in_turn.get_results()[target_strings[index]] == 0:
                        result = self._checker.check_upstairs(index+1, self._dice)
                        self.player_in_turn.mark_upstairs(index+1, result)
                        self.end_player_turn()

    def handle_clicked_die(self, mouse_pos):
        """Tarkistaa onko klikattu jotain nopista

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if self.phase in [1, 2]:
            for die in self._dice:
                if die.in_area(mouse_pos):
                    die.change_freeze_state()

    def handle_clicked_throw_area(self, mouse_pos):
        """Tarkistaa onko klikattu noppien ja tuloslistan välissä

        Args:
            mouse_pos (tuple): hiiren sijainti
        """
        if mouse_pos[1] in range(74, 124) and self.phase < 3:
            self._turn_started = True
            self._rolling_in_progress = True  # to prevent prospective results from flashing
            for _ in range(10):
                CLOCK.tick(30)
                self._throw_dice()
                self._update_screen()
            self.phase += 1
            self._rolling_in_progress = False

    def freeze_all(self):
        for die in self._dice:
            if not die.get_freeze_state():
                die.change_freeze_state()

    def _throw_dice(self):
        """Kutsuu kaikkien noppien throw()-metodia
        """
        for die in self._dice:
            die.throw()

    def end_player_turn(self):
        """Päättää pelaajan vuoron
        """
        self.marked = True
        self.phase = 3
        self._turn_started = False

    def _init_players(self):
        """Luo kaikille pelaajille name-parametrista kuvan
        jotta pygame voi piirtää sen
        """
        for index, player in enumerate(self._players):
            name = player.get_name()
            name_img = FONT.render(name, False, BLACK)
            player.set_text(name_img)
            player.set_text_pos((180 + index*47, 140))

    def _update_screen(self):
        """Piirtää kaiken näytölle
        """
        self.draw_dice_and_scorecard()
        self.draw_player_data()
        self.draw_annotation()

        pygame.display.flip()

    def draw_dice_and_scorecard(self):
        """Piirtää nopat ja tuloslistan
        """
        for die in self._dice:
            if self.phase == 3:
                self.draw_die_border(die, PURPLE)
            else:
                if die.get_freeze_state():
                    self.draw_die_border(die, GREEN)
                else:
                    self.draw_die_border(die, BLACK)
            self._display.blit(self._d_images[die.get_face()], die.get_position())

        pygame.draw.rect(self._display, BLACK, (0, 73, 377, 377))
        self._display.blit(self._scorecard_img, (0, 128))

    def draw_player_data(self):
        """Piirtää pelaajien nimet, tarjolla olevat tulokset
        ja jo kirjatut tulokset (kutsuen draw_prospective_results)
        """
        for player in self._players:
            # draw player names
            name_img = player.get_text()
            name_pos = player.get_text_pos()
            self._display.blit(name_img, name_pos)

            if self.phase > 0 and not self._rolling_in_progress:
                if player is self.player_in_turn:
                    self.draw_prospective_results(player)
                    
            # draw player results
            for result_name, result_value in player.get_results().items():
                if result_value == 0:
                    continue

                result_img = FONT.render(str(result_value), False, BLACK)
                result_pos = (player.get_text_pos()[0] + 10, COORDINATES[result_name])
                self._display.blit(result_img, result_pos)

    def draw_annotation(self):
        """Piirtää aputekstin noppien ja tuloslistan väliin
        """
        annotation = f'{self.player_in_turn.get_name()}'
        if self.phase == 0:
            annotation += ', heitto 1. Klikkaa tällä alueella'
        elif self.phase < 3:
            annotation += f', heitto {self.phase+1} tai merkkaa tulos'
        else:
            annotation += ", merkkaa tulos"
        annotation_img = FONT.render(annotation, False, WHITE)
        self._display.blit(annotation_img, (20, 90))

    def draw_die_border(self, die, color):
        """Piirtää annetun värisen kehyksen
        annetulle nopalle

        Args:
            die (Die): noppa
            color (tuple): rgb-väri
        """
        die_pos = die.get_position()
        pygame.draw.rect(self._display, color, (die_pos[0]-5, die_pos[1]-5, 75, 75))

    def draw_prospective_results(self, player):
        """Piirtää harmaat tulokset kaikkiin ruutuihin
        joissa pelaaja voi saada pisteitä

        Args:
            player (Player): vuorossa oleva pelaaja
        """
        for index, clickable_result in enumerate(CLICKABLE_RESULTS):
            if player.get_results()[clickable_result] == 0:  # ei jo merkattu
                if index < 6:  # yläkerta
                    prospective_result = self._checker.check_upstairs(index+1, self._dice)
                else:  # alakerta
                    prospective_result = CHECKER_FUNCTIONS[index-6](self._checker, self._dice)

                if prospective_result != 0:
                    prospective_result_img = FONT.render(str(prospective_result), False, GRAY)
                    prospective_result_pos = (player.get_text_pos()[0] + 10, COORDINATES[clickable_result])
                    self._display.blit(prospective_result_img, prospective_result_pos)

    def _load_images(self):
        """Lataa tarvittavat kuvat
        """
        for i in range(1, 7):
            self._d_images.append(
                pygame.transform.scale(pygame.image.load(f'src/images/{i}.png'), (65, 65)))

        self._scorecard_img = pygame.image.load('src/images/taulukko.png')  # 377 * 610
