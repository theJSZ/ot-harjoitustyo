import pygame
from resources.coordinates import COORDINATES
from resources.clickable_result_names import CLICKABLE_RESULTS
from entities.result_checker import ResultChecker


GREEN = (10, 200, 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (200, 10, 200)
GRAY = (160, 160, 160)
LIGHT_GRAY = (210, 210, 210)
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Sans Serif', 30)
CHECKER_FUNCTIONS = ResultChecker.get_functions()
RESULT_BOX_WIDTH = 47
class Drawer:
    """Luokka joka vastaa kaikesta piirtämisestä
    """
    def __init__(self, game):
        self.game = game
        self._d_images = [None]
        self._load_dice_images()
        self._scorecard_img = pygame.image.load('src/images/taulukko.png')  # 377 * 610

    def update_screen(self):
        """Piirtää kaiken näytölle
        """
        self.draw_dice()
        self.hide_annotation()
        self.draw_annotation()
        self.draw_scorecard()

        for player in self.game.players:
            self.draw_player_data(player)

        pygame.display.flip()

    def draw_dice(self):
        """Piirtää nopat ja tuloslistan
        """
        for die in self.game.dice:
            if self.game.player_in_turn.phase == 3:
                self.draw_die_border(die, PURPLE)
            else:
                if die.frozen:
                    self.draw_die_border(die, GREEN)
                else:
                    self.draw_die_border(die, BLACK)

            die_image = self._d_images[die.face]
            self.game.display.blit(die_image, die.get_position())

    def draw_die_border(self, die, color):
        """Piirtää annetun värisen kehyksen
        annetulle nopalle

        Args:
            die (Die): noppa
            color (tuple): rgb-väri
        """
        die_pos = die.get_position()
        pygame.draw.rect(self.game.display, color, (die_pos[0]-5, die_pos[1]-5, 75, 75))

    def hide_annotation(self):
        """Maalaa edellisen tekstin yli mustalla
        """
        pygame.draw.rect(self.game.display, BLACK, (0, 73, 377, 377))

    def draw_annotation(self, annotation=None, game_in_progress=True, y_offset=0):
        """Piirtää infotekstin noppien ja tuloslistan väliin
        """
        if game_in_progress:
            if self.game.player_in_turn.rolling_in_progress:
                return

            phase = self.game.player_in_turn.phase
            annotation = f'{self.game.player_in_turn.name}'

            if phase == 0:
                annotation += ', heitto 1'
                if not self.game.player_in_turn.played():  # it is player's first turn
                    annotation += '. Klikkaa tällä alueella'

            elif phase < 3:
                annotation += f', heitto {phase+1}'
                if not self.game.player_in_turn.played():  # it is player's first turn
                    annotation += ' tai merkkaa tulos'

            else:
                annotation += ", merkkaa tulos"

        annotation_img = FONT.render(annotation, False, WHITE)
        annotation_width = annotation_img.get_size()[0]
        annotation_x_position = (377 - annotation_width) / 2  # make center of box
        self.game.display.blit(annotation_img, (annotation_x_position, 90+y_offset))

    def draw_scorecard(self):
        """Piirtää tuloslapun pohjan
        """
        self.game.display.blit(self._scorecard_img, (0, 128))

    def draw_prospective_results(self, player):
        """Piirtää harmaat tulokset kaikkiin ruutuihin
        joissa pelaaja voi saada pisteitä

        Args:
            player (Player): vuorossa oleva pelaaja
        """
        for index, clickable_result in enumerate(CLICKABLE_RESULTS):
            if player.results[clickable_result] == 0:  # ei jo merkattu
                if index < 6:  # yläkerta
                    prospective_result = self.game.checker.check_upstairs(index+1, self.game.dice)

                else:  # alakerta
                    checker_to_use = CHECKER_FUNCTIONS[index-6]
                    prospective_result = checker_to_use(self.game.checker, self.game.dice)

                if prospective_result == 0:
                    prospective_result = '-'
                    color = LIGHT_GRAY
                else:
                    color = GRAY

                prospective_result_img = FONT.render(str(prospective_result), False, color)
                image_width = prospective_result_img.get_size()[0]
                centering_addition = (RESULT_BOX_WIDTH - image_width) / 2
                x_position = centering_addition + player.text_pos[0]
                prospective_result_pos = (x_position, COORDINATES[clickable_result])
                self.game.display.blit(prospective_result_img, prospective_result_pos)

    def draw_player_data(self, player, game_in_progress=True):
        """Piirtää pelaajien nimet, tarjolla olevat tulokset
        ja jo kirjatut tulokset (kutsuen draw_prospective_results)
        """
        # draw player name
        name_img = player.text
        name_img_width = name_img.get_size()[0]

        name_y_pos = player.text_pos[1] - 1
        name_x_pos = player.text_pos[0] + (45 - name_img_width) / 2

        self.game.display.blit(name_img, (name_x_pos, name_y_pos))

        if game_in_progress:
            if self.game.player_in_turn.phase > 0 and not player.rolling_in_progress:
                if player is self.game.player_in_turn:
                    self.draw_prospective_results(player)

        # draw player results
        for result_name, result_value in player.results.items():
            if result_value == 0:
                continue

            result_img = FONT.render(str(result_value), False, BLACK)
            centering_addition = (RESULT_BOX_WIDTH - result_img.get_size()[0]) / 2
            result_pos = (player.text_pos[0] + centering_addition, COORDINATES[result_name])
            self.game.display.blit(result_img, result_pos)

    def hide_dice(self):
        """Maalaa noppien yli mustalla, vanhojen tulosten
        katselussa tarvitaan
        """
        pygame.draw.rect(self.game.display, BLACK, (0, 0, 377, 377))
  
    def _load_dice_images(self):
        """Lataa tarvittavat kuvat
        """
        for i in range(1, 7):
            self._d_images.append(
                pygame.transform.scale(pygame.image.load(f'src/images/{i}.png'), (65, 65)))

    def init_players(self, players: list):
        """Luo kaikille pelaajille name-parametrista kuvan
        jotta pygame voi piirtää sen
        """
        for index, player in enumerate(players):
            name = player.name
            name_img = FONT.render(name, False, BLACK)

            if name_img.get_size()[0] > 44:
                name_img = pygame.transform.scale(name_img, (44, 20))

            player.text = name_img
            name_x_position = 180 + index*47
            player.set_text_pos((name_x_position, 145))
