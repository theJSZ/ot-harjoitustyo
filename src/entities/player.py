from resources.clickable_result_names import CLICKABLE_RESULTS


class Player:
    """Luokka pelaajalle
    """
    def __init__(self, name: str, position: int=None):
        """Alustaa pelaajalle nimen ja tyhjän tuloslistan

        Args:
            name (string): pelaajan nimi
        """
        self.name = name
        self.position = position
        self.rolling_in_progress = False
        self.marked = False
        self.phase = 0
        self.text = None  # rendered representation of name
        self.text_pos = None
        self.results = self.init_results()

    def init_results(self):
        """Alustaa pelaajan tuloslistan

        Returns:
            dict: Tulokset avain-arvo-pareina
        """
        results = {}
        for result_name in CLICKABLE_RESULTS:
            results[result_name] = 0

        return results

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
        target_strings = CLICKABLE_RESULTS[0:6]

        for string in target_strings:
            if self.results[string] != 'x':
                self.results["Välisumma"] += self.results[string]
        if self.results["Välisumma"] >= 63:
            self.results["Välisumma"] += 50

    def mark_result(self, result_name: int, result_value: int):
        """Päivittää tuloksen annettuun ruutuun.
        Kutsuu update_valisumma() ja update_total()

        Args:
            result_name (string): Halutun tuloksen nimi
            result_value (int): Halutun tuloksen arvo
        """
        if result_value == 0:
            result_value = 'x'

        self.results[result_name] = result_value
        self.update_valisumma()
        self.update_total()

    def update_total(self):
        """Päivittää yhteispisteet
        """

        total = 0

        for item in CLICKABLE_RESULTS[6:] + ["Välisumma"]:
            if self.results[item] != 'x':
                total += self.results[item]

        self.results["Yhteensä"] = total
