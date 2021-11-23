class Player:
    def __init__(self, name):
        self._name = name
        self._turn = None
        self._text = None  # rendered representation of name
        self._textPos = None
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

    def setTurn(self, turn):
        self._turn = turn

    def getTurn(self):
        return self._turn

    def getResults(self):
        return self._results

    def getName(self):
        return self._name

    def setText(self, img):
        self._text = img

    def getText(self):
        return self._text

    def setTextPos(self, pos):
        self._textPos = (pos)

    def getTextPos(self):
        return self._textPos

    def markUpstairs(self, target: int, dice: list):
        target_strings = ["", "Ykköset", "Kakkoset", "Kolmoset", "Neloset", "Viitoset", "Kuutoset"]
        for Die in dice:
            if Die.getFace() == target:
                self._results[target_strings[target]] += target

    def markTwos(self, dice: list):
        pass

    def markThrees(self, dice: list):
        pass

    def markFours(self, dice: list):
        pass

    def markFives(self, dice: list):
        pass

    def markSixes(self, dice: list):
        pass

    def markPair(self, dice: list):
        pass

    def markTwoPair(self, dice: list):
        pass

    def markThreeKind(self, dice: list):
        pass

    def markFourKind(self, dice: list):
        pass

    def markSmallStraight(self, dice: list):
        pass

    def markLargeStraight(self, dice: list):
        pass

    def markFullHouse(self, dice: list):
        pass

    def markChance(self, dice: list):
        pass

    def markYatzy(self, dice: list):
        pass