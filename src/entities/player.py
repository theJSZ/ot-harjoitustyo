class Player:
    def __init__(self, name: str):
        """Alustaa pelaajalle nimen ja tyhjän tuloslistan

        Args:
            name (string): pelaajan nimi
        """
        self._name = name
        self._turn = None
        self._text = None  # rendered representation of name
        self._text_pos = None
        self._results = {"Ykköset":     0,
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
        for value in self._results.values():
            if value != 0:
                return True
        return False

    def get_results(self):
        """Palauttaa pelaajan tuloslistan

        Returns:
            dict: tuloslista
        """
        return self._results

    def get_name(self):
        """Palauttaa pelaajan nimen

        Returns:
            string: pelaajan nimi
        """
        return self._name

    def set_text(self, img):
        """Antaa pelaajalle kuvaesityksen nimestä

        Args:
            img: kuva nimestä
        """
        self._text = img

    def get_text(self):
        """Palauttaa kuvaesityksen nimestä

        Returns:
            image(?): kuva nimestä
        """
        return self._text

    def set_text_pos(self, pos: tuple):
        """Asettaa nimitekstille paikan käyttöliittymään

        Args:
            pos (tuple): nimen koordinaatit
        """
        self._text_pos = (pos)

    def get_text_pos(self):
        """Palauttaa nimen paikan käyttöliittymässä

        Returns:
            tuple: nimen koordinaatit
        """
        return self._text_pos

    def update_valisumma(self):
        """Päivittää tuloslistan välisumman
        (summa Ykköset, Kakkoset, ..., Kuutoset)
        """
        self._results["Välisumma"] = 0
        target_strings = ["Ykköset", "Kakkoset", "Kolmoset", "Neloset", "Viitoset", "Kuutoset"]
        for string in target_strings:
            if self._results[string] != 'x':
                self._results["Välisumma"] += self._results[string]
        if self._results["Välisumma"] >= 63:
            self._results["Välisumma"] += 50

    def mark_upstairs(self, result_name: int, result_value: int):
        """Päivittää tuloksen "yläkertaan" eli välille [Ykköset ... Kuutoset]
        Kutsuu update_valisumma() ja update_total()

        Args:
            result_name (string): Halutun tuloksen nimi
            result_value (int): Halutun tuloksen arvo
        """
        target_strings = ["", "Ykköset", "Kakkoset", "Kolmoset", "Neloset", "Viitoset", "Kuutoset"]
        if result_value == 0:
            result_value = 'x'
        if self._results[target_strings[result_name]] != 0:
            print("something is wrong, trying to mark over existing result")
            return
        self._results[target_strings[result_name]] = result_value
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
        if self._results[result_name] != 0:
            print("something is wrong, trying to mark over existing result")
            return
        self._results[result_name] = result
        self.update_total()

    def update_total(self):
        """Päivittää yhteispisteet, laskee yhteen kaiken muun paitsi
        "Välisumma" ja "Yhteensä"
        """
        total = 0
        for name, value in self._results.items():
            if value == 'x' or name in ["Ykköset", "Kakkoset", "Kolmoset", "Neloset", "Viitoset", "Kuutoset", "Yhteensä"]: # or name == "Yhteensä":
                continue
            total += value

        self._results["Yhteensä"] = total
