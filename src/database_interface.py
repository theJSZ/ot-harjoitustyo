import sys
import sqlite3
from datetime import datetime
import pygame
from entities.player import Player
from entities.drawer import Drawer

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Sans Serif', 30)
BLACK = (0, 0, 0)
CLOCK = pygame.time.Clock()


class DatabaseWriter:
    def __init__(self):
        self.database = sqlite3.connect("./data/yatzy.db")
        self.database.isolation_level = None
        self.create_tables()
        self.date = datetime.now()
    def create_tables(self):
        self.database.execute(
            """CREATE TABLE IF NOT EXISTS tulokset(id INTEGER PRIMARY KEY,
            ykköset INTEGER, kakkoset INTEGER, kolmoset INTEGER, neloset INTEGER,
            viitoset INTEGER, kuutoset INTEGER, pari INTEGER, kaksi_paria INTEGER,
            kolme_samaa INTEGER, neljä_samaa INTEGER, pikku_suora INTEGER,
            iso_suora INTEGER, täyskäsi INTEGER, sattuma INTEGER, yatzy INTEGER, pelaaja TEXT)""")

        self.database.execute(
            """CREATE TABLE IF NOT EXISTS pelit(id INTEGER PRIMARY KEY,
            tulos1 INTEGER DEFAULT 0 REFERENCES tulokset,
            tulos2 INTEGER DEFAULT 0 REFERENCES tulokset,
            tulos3 INTEGER DEFAULT 0 REFERENCES tulokset,
            tulos4 INTEGER DEFAULT 0 REFERENCES tulokset,
            date DATE)""")

    def add_game(self, players: list):
        result_ids = [0, 0, 0, 0]
        year = self.date.year
        month = self.date.month
        day = self.date.day
        timestamp = f'{year}-{month:02d}-{day:02d}'

        for index, player in enumerate(players):
            results = player.results
            for result in results:
                if result == 'x':
                    result = 0
            self.database.execute(
                """INSERT INTO tulokset(ykköset, kakkoset, kolmoset,
                neloset, viitoset, kuutoset,
                pari, kaksi_paria, kolme_samaa, neljä_samaa,
                pikku_suora, iso_suora, täyskäsi, sattuma, yatzy, pelaaja)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [results["Ykköset"],
                      results["Kakkoset"],
                      results["Kolmoset"],
                      results["Neloset"],
                      results["Viitoset"],
                      results["Kuutoset"],
                      results["1 pari"],
                      results["2 paria"],
                      results["3 samaa"],
                      results["4 samaa"],
                      results["Pieni suora"],
                      results["Suuri suora"],
                      results["Täyskäsi"],
                      results["Sattuma"],
                      results["Yatzy"],
                      player.name])

            result_id = self.database.execute("SELECT MAX(id) from tulokset").fetchone()[0]
            result_ids[index] = int(result_id)

        self.database.execute("""INSERT INTO pelit(tulos1, tulos2, tulos3, tulos4, date)
        VALUES(?, ?, ?, ?, ?)""", [result_ids[0],
                                   result_ids[1],
                                   result_ids[2],
                                   result_ids[3],
                                   timestamp])

class DatabaseReader:
    def __init__(self):
        self.display = pygame.display.set_mode((377, 760))
        self.database = sqlite3.connect("./data/yatzy.db")
        self.database.isolation_level = None
        self.drawer = Drawer(self)

    def show_game(self, game_id: int = None):
        if not game_id:
            game_id = self.database.execute("SELECT MAX(id) FROM pelit").fetchone()[0]
        stored_games = self.database.execute("SELECT * FROM pelit").fetchall()
        number_of_stored_games = len(stored_games)

        game = self.database.execute("SELECT * FROM pelit WHERE ID = (?)", [game_id]).fetchone()
        if not game:
            return

        result1_id = game[1]
        result2_id = game[2]
        result3_id = game[3]
        result4_id = game[4]
        timestamp = game[5]
        results = []
        self.players = []

        for result_id in (result1_id, result2_id, result3_id, result4_id):
            self.fetch_result(result_id, results)

        for result in results:
            player = Player(result[-1])
            player.results["Ykköset"] = result[1]
            player.results["Kakkoset"] = result[2]
            player.results["Kolmoset"] = result[3]
            player.results["Neloset"] = result[4]
            player.results["Viitoset"] = result[5]
            player.results["Kuutoset"] = result[6]
            player.update_valisumma()
            player.results["1 pari"] = result[7]
            player.results["2 paria"] = result[8]
            player.results["3 samaa"] = result[9]
            player.results["4 samaa"] = result[10]
            player.results["Pieni suora"] = result[11]
            player.results["Suuri suora"] = result[12]
            player.results["Täyskäsi"] = result[13]
            player.results["Sattuma"] = result[14]
            player.results["Yatzy"] = result[15]
            player.update_total()

            self.players.append(player)

        self.init_players()

        self.drawer.hide_dice()
        self.drawer.hide_annotation()
        self.drawer.draw_annotation('Historian havinaa!', False, -80)
        self.drawer.draw_annotation('Selaa nuolinäppäimillä', False, -40)

        self.drawer.draw_annotation(f'Peli {game_id}: {timestamp}', False)
        self.drawer.draw_scorecard()
        for player in self.players:
            self.drawer.draw_player_data(player, False)
            pygame.display.flip()

        running = True
        while running:
            CLOCK.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if game_id > 1:
                            self.show_game(game_id-1)
                    if event.key == pygame.K_RIGHT:
                        if game_id < number_of_stored_games:
                            self.show_game(game_id+1)

    def init_players(self):
        """Luo kaikille pelaajille name-parametrista kuvan
        jotta pygame voi piirtää sen
        """
        for index, player in enumerate(self.players):
            name = player.name
            name_img = FONT.render(name, False, BLACK)
            if name_img.get_size()[0] > 44:
                name_img = pygame.transform.scale(name_img, (44, 20))
            player.text = name_img
            name_x_position = 180 + index*47
            player.set_text_pos((name_x_position, 145))


    def fetch_result(self, result_id, results: list):
        if result_id == 0:
            return

        results.append(self.database.execute("SELECT * FROM tulokset WHERE ID = (?)"
                                             , [result_id]).fetchone())

if __name__ == "__main__":
    d = DatabaseReader()
    d.show_game(1)
