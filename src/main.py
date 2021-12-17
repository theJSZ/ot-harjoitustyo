from time import sleep
import random
import math
import os
from database_interface import DatabaseReader
from entities.player import Player
from yatzy import Yatzy

PI = 3.1415
PLAYER_LIST = []

def print_yatzy(offset):
    """Tulostaa YATZY Ascii-laatikossa

    Args:
        offset (int): haluttu määrä tyhjää ennen laatikkoa
    """
    print(offset*' ' + u'\u250F' + 5*u'\u2501' + u'\u2513')
    print(offset*' ' + u'\u2503' + "YATZY" + u'\u2503')
    print(offset*' ' + u'\u2517' + 5*u'\u2501' + u'\u251B', flush=True)

def invalid_player_name():
    """Tarkistaa onko annettu nimi epäkelpo

    Returns:
        [bool]: True jos epäkelpo, muuten False
    """
    lowercase_names = [player.name.lower() for player in PLAYER_LIST]
    return len(player_name) > 3 or player_name.lower() in lowercase_names

def check_player_name():
    """Ilmoittaa mikä nimessä on vialla
    """
    if len(player_name) > 3:
        print("3 merkkiä tai vähemmän :(\n")
    if player_name.lower() in [player.name.lower() for player in PLAYER_LIST]:
        print("Nimi käytössä :(\n")


if __name__ == "__main__":
    os.system('clear')
    print_yatzy(0)

    while True:
        os.system('clear')
        print_yatzy(0)

        N_PLAYERS = input("Pelaajien määrä? (1-4, tai 0: katso vanhoja tuloksia)\n")

        if N_PLAYERS not in ("1", "2", "3", "4", "0"):
            continue

        N_PLAYERS = int(N_PLAYERS)
        break

    if N_PLAYERS == 0:
        db_reader = DatabaseReader()
        db_reader.show_game(1)

    else:    
        for i in range(N_PLAYERS):
            os.system('clear')
            print_yatzy(0)

            player_name = "xxxx"
            while invalid_player_name():
                player_name = input(f"Pelaaja {i+1}: ")
                check_player_name()

            PLAYER_LIST.append(Player(player_name))

        os.system('clear')

        for i in range(15):
            print_yatzy(random.randint(0, 10) + 18 + (int(math.sin(i/5)*30)))
            sleep(0.10)
        os.system('clear')
        GAME = Yatzy(PLAYER_LIST)
