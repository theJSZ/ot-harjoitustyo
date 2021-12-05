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

    def update_valisumma(self):
        self._results["Välisumma"] = 0
        target_strings = ["Ykköset", "Kakkoset", "Kolmoset", "Neloset", "Viitoset", "Kuutoset"]
        for string in target_strings:
            if self._results[string] != 'x':
                self._results["Välisumma"] += self._results[string]
        if self._results["Välisumma"] >= 63:
            self._results["Bonus"] = 50

    def mark_upstairs(self, target: int, dice: list):
        target_strings = ["", "Ykköset", "Kakkoset", "Kolmoset", "Neloset", "Viitoset", "Kuutoset"]
        if self._results[target_strings[target]] != 0:
            return False
        for die in dice:
            if die.get_face() == target:
                self._results[target_strings[target]] += target
        if self._results[target_strings[target]] == 0:
            self._results[target_strings[target]] = 'x'
        return True                        

    def mark_pair(self, dice: list):
        if self._results["1 pari"] != 0:
            return False
        faces = [0 for _ in range(7)]
        for die in dice:
            faces[die.get_face()] += 1

        for face in range(6, 0, -1):
            if faces[face] >= 2:
                self._results["1 pari"] = 2*face
                return
        self._results["1 pari"] = 'x'
        return True

    def mark_two_pair(self, dice: list):
        if self._results["2 paria"] != 0:
            return False
        faces = [0 for _ in range(7)]
        total = 0
        for die in dice:
            faces[die.get_face()] += 1

        pairs = set()
        for face in range(6, 0, -1):
            if faces[face] >= 2:
                pairs.add(face)
        if len(pairs) < 2:
            self._results["2 paria"] = 'x'
        else:
            total = 0
            total += max(pairs)*2
            pairs.remove(max(pairs))
            total += max(pairs)*2
            self._results["2 paria"] = total
        return True

    def mark_three_kind(self, dice: list):
        if self._results["3 samaa"] != 0:
            return False
        faces = [0 for _ in range(7)]
        total = 'x'
        for die in dice:
            faces[die.get_face()] += 1
            if faces[die.get_face()] == 3:
                total = 3*die.get_face()
        self._results["3 samaa"] = total
        return True

    def mark_four_kind(self, dice: list):
        if self._results["4 samaa"] != 0:
            return False
        faces = [0 for _ in range(7)]
        total = 'x'
        for die in dice:
            faces[die.get_face()] += 1
            if faces[die.get_face()] == 4:
                total = 4*die.get_face()
        self._results["4 samaa"] = total
        return True

    def mark_small_straight(self, dice: list):
        if self._results["Pieni suora"] != 0:
            return False
        faces = []
        for die in dice:
            faces.append(die.get_face())
        if sorted(faces) == [1, 2, 3, 4, 5]:
            self._results["Pieni suora"] = 15
        else:
            self._results["Pieni suora"] = 'x'
        return True

    def mark_large_straight(self, dice: list):
        if self._results["Suuri suora"] != 0:
            return False
        faces = []
        for die in dice:
            faces.append(die.get_face())
        if sorted(faces) == [2, 3, 4, 5 ,6]:
            self._results["Suuri suora"] = 20
        else:
            self._results["Suuri suora"] = 'x'
        return True

    def mark_full_house(self, dice: list):
        if self._results["Täyskäsi"] != 0:
            return False
        die_set = set()
        total = 0
        for die in dice:
            die_set.add(die.get_face())
        if len(die_set) == 2:
            for die in dice:
                total += die.get_face()
        else:
            total = 'x'
        self._results["Täyskäsi"] = total
        return True

    def mark_chance(self, dice: list):
        if self._results["Sattuma"] != 0:
            return False
        total = 0
        for die in dice:
            total += die.get_face()
        self._results["Sattuma"] = total
        return True

    def mark_yatzy(self, dice: list):
        if self._results["Yatzy"] != 0:
            return False
        if sorted(dice)[0] == sorted(dice)[4]:
            total = 50
        else:
            total = 'x'
        self._results["Yatzy"] = total
        return True