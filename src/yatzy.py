import pygame
from die import Die
from scorecard import Scorecard
import sys
from player import Player

DICE_Y_POS = 5
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

marker_functions = [Player.mark_pair,
                    Player.mark_two_pair,
                    Player.mark_three_kind,
                    Player.mark_four_kind,
                    Player.mark_small_straight,
                    Player.mark_large_straight,
                    Player.mark_full_house,
                    Player.mark_chance,
                    Player.mark_yatzy]

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Sans Serif', 30)
clock = pygame.time.Clock()


    

class Yatzy:
    def __init__(self, players):
        self._display = pygame.display.set_mode((377, 760))
        self._d_images = [None]
        self._load_images()
        self._players = players
        self._number_of_players = len(players)
        self._init_players()
        self._dice = [Die() for _ in range(5)]

        for index, die in enumerate(self._dice):
            die.set_position((5 + index*73, DICE_Y_POS))
        self._scorecard = Scorecard(self._players)
        self._run()

    def _run(self):
        self._running = True
        round = 0

# For each round of 15:
#  for each player:
#   for 3 "phases": 
#    roll
#    if phase 3: mark, break (and next player phase 1)
#    else:
#     mark?
#     if mark:
#      break (and next player phase 1)

        while round < 15:
            round += 1
            for player in self._players:
                self.phase = 0
                marked = False
                for die in self._dice:
                    if die.get_freeze_state():
                        die.change_freeze_state()
                while self.phase < 3 or not marked:
                    # print(pygame.mouse.get_pos())
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            clicked_item = self.handle_clicked_item(mouse_pos)

                            if self.phase != 0:
                                for die in self._dice:
                                    if die.in_area(mouse_pos):
                                        die.change_freeze_state()
                                for index, y_pos in enumerate([172, 203, 234, 265, 296, 327]):
                                    if mouse_pos[1] in range(y_pos, y_pos+30):
                                        if (player.mark_upstairs(index+1, self._dice)):
                                            player.update_valisumma()
                                            print()
                                            for item in player.get_results().items():
                                                print(item)
                                            marked = True
                                            self.phase = 3
                                for index, y_pos in enumerate([415, 446, 477, 508, 538, 569, 600, 631, 662]):
                                    if mouse_pos[1] in range(y_pos, y_pos+30):
                                        if (marker_functions[index](player, self._dice)):
                                            print()
                                            for item in player.get_results().items():
                                                print(item)
                                            marked = True
                                            self.phase = 3

                            # if clicked_item == "button" and self.phase < 3:
                            #     self.throw_dice()
                            #     self.phase += 1

                        self._update_screen()
        sys.exit()

    def handle_clicked_item(self, mouse_pos: tuple):
        if mouse_pos[1] in range(74, 124) and self.phase < 3:
            self.throw_dice()
            self.phase += 1



    def throw_dice(self):
        for die in self._dice:
            die.throw()

    def _init_players(self):
        for index, player in enumerate(self._players):
            name = player.get_name()
            name_img = font.render(name, False, (0, 0, 0))
            name_img = pygame.transform.scale(name_img, (44, 20))
            player.set_text(name_img)
            player.set_text_pos((180 + index*47, 140))
            player.set_turn(index)

    def _update_screen(self):
        for die in self._dice:
            die_pos = die.get_position()
            if die.get_freeze_state():
                pygame.draw.rect(self._display, GREEN, (die_pos[0]-5, die_pos[1]-5, die_pos[0]+75, die_pos[1]+75))
            else:
                pygame.draw.rect(self._display, BLACK, (die_pos[0]-5, die_pos[1]-5, die_pos[0]+75, die_pos[1]+75))
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
        # around 65 pixels
