import sqlite3

class DatabaseInterface:
    def __init__(self):
        self.db = sqlite3.connect("./data/yatzy.db")
        self.db.isolation_level = None

    def create_tables(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS tulokset(id INTEGER PRIMARY KEY, 
            ykköset INTEGER, kakkoset INTEGER, kolmoset INTEGER, neloset INTEGER, 
            viitoset INTEGER, kuutoset INTEGER, pari INTEGER, kaksi_paria INTEGER, 
            kolme_samaa INTEGER, neljä_samaa INTEGER, pikku_suora INTEGER, 
            iso_suora INTEGER, täyskäsi INTEGER, sattuma INTEGER, yatzy INTEGER, pelaaja TEXT)""")

        self.db.execute(
            """CREATE TABLE IF NOT EXISTS pelit(id INTEGER PRIMARY KEY, 
            tulos1 INTEGER DEFAULT 0 REFERENCES tulokset, tulos2 INTEGER DEFAULT 0 REFERENCES tulokset, 
            tulos3 INTEGER DEFAULT 0 REFERENCES tulokset, tulos4 INTEGER DEFAULT 0 REFERENCES tulokset)""")

    def add_game(self, players: list):
        result_ids = [0, 0, 0, 0]
        for index, player in enumerate(players):
            results = player.results
            for result in results:
                if result == 'x':
                    result = 0
            self.db.execute(
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
                      player.name]
            )
            result_id = self.db.execute("SELECT MAX(id) from tulokset").fetchone()[0]
            result_ids[index] = int(result_id)

        self.db.execute("""INSERT INTO pelit(tulos1, tulos2, tulos3, tulos4)
        VALUES(?, ?, ?, ?)""", [result_ids[0], result_ids[1], result_ids[2], result_ids[3]]
        )


d = DatabaseInterface()
d.create_tables()