from player import Player
from yatzy import Yatzy

    
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
