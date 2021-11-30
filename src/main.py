import sys
import pygame
from die import Die
from player import Player
from scorecard import Scorecard

DICE_Y_POS = 5

class Yatzy:
    def __init__(self, players):
        self._display = pygame.display.set_mode((377, 760))
        self._d_images = [None]
        self._load_images()
        self._players = players
        self._init_players()
        self._dice = [Die() for _ in range(5)]

        for index, die in enumerate(self._dice):
            die.set_position((5 + index*73, DICE_Y_POS))
        self._scorecard = Scorecard(self._players)
        self._run()

    def _run(self):
        self._running = True
        rounds_left = 15
        while rounds_left:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[1] in range(74, 124):
                        for die in self._dice:
                            die.throw()
                        rounds_left -= 1
            self._update_screen()
        sys.exit()

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

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Sans Serif', 30)

    player_list = []

    while True:
        try:
            n_players = int(input("How many players? "))
        except:
            print("invalid input")
            continue
        if not n_players in range(1, 5):
            print("1 to 4 players")
            continue
        break

    print("Names:")
    for i in range(n_players):
        player_name = input(f"p{i+1}: ")
        player_list.append(Player(player_name))
    game = Yatzy(player_list)
