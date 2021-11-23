from time import sleep
from die import Die
from player import Player
from scorecard import Scorecard
import pygame
import os

DICE_Y_POS = 5

class Yatzy:
    def __init__(self, players):
        self._display = pygame.display.set_mode((377, 760))
        self._d_images = [None]
        self._loadImages()
        self._players = players
        self._initPlayers()
        self._dice = [Die() for _ in range(5)]

        for x, die in enumerate(self._dice):
            die.setPosition((5 + x*73, DICE_Y_POS))
        self._scorecard = Scorecard(self._players)
        self._run()

    def _run(self):
        self._running = True
        rounds_left = 15
        while rounds_left:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[1] in range(74, 124):
                        for d in self._dice:
                            d.throw()
                        rounds_left -= 1
            self._updateScreen()
        exit()

    def _initPlayers(self):
        for x, player in enumerate(self._players):
            name = player.getName()
            name_img = font.render(name, False, (0, 0, 0))
            name_img = pygame.transform.scale(name_img, (44, 20))
            player.setText(name_img)
            player.setTextPos((180 + x*47, 140))
            player.setTurn(x)        

    def _updateScreen(self):
        for d in self._dice:
            self._display.blit(self._d_images[d.getFace()], d.getPosition())

        self._display.blit(self._scorecard_img, (0, 128))

        for player in self._players:
            name_img = player.getText()
            name_pos = player.getTextPos()
            self._display.blit(name_img, name_pos)  

        pygame.display.flip()

    def _loadImages(self):

        for i in range(1, 7):
            self._d_images.append(pygame.transform.scale(pygame.image.load(f'src/images/{i}.png'), (65, 65)))

        self._scorecard_img = pygame.image.load('src/images/taulukko.png')  # 377 * 610
        # Each die has 377/5 = 75.4 pixels of space
        # Leave a margin of 5 on each side and they should be
        # around 65 pixels

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Sans Serif', 30)

    players = []
    nPlayers = int(input("How many players? "))
    print("Names:")
    for i in range(nPlayers):
        name = input(f"p{i+1}: ")
        players.append(Player(name))
    game = Yatzy(players)

    

