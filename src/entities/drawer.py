import pygame
from resources.coordinates import COORDINATES
from resources.clickable_result_names import CLICKABLE_RESULTS
from entities.result_checker import ResultChecker


DICE_Y_POS = 5
GREEN = (10, 200, 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# RED = (255, 0, 0)
PURPLE = (200, 10, 200)
GRAY = (160, 160, 160)
# DARK_GRAY = (50, 50, 50)
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Sans Serif', 30)
CLOCK = pygame.time.Clock()
CHECKER_FUNCTIONS = ResultChecker.get_functions()

class Drawer:
    def __init__(self, game):
        self.game = game
        self._d_images = [None]
        self._load_dice_images()


    def draw_die_border(self, die, color):
        """Piirtää annetun värisen kehyksen
        annetulle nopalle

        Args:
            die (Die): noppa
            color (tuple): rgb-väri
        """
        die_pos = die.get_position()
        pygame.draw.rect(self.game._display, color, (die_pos[0]-5, die_pos[1]-5, 75, 75))

    def draw_prospective_results(self, player):
        """Piirtää harmaat tulokset kaikkiin ruutuihin
        joissa pelaaja voi saada pisteitä

        Args:
            player (Player): vuorossa oleva pelaaja
        """
        for index, clickable_result in enumerate(CLICKABLE_RESULTS):
            if player._results[clickable_result] == 0:  # ei jo merkattu
                if index < 6:  # yläkerta
                    prospective_result = self.game._checker.check_upstairs(index+1, self.game._dice)
                else:  # alakerta
                    prospective_result = CHECKER_FUNCTIONS[index-6](self.game._checker, self.game._dice)

                if prospective_result != 0:
                    prospective_result_img = FONT.render(str(prospective_result), False, GRAY)
                    prospective_result_pos = (player._text_pos[0] + 10, COORDINATES[clickable_result])
                    self.game._display.blit(prospective_result_img, prospective_result_pos)

    
    def draw_annotation(self):
        """Piirtää aputekstin noppien ja tuloslistan väliin
        """
        if self.game._rolling_in_progress:
            return

        annotation = f'{self.game._player_in_turn._name}'
        if self.game._phase == 0:
            annotation += ', heitto 1'
            if not self.game._player_in_turn.played():
                annotation +=  '. Klikkaa tällä alueella'
        elif self.game._phase < 3:
            annotation += f', heitto {self.game._phase+1} tai merkkaa tulos'
        else:
            annotation += ", merkkaa tulos"
        
        annotation_img = FONT.render(annotation, False, WHITE)
        annotation_width = annotation_img.get_size()[0]
        annotation_x_position = (377 - annotation_width) / 2
        self.game._display.blit(annotation_img, (annotation_x_position, 90))


    def draw_player_data(self):
        """Piirtää pelaajien nimet, tarjolla olevat tulokset
        ja jo kirjatut tulokset (kutsuen draw_prospective_results)
        """
        for player in self.game._players:
            # draw player names
            name_img = player._text
            name_img_width = name_img.get_size()[0]

            name_y_pos = player._text_pos[1] - 1
            name_x_pos = player._text_pos[0] + (45 - name_img_width) / 2
            
            self.game._display.blit(name_img, (name_x_pos, name_y_pos))

            if self.game._phase > 0 and not self.game._rolling_in_progress:
                if player is self.game._player_in_turn:
                    self.draw_prospective_results(player)
                    
            # draw player results
            for result_name, result_value in player._results.items():
                if result_value == 0:
                    continue

                result_img = FONT.render(str(result_value), False, BLACK)
                result_pos = (player._text_pos[0] + 10, COORDINATES[result_name])
                self.game._display.blit(result_img, result_pos)

    def draw_dice_and_scorecard(self):
        """Piirtää nopat ja tuloslistan
        """
        for die in self.game._dice:
            if self.game._phase == 3:
                self.draw_die_border(die, PURPLE)
            else:
                if die._frozen:
                    self.draw_die_border(die, GREEN)
                else:
                    self.draw_die_border(die, BLACK)
            self.game._display.blit(self._d_images[die.face], die.get_position())

        # hides the previous annotation
        pygame.draw.rect(self.game._display, BLACK, (0, 73, 377, 377))
        
        self.game._display.blit(self._scorecard_img, (0, 128))

    def _load_dice_images(self):
        """Lataa tarvittavat kuvat
        """
        for i in range(1, 7):
            self._d_images.append(
                pygame.transform.scale(pygame.image.load(f'src/images/{i}.png'), (65, 65)))

        self._scorecard_img = pygame.image.load('src/images/taulukko.png')  # 377 * 610
