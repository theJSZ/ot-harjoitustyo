import sys
import pygame
from entities.die import Die
from entities.scorecard import Scorecard
from entities.result_checker import ResultChecker

DICE_Y_POS = 5
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

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
    def __init__(self, players):
        self._display = pygame.display.set_mode((377, 760))
        self._d_images = [None]
        self._load_images()
        self._players = players
        self._number_of_players = len(players)
        self._init_players()
        self._dice = [Die() for _ in range(5)]
        self._checker = ResultChecker()

        for index, die in enumerate(self._dice):
            die.set_position((5 + index*73, DICE_Y_POS))
        self._scorecard = Scorecard(self._players)
        self._run()

    def _run(self):

        game_round = 0
        while game_round < 15:
            game_round += 1
            for player in self._players:
                self.init_player_turn(player)
                self.init_dice()
                while self.phase < 3 or not self.marked:
                    # print(pygame.mouse.get_pos())
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            self.handle_clicked_item(mouse_pos)

                        self._update_screen()
        sys.exit()

    def init_player_turn(self, player):
        self.player_in_turn = player
        self.phase = 0
        self.marked = False

    def init_dice(self):
        for die in self._dice:
            if die.get_freeze_state():
                die.change_freeze_state()


    def handle_clicked_item(self, mouse_pos: tuple):
        if mouse_pos[1] in range(74, 124) and self.phase < 3:
            self.throw_dice()
            self.phase += 1
            return

        if self.phase != 0:
            for die in self._dice:
                if die.in_area(mouse_pos):
                    die.change_freeze_state()
                    return

        # if clicked upstairs
        for index, y_pos in enumerate([172, 203, 234, 265, 296, 327]):
            if mouse_pos[1] in range(y_pos, y_pos+30):
                target_strings = ["Ykköset",
                                  "Kakkoset",
                                  "Kolmoset",
                                  "Neloset",
                                  "Viitoset",
                                  "Kuutoset"]
                # if not yet marked
                if self.player_in_turn.get_results()[target_strings[index]] == 0:
                    result = self._checker.check_upstairs(index+1, self._dice)
                    self.player_in_turn.mark_upstairs(index+1, result)

                    print()
                    print(self.player_in_turn.get_name())
                    for item in self.player_in_turn.get_results().items():
                        print(item)

                    self.end_player_turn()
                    return

        # if clickd downstairs
        for index, y_pos in enumerate([400, 431, 462, 500, 531, 562, 597, 628, 664]):
            if mouse_pos[1] in range(y_pos, y_pos+30):
                target_strings = ["1 pari",
                                  "2 paria",
                                  "3 samaa",
                                  "4 samaa",
                                  "Pieni suora",
                                  "Suuri suora",
                                  "Täyskäsi",
                                  "Sattuma",
                                  "Yatzy"]
                # if not yet marked
                if self.player_in_turn.get_results()[target_strings[index]] == 0:
                    result = CHECKER_FUNCTIONS[index](self._checker, self._dice)
                    self.player_in_turn.mark_downstairs(target_strings[index], result)

                print()
                print(self.player_in_turn.get_name())
                for item in self.player_in_turn.get_results().items():
                    print(item)
                self.end_player_turn()


    def throw_dice(self):
        for die in self._dice:
            die.throw()

    def end_player_turn(self):
        self.marked = True
        self.phase = 3

    def _init_players(self):
        for index, player in enumerate(self._players):
            name = player.get_name()
            name_img = FONT.render(name, False, (0, 0, 0))
            name_img = pygame.transform.scale(name_img, (44, 20))
            player.set_text(name_img)
            player.set_text_pos((180 + index*47, 140))

    def _update_screen(self):
        for die in self._dice:
            die_pos = die.get_position()
            if die.get_freeze_state():
                pygame.draw.rect(self._display, GREEN, (die_pos[0]-5, die_pos[1]-5, 75, 75))
            else:
                pygame.draw.rect(
                    self._display, BLACK,
                    (die_pos[0]-5, die_pos[1]-5, die_pos[0]+75, die_pos[1]+75))
            self._display.blit(self._d_images[die.get_face()], die.get_position())

        self._display.blit(self._scorecard_img, (0, 128))

        for player in self._players:
            name_img = player.get_text()
            name_pos = player.get_text_pos()
            self._display.blit(name_img, name_pos)


        pygame.display.flip()

    def _load_images(self):

        for i in range(1, 7):
            self._d_images.append(
                pygame.transform.scale(pygame.image.load(f'src/images/{i}.png'), (65, 65)))

        self._scorecard_img = pygame.image.load('src/images/taulukko.png')  # 377 * 610
        # Each die has 377/5 = 75.4 pixels of space
        # Leave a margin of 5 on each side and they should be
        # agame_round 65 pixels
