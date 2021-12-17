class Player:
    """Luokka pelaajalle
    """
    def __init__(self, name: str):
        """Alustaa pelaajalle nimen ja tyhjän tuloslistan

        Args:
            name (string): pelaajan nimi
        """
        self.name = name
        self.rolling_in_progress = False
        self.marked = False
        self.phase = 0
        self.text = None  # rendered representation of name
        self.text_pos = None
        self.results = {"Ykköset":     0,
                        "Kakkoset":    0,
                        "Kolmoset":    0,
                        "Neloset":     0,
                        "Viitoset":    0,
                        "Kuutoset":    0,
                        "Välisumma":   0,
                        "1 pari":      0,
                        "2 paria":     0,
                        "3 samaa":     0,
                        "4 samaa":     0,
                        "Pieni suora": 0,
                        "Suuri suora": 0,
                        "Täyskäsi":    0,
                        "Sattuma":     0,
                        "Yatzy":       0,
                        "Yhteensä":    0}

    def played(self):
        """Palauttaa tiedon onko pelaaja jo pelannut

        Returns:
            bool: on / ei ole pelannut
        """
        for value in self.results.values():
            if value != 0:
                return True
        return False

    def set_text_pos(self, pos: tuple):
        """Asettaa nimitekstille paikan käyttöliittymään

        Args:
            pos (tuple): nimen koordinaatit
        """
        self.text_pos = (pos)

    def update_valisumma(self):
        """Päivittää tuloslistan välisumman
        (summa Ykköset, Kakkoset, ..., Kuutoset)
        """
        self.results["Välisumma"] = 0
        target_strings = ["Ykköset", "Kakkoset", "Kolmoset", "Neloset", "Viitoset", "Kuutoset"]
        for string in target_strings:
            if self.results[string] != 'x':
                self.results["Välisumma"] += self.results[string]
        if self.results["Välisumma"] >= 63:
            self.results["Välisumma"] += 50

    def mark_upstairs(self, result_name: int, result_value: int):
        """Päivittää tuloksen "yläkertaan" eli välille [Ykköset ... Kuutoset]
        Kutsuu update_valisumma() ja update_total()

        Args:
            result_name (string): Halutun tuloksen nimi
            result_value (int): Halutun tuloksen arvo
        """
        if result_value == 0:
            result_value = 'x'

        # self.results[target_strings[result_name]] = result_value
        self.results[result_name] = result_value
        self.update_valisumma()
        self.update_total()

    def mark_downstairs(self, result_name: str, result: int):
        """Päivittää tuloksen "alakertaan" eli välille [Pari ... Yatzy]
        Kutsuu update_total()

        Args:
            result_name (str): Halutun tuloksen nimi
            result (int): Halutun tuloksen arvo
        """
        if result == 0:
            result = 'x'

        self.results[result_name] = result
        self.update_total()

    def update_total(self):
        """Päivittää yhteispisteet, laskee yhteen kaiken muun paitsi
        "Välisumma" ja "Yhteensä"
        """
        items_to_sum = ["Välisumma",
                        "1 pari",
                        "2 paria",
                        "3 samaa",
                        "4 samaa",
                        "Pieni suora",
                        "Suuri suora",
                        "Täyskäsi",
                        "Sattuma",
                        "Yatzy"]

        total = 0
        for item in items_to_sum:
            if self.results[item] != 'x':
                total += self.results[item]

        self.results["Yhteensä"] = total
