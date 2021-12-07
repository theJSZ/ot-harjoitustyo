from entities.player import Player
from yatzy import Yatzy


PLAYER_LIST = []

while True:
    try:
        N_PLAYERS = int(input("How many players? "))
    except TypeError:
        print("invalid input")
        continue

    if N_PLAYERS not in range(1, 5):
        print("1 to 4 players")
        continue

    break

print("Names:")
for i in range(N_PLAYERS):
    player_name = input(f"p{i+1}: ")
    PLAYER_LIST.append(Player(player_name))

GAME = Yatzy(PLAYER_LIST)
