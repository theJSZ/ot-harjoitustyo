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
    """Luokka tietokantaan kirjoittamiseen, luo tietokannan
    jos sitä ei ole
    """
    def __init__(self):
        self.database = sqlite3.connect("./data/yatzy.db")
        self.database.isolation_level = None
        self.create_tables()
        self.date = datetime.now()
    def create_tables(self):
        """Luo tarvittavat taulut tietokantaan
        """
        self.database.execute(
            """CREATE TABLE IF NOT EXISTS tulokset(id INTEGER PRIMARY KEY,
            ykköset INTEGER, kakkoset INTEGER, kolmoset INTEGER, neloset INTEGER,
            viitoset INTEGER, kuutoset INTEGER, pari INTEGER, kaksi_paria INTEGER,
            kolme_samaa INTEGER, neljä_samaa INTEGER, pikku_suora INTEGER,
            iso_suora INTEGER, täyskäsi INTEGER, sattuma INTEGER, yatzy INTEGER, pelaaja TEXT)""")

        self.database.execute(
            """CREATE TABLE IF NOT EXISTS pelit(id INTEGER PRIMARY KEY,
            tulos1_id INTEGER DEFAULT 0 REFERENCES tulokset,
            tulos2_id INTEGER DEFAULT 0 REFERENCES tulokset,
            tulos3_id INTEGER DEFAULT 0 REFERENCES tulokset,
            tulos4_id INTEGER DEFAULT 0 REFERENCES tulokset,
            date DATE)""")

        self.database.execute(
            """CREATE TABLE IF NOT EXISTS totals(id INTEGER PRIMARY KEY,
            tulos_id INTEGER REFERENCES tulokset, tulos INTEGER)"""
        )

    def add_game(self, players: list):
        """Lisää pelaajien tulokset tietokantaan
        """
        result_ids = [0, 0, 0, 0]
        year = self.date.year
        month = self.date.month
        day = self.date.day
        timestamp = f'{year}-{month:02d}-{day:02d}'

        for index, player in enumerate(players):
            results = player.results
            total = results["Yhteensä"]
           
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

            self.database.execute("""INSERT INTO totals (tulos_id, tulos)
                                  VALUES (?, ?)""", [result_id, total])
 
        self.database.execute("""INSERT INTO pelit(tulos1_id, tulos2_id, tulos3_id, tulos4_id, date)
        VALUES(?, ?, ?, ?, ?)""", [result_ids[0],
                                   result_ids[1],
                                   result_ids[2],
                                   result_ids[3],
                                   timestamp])

        
class DatabaseReader:
    """Luokka tietokannan lukemiseen
    """
    def __init__(self):
        self.display = pygame.display.set_mode((377, 760))
        self.database = sqlite3.connect("./data/yatzy.db")
        self.database.isolation_level = None
        self.drawer = Drawer(self)

    def find_grand_champion(self, database):
        """Etsii parhaan yksittäisen tuloksen
        ja sille pelaajan tietokannasta

        Args:
            database (db): tutkittava tietokanta

        Returns:
            [tuple]: (pelaajan nimi, tulos)
        """
        high_score, high_score_id = database.execute("SELECT MAX(tulos), tulos_id FROM totals").fetchone()
        grand_champion = database.execute("SELECT pelaaja FROM tulokset WHERE id = (?)", [high_score_id]).fetchone()[0]
        return (grand_champion, high_score)

    def show_game(self, game_id: int = None):
        """Etsii tietokannasta pelin annetulla id-numerolla
        ja piirtää sen näytölle

        Args:
            game_id (int, optional): haluttu id. Jos None, hakee uusimman pelin
        """
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

        grand_champion, high_score = self.find_grand_champion(self.database)
        self.drawer.draw_annotation(f'Grand Champion: {grand_champion} - {high_score}', False, -80)
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
        """Hakee yhden yksittäisen tuloksen
        (eli sarakkeen yatzy-lapusta)

        Args:
            result_id (int): halutun tuloksen id
            results (list): tulos listana
        """
        if result_id == 0:
            return

        results.append(self.database.execute("SELECT * FROM tulokset WHERE id = (?)"
                                             , [result_id]).fetchone())

if __name__ == "__main__":

    # testailua
    # player = Player("JSZ")
    # player.results = {"Ykköset":     3,
    #                   "Kakkoset":    6,
    #                   "Kolmoset":    9,
    #                   "Neloset":     12,
    #                   "Viitoset":    15,
    #                   "Kuutoset":    18,
    #                   "Välisumma":   0,
    #                   "1 pari":      12,
    #                   "2 paria":     16,
    #                   "3 samaa":     15,
    #                   "4 samaa":     8,
    #                   "Pieni suora": 15,
    #                   "Suuri suora": 'x',
    #                   "Täyskäsi":    24,
    #                   "Sattuma":     15,
    #                   "Yatzy":       'x',
    #                   "Yhteensä":    0}

    # player.update_valisumma()
    # player.update_total()

    # players = [player]

    # d = DatabaseWriter()
    # d.add_game(players)

    dr = DatabaseReader()
    dr.show_game()