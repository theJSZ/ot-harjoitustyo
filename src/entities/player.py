class Player:
    def __init__(self, name):
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
                         "Bonus":       0,
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

    def get_results(self):
        return self._results

    def get_name(self):
        return self._name

    def set_text(self, img):
        self._text = img

    def get_text(self):
        return self._text

    def set_text_pos(self, pos):
        self._text_pos = (pos)

    def get_text_pos(self):
        return self._text_pos

    def update_valisumma(self):
        self._results["Välisumma"] = 0
        target_strings = ["Ykköset", "Kakkoset", "Kolmoset", "Neloset", "Viitoset", "Kuutoset"]
        for string in target_strings:
            if self._results[string] != 'x':
                self._results["Välisumma"] += self._results[string]
        if self._results["Välisumma"] >= 63:
            self._results["Bonus"] = 50

    def mark_upstairs(self, result_name: int, result_value: int):
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
        if result == 0:
            result = 'x'
        if self._results[result_name] != 0:
            print("something is wrong, trying to mark over existing result")
            return
        self._results[result_name] = result
        self.update_total()

    def update_total(self):
        total = 0
        for key, value in self._results.items():
            if value == 'x' or key == "Välisumma" or key == "Yhteensä":
                continue
            total += value

        self._results["Yhteensä"] = total
