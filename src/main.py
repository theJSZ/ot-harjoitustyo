from entities.player import Player
from yatzy import Yatzy


PLAYER_LIST = []

while True:
    N_PLAYERS = input("How many players? [1 to 4]\n")

    if N_PLAYERS not in ("1", "2", "3", "4"):
        print("1 to 4 players")
        continue

    N_PLAYERS = int(N_PLAYERS)
    break

print("Names:")
for i in range(N_PLAYERS):
    player_name = input(f"p{i+1}: ")
    PLAYER_LIST.append(Player(player_name))

GAME = Yatzy(PLAYER_LIST)
