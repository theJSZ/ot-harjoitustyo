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
                         "Yatzy":       0}

    def __str__(self):
        return self._name

    def set_turn(self, turn):
        self._turn = turn

    def get_turn(self):
        return self._turn

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

    def mark_upstairs(self, target: int, dice: list):
        target_strings = ["", "Ykköset", "Kakkoset", "Kolmoset", "Neloset", "Viitoset", "Kuutoset"]
        for die in dice:
            if die.get_face() == target:
                self._results[target_strings[target]] += target

    def mark_twos(self, dice: list):
        pass

    def mark_threes(self, dice: list):
        pass

    def mark_fours(self, dice: list):
        pass

    def mark_fives(self, dice: list):
        pass

    def mark_sixes(self, dice: list):
        pass

    def mark_pair(self, dice: list):
        pass

    def mark_two_pair(self, dice: list):
        pass

    def mark_three_kind(self, dice: list):
        pass

    def mark_four_kind(self, dice: list):
        pass

    def mark_small_straight(self, dice: list):
        pass

    def mark_large_straight(self, dice: list):
        pass

    def mark_full_house(self, dice: list):
        pass

    def mark_chance(self, dice: list):
        pass

    def mark_yatzy(self, dice: list):
        pass
